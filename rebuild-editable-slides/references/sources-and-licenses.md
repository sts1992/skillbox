# Primary sources and dependency choices

Checked 2026-10-02. These are upstream references, not a promise that every feature works on every source.

- [pdfplumber documentation](https://github.com/jsvine/pdfplumber/blob/stable/README.md): characters with bbox/font/style, vector geometry, table detection. [Color interpretation](https://github.com/jsvine/pdfplumber/blob/stable/docs/colors.md) has limitations for unusual color spaces. [MIT license](https://github.com/jsvine/pdfplumber/blob/stable/LICENSE.txt).
- [pdfminer.six layout analysis](https://pdfminersix.readthedocs.io/en/latest/topic/converting_pdf_to_text.html): text grouping is heuristic. [MIT license](https://github.com/pdfminer/pdfminer.six/blob/master/LICENSE).
- [Tesseract CLI](https://tesseract-ocr.github.io/tessdoc/Command-Line-Usage.html): language/segmentation options and TSV/hOCR. [Input formats](https://tesseract-ocr.github.io/tessdoc/InputFormats.html): PDFs must be rasterized before OCR. [Quality guidance](https://tesseract-ocr.github.io/tessdoc/ImproveQuality.html). [Apache-2.0 license](https://github.com/tesseract-ocr/tesseract/blob/main/LICENSE).
- [Official models](https://tesseract-ocr.github.io/tessdoc/): language models are separate; best/fast require LSTM OCR. [Japanese vertical model](https://github.com/tesseract-ocr/tessdata_best/blob/main/jpn_vert.traineddata).
- [Poppler upstream](https://poppler.freedesktop.org/): local PDF rendering. GPL-family licensing applies; inspect the exact distribution's notices before bundling. This skill invokes an existing installation and redistributes no Poppler binary.
- [pypdfium2 licensing](https://pypdfium2.readthedocs.io/en/stable/readme.html#licensing): an alternative renderer with permissive wrapper/PDFium licenses and dependency notices. Not required by bundled scripts.
- [PyMuPDF licensing](https://pymupdf.io/licensing): AGPL or commercial licensing. Powerful optional geometry extraction, but not used by this implementation. Review obligations for the intended distribution/deployment rather than assuming every private local use needs a paid license.
- [WebPlotDigitizer workflow](https://automeris.io/docs/digitize/): data digitization requires calibration and interpretation. Useful when explicitly reconstructing estimates, not proof of original chart values.

The renderer uses the supplied `@oai/artifact-tool` runtime. That dependency is not bundled, relicensed or installed by this skill. Follow the available Presentations runtime and validation instructions. The original scripts in this skill are workflow code; dependency licenses remain separate. No external conversion/OCR API is called.
