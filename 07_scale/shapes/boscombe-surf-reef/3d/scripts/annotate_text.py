"""Page crops of the two ICCE papers with the sentences / table rows used for the 3D model highlighted (private research copies).
Source PDFs: https://icce-ojs-tamu.tdl.org/icce/article/download/1352/pdf_106 (Mead et al. 2010) and
             https://icce-ojs-tamu.tdl.org/icce/article/download/6794/pdf_441/27535 (Rendle & Davidson 2012). Path to local copies via env PDF_DIR."""
import os, sys
from pathlib import Path
import fitz
from PIL import Image, ImageDraw, ImageFont
HERE = Path(__file__).resolve().parent
OUT = HERE.parent / "annotated"; OUT.mkdir(exist_ok=True)
PDF_DIR = Path(os.environ.get("PDF_DIR", "C:/Users/lior/AppData/Local/Temp/claude/C--/06e3858c-68a5-4ccd-8162-d4bb676180d2/scratchpad/bosc3d"))

# job: (pdf, page number (1-based), needles to highlight (exact phrase search), clip rect for word highlighting or None, crop pad, out name, caption)
JOBS = [
    ("mead2010.pdf", 2, ["Table 1. Water levels", "crest height of 0.5 m above chart datum"], (255, 292, 350, 377), (60, 25), "text_mead2010_p2_table1_and_crest.png",
     "Mead et al. (2010) p.2: Table 1 water levels at Boscombe (m ACD) and the design crest height (+0.5 m above chart datum)"),
    ("mead2010.pdf", 3, ["water depths of 3-5 m", "(CD)"], None, (45, 45), "text_mead2010_p3_design_depth.png",
     "Mead et al. (2010) p.3: design set in water depths of 3-5 m (CD)"),
    ("mead2010.pdf", 1, ["tidal", "MHWS and MLWS at", "raise the crest to a"], None, (30, 60), "text_mead2010_p1_tide_gauge.png",
     "Mead et al. (2010) p.1: tide gauge on Bournemouth Pier, MHWS-MLWS range 1.76 m, crest raised above MLWS"),
    ("rendle2012.pdf", 3, ["225 m offshore in 2.7 to 5 m depth", "maximum spring tidal"], None, (60, 60), "text_rendle2012_depth_tides.png",
     "Rendle & Davidson (2012) p.3: 225 m offshore, 2.7-5 m depth; maximum spring tidal range 1.96 m"),
    ("rendle2012.pdf", 8, ["mean sea level (MSL) is equivalent to Chart Datum", "-3.5 m contour has eroded"], None, (60, 60), "text_rendle2012_datum_sentence.png",
     "Rendle & Davidson (2012) p.8: the (garbled) datum sentence discussed in METHODS_3D.md (assumption A3)"),
]

def run():
    for pdf, pno, needles, wclip, pad, name, cap in JOBS:
        doc = fitz.open(PDF_DIR / pdf)
        page = doc[pno - 1]
        rects = []
        for nd in needles:
            if nd in ("tidal",):
                continue
            rects += page.search_for(nd)
        if wclip:
            for w in page.get_text("words", clip=fitz.Rect(*wclip)):
                rects.append(fitz.Rect(w[:4]))
        if not rects:
            print("NOT FOUND", name); continue
        for r in rects:
            page.add_highlight_annot(r)
        u = fitz.Rect(rects[0])
        for r in rects: u |= r
        clip = fitz.Rect(page.rect.x0, max(page.rect.y0, u.y0 - pad[0]), page.rect.x1, min(page.rect.y1, u.y1 + pad[1]))
        pix = page.get_pixmap(matrix=fitz.Matrix(2.2, 2.2), clip=clip, annots=True)
        img = Image.frombytes("RGB", (pix.width, pix.height), pix.samples)
        strip = Image.new("RGB", (img.width, 34), (30, 30, 30)); ImageDraw.Draw(strip).text((8, 8), "ANNOTATED CROP (page %d, highlight added): %s. Private research copy." % (pno, cap), font=ImageFont.truetype("arial.ttf", 15), fill=(255, 255, 255))
        out = Image.new("RGB", (img.width, img.height + 34)); out.paste(strip, (0, 0)); out.paste(img, (0, 34)); out.save(OUT / name, optimize=True)
        print(name, "rects", len(rects), "crop h", img.height)

if __name__ == "__main__":
    run()
