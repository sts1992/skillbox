# OCR and fidelity

For born-digital PDF, prefer text/vector extraction to OCR. The draft uses words with font/color information and coarse rectangles/lines; PDF paint order, clipping, gradients and logical grouping are not reconstructed automatically. A table candidate may simply be three diagram boxes.

For scans, rasterize at about 300 dpi (or sufficient pixels for the smallest text) using `pdftoppm -r 300 -png input.pdf page`. Then use the image extractor. The built-in PDF preview is 96 dpi and suited to layout evidence, not guaranteed OCR quality. For small text in a scanned PDF, explicitly use the higher-resolution image route rather than trusting low-resolution OCR.

Check `tesseract --list-langs`. Use installed `jpn+eng` for Japanese/English and a supported vertical model such as `jpn_vert` for vertical Japanese. Do not assume models exist. If missing, use agent visual transcription or install official models only when environment permissions allow. Japanese text often has no spaces: OCR word joins in the draft need proofreading. The skill does not bundle models or auto-download them.

Choose segmentation by region: `--psm 11` for sparse labels (default), 6 for a uniform block, 7 for one line. Deskew and inspect contrast/alpha if text recognition is poor. Preserve raw TSV evidence. OCR confidence is an engine score, not a calibrated probability of semantic correctness.

Fonts cannot generally be recovered/licensed from a screenshot. Prefer an available close family; record substitutions and inspect line breaks. Japanese font fallback needs an actual installed CJK font. A font name in OOXML alone does not prove PowerPoint has that font. Do not embed third-party fonts without appropriate rights.

For charts without complete source data, do not manufacture spreadsheet values. Either rebuild the visible chart as editable shapes/labels and state the limitation, or ask for data. Reconstructing a graphic and recovering original data are separate tasks.

Render every final slide and compare it with the source at equal dimensions. Use pixel differences only as a diagnostic; anti-aliasing and font differences can dominate. Inspect text/cell/connector coverage and numbers explicitly. Do not trade missing evidence for a high image-similarity score. Do not hide a screenshot behind editable overlays.
