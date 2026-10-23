-- Pandoc Lua filter: clickable cross-references.
--  * "Appendix X", "Appendix X.n", "Section X.n", "Appendices A to F" -> link to the appendix / appendix-section heading
--  * "Figure N" / "Table N" (also E1, G3 ...) -> link to the caption that starts "**Figure N.**" / "**Table N.**"
-- The Markdown source is not changed. Runs before tables.lua.
local stringify = pandoc.utils.stringify
local targets = {}   -- key ("A", "A.14") -> heading identifier
local caps = {}      -- "Figure 1" / "Table C2" -> anchor name

local function prescan(doc)
  for _, b in ipairs(doc.blocks) do
    if b.t == 'Header' then
      local s = stringify(b)
      local L = s:match('^Appendix (%a)%.')
      if L then targets[L] = b.identifier end
      local k = s:match('^(%a%.%d+)%s')
      if k then targets[k] = b.identifier end
    end
  end
end

local function cap_key(s)
  local k, n = s:match('^(%a+) (%a?%d+)%.')
  if (k == 'Figure' or k == 'Table') and n then return k .. ' ' .. n end
end

local function anchor(key) return 'cap-' .. key:gsub(' ', '-') end

local function lead_anchor(inls)
  local f = inls[1]
  if f and f.t == 'Strong' then
    local key = cap_key(stringify(f))
    if key and not caps[key] then caps[key] = anchor(key); return key end
  end
end

local function mark_caps(doc)
  -- add a hypertarget at the start of every caption paragraph / figure caption
  local function fix(inls)
    local key = lead_anchor(inls)
    if key then inls:insert(1, pandoc.RawInline('latex', '\\protect\\hypertarget{' .. caps[key] .. '}{}')) end
  end
  doc = doc:walk({
    Para = function(p) fix(p.content); return p end,
    Plain = function(p) fix(p.content); return p end,
    Figure = function(f)
      for _, b in ipairs(f.caption.long) do
        if b.t == 'Para' or b.t == 'Plain' then fix(b.content) end
      end
      return f
    end })
  return doc
end

-- split "A.14," into (core "A.14", trailing ",")
local function core(s, pat)
  local c = s:match(pat)
  if not c then return nil end
  return c, s:sub(#c + 1)
end

local function linkify(inls)
  local out, i, n = pandoc.List(), 1, #inls
  local function sp(j) return inls[j] and (inls[j].t == 'Space' or inls[j].t == 'SoftBreak') end
  while i <= n do
    local e = inls[i]
    local done = false
    if e.t == 'Str' and (e.text == 'Appendix' or e.text == 'Appendices' or e.text == 'Section') and sp(i + 1)
       and inls[i + 2] and inls[i + 2].t == 'Str' then
      local word = e.text
      local c, rest = core(inls[i + 2].text, '^%u%.%d+')
      if not c and word ~= 'Section' then c, rest = core(inls[i + 2].text, '^%u') ; if c and #inls[i+2].text > 1 and inls[i+2].text:sub(2,2):match('%w') then c = nil end end
      if c and targets[c] then
        out:insert(pandoc.Link({e, inls[i + 1], pandoc.Str(c)}, '#' .. targets[c]))
        if rest ~= '' then out:insert(pandoc.Str(rest)) end
        i = i + 3; done = true
        -- "Appendices A to F" / "A and B": link the following letters too
        if word == 'Appendices' then
          while sp(i) and inls[i + 1] and inls[i + 1].t == 'Str' and (inls[i + 1].text == 'to' or inls[i + 1].text == 'and')
                and sp(i + 2) and inls[i + 3] and inls[i + 3].t == 'Str' do
            local c2, r2 = core(inls[i + 3].text, '^%u')
            if c2 and targets[c2] and not inls[i+3].text:sub(2,2):match('%w') then
              out:insert(inls[i]); out:insert(inls[i + 1]); out:insert(inls[i + 2])
              out:insert(pandoc.Link({pandoc.Str(c2)}, '#' .. targets[c2]))
              if r2 ~= '' then out:insert(pandoc.Str(r2)) end
              i = i + 4
            else break end
          end
        end
      end
    elseif e.t == 'Str' and (e.text == 'Figure' or e.text == 'Table') and sp(i + 1)
       and inls[i + 2] and inls[i + 2].t == 'Str' then
      local c, rest = core(inls[i + 2].text, '^%u?%d+')
      local key = c and (e.text .. ' ' .. c)
      if key and caps[key] and not (rest:sub(1, 1):match('%d')) then
        out:insert(pandoc.Link({e, inls[i + 1], pandoc.Str(c)}, '#' .. caps[key]))
        if rest ~= '' then out:insert(pandoc.Str(rest)) end
        i = i + 3; done = true
      end
    end
    if not done then out:insert(e); i = i + 1 end
  end
  return out
end

function Pandoc(doc)
  prescan(doc)
  -- collect caption anchors first (so forward references work), then mark and link
  doc = mark_caps(doc)
  return doc:walk({
    traverse = 'topdown',
    Header = function(h) return h, false end,
    Link = function(l) return l, false end,
    Strong = function(st) if cap_key(stringify(st)) then return st, false end end,
    Inlines = function(inls) return linkify(inls) end,
  })
end
