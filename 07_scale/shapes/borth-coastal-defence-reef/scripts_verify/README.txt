Scripts used in the 2026-10-06 verification of borth-coastal-defence-reef (copied from the session scratchpad; paths inside them point to that scratchpad, edit D / base before running).
recompute.py  independent canonical-frame recompute (Web-Mercator -> local metres -> frame); prints max diff to shape.json
sop.py        OS-grid setting-out points R1-R15 (drawing 9V5090/1020) -> WGS84 -> pixel on the 2024 image (pyproj EPSG:27700)
design1.py    georeference the vector PDF of drawing 1020 by its 15 setting-out points (similarity fit)
design2.py    extract the concentric toe rings of both reefs from the PDF vector paths (needs the PDF in dl/plans/)
compare3.py   IoU / centroid offsets: design rings vs traced polygons
lidar1-3.py   read the Welsh Government LiDAR tile SN6089 (download URL in HANDOFF.md): masks, crest percentiles, slopes, axis profiles
figs1.py, figs2.py  the two figures in overlays/ ; adds.py  builds alt_outlines_m in the canonical frame
