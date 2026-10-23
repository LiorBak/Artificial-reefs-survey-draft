-- Pandoc Lua filter for the LaTeX build: sensible column widths, smaller type for wide tables,
-- landscape pages (with their caption paragraph) for wide tables; table captions below the table in footnote size.
local stringify = pandoc.utils.stringify

local function words_max(s)
  local m = 0
  for w in s:gmatch('%S+') do if #w > m then m = #w end end
  return m
end

local function analyse(tbl)
  local n = #tbl.colspecs
  local maxlen, sumlen, cnt, maxword = {}, {}, {}, {}
  for i = 1, n do maxlen[i] = 0; sumlen[i] = 0; cnt[i] = 0; maxword[i] = 0 end
  local function row(r)
    for i, c in ipairs(r.cells) do
      if i <= n then
        local s = stringify(pandoc.Blocks(c.contents):walk({ Note = function() return {} end }))
        local l = #s
        if l > 0 then
          sumlen[i] = sumlen[i] + l; cnt[i] = cnt[i] + 1
          if l > maxlen[i] then maxlen[i] = l end
          local mw = words_max(s)
          if mw > maxword[i] then maxword[i] = mw end
        end
      end
    end
  end
  -- wide tables (10+ columns): header words may wrap, so the widths follow the body only
  if n < 10 then for _, r in ipairs(tbl.head.rows) do row(r) end end
  for _, b in ipairs(tbl.bodies) do for _, r in ipairs(b.body) do row(r) end end
  local w, tot = {}, 0
  for i = 1, n do
    local mean = cnt[i] > 0 and sumlen[i] / cnt[i] or 1
    local x = math.min(0.5 * maxlen[i] + 0.5 * mean, 48)
    x = math.max(x, maxword[i] * 1.45 + 2, 4)
    -- wide tables: text (left-aligned) columns wrap worse than short numbers, so they get more room
    if n >= 10 and tbl.colspecs[i][1] == 'AlignLeft' and maxlen[i] > 8 then x = x * 1.4 end
    w[i] = x; tot = tot + x
  end
  for i = 1, n do
    local al = tbl.colspecs[i][1]
    tbl.colspecs[i] = {al, w[i] / tot}
  end
  -- io.stderr:write(string.format('TABLE cols=%d weight=%.0f\n', n, tot))
  return n, tot
end

local function starts_with_table(b)
  if b.t ~= 'Para' and b.t ~= 'Plain' then return false end
  local f = b.content[1]
  return f and f.t == 'Strong' and stringify(f):match('^Table') ~= nil
end

function Blocks(blocks)
  local out = {}
  for _, b in ipairs(blocks) do
    if b.t == 'Table' then
      local n, tot = analyse(b)
      local size = n >= 10 and '\\scriptsize' or (n >= 7 and '\\footnotesize' or nil)
      local land = n >= 8 and tot >= 150
      -- the caption paragraph ("**Table N.** ...") written above the table in Markdown is set BELOW the table,
      -- in footnote size (the same size as the figure captions), kept on the page of the table's last row
      local cap
      if #out > 0 and starts_with_table(out[#out]) then cap = table.remove(out) end
      if land then out[#out + 1] = pandoc.RawBlock('latex', '\\begin{landscape}') end
      -- in wide (landscape) tables the cell notes are set in script size so that table and notes share one page
      out[#out + 1] = pandoc.RawBlock('latex', '\\begingroup\\let\\origfootnotesize\\footnotesize'
        .. (size and ('\\renewcommand{\\tablefont}{' .. (size == '\\footnotesize' and '\\origfootnotesize' or size) .. '}') or '')
        .. (land and '\\let\\footnotesize\\scriptsize\\setlength{\\tabcolsep}{3.5pt}\\renewcommand{\\arraystretch}{1.0}' or ''))
      out[#out + 1] = b
      out[#out + 1] = pandoc.RawBlock('latex', '\\endgroup')
      if cap then
        out[#out + 1] = pandoc.RawBlock('latex', '\\nopagebreak[4]\\vspace{-2pt}\\begingroup\\footnotesize\\setlength{\\parindent}{0pt}')
        out[#out + 1] = cap
        out[#out + 1] = pandoc.RawBlock('latex', '\\par\\endgroup\\medskip')
      end
      if land then out[#out + 1] = pandoc.RawBlock('latex', '\\end{landscape}') end
    else
      out[#out + 1] = b
    end
  end
  return out
end

-- Figures: keep the widths of the Markdown attributes; limit the height so that image and (long) caption fit on a page.
function Figure(fig)
  local cap = 0
  for _, b in ipairs(fig.caption.long) do cap = cap + #stringify(b) end
  local lines = math.ceil(cap / 125)
  local cap_pt = lines * 10.5 + 14
  local avail = 690 - cap_pt - 24
  local pct = math.floor(100 * avail / 700)
  if pct > 85 then pct = 85 end
  if pct < 25 then pct = 25 end
  fig.content = fig.content:walk({
    Image = function(img)
      img.attributes.height = pct .. '%'
      return img
    end })
  return fig
end
