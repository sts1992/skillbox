---
name: rebuild-editable-slides
description: Reconstruct slide-like PDFs, screenshots, PNGs and JPEGs as editable PowerPoint text, shapes, connectors, tables and verified-data charts. Use for requests such as image-to-editable-PPT or PDFスライドを編集できるパワポにする. Requires visual interpretation and review; do not use for merely placing an image on a slide.
---

# Rebuild Editable Slides

Reconstruct the visible content and layout as native PowerPoint objects. Treat extraction as evidence, not original authoring structure. Preserve slide order, wording, numerical values, proportions and visual hierarchy. Do not rewrite the source or promise pixel-perfect, one-click recovery.

## Prerequisites

Use local files and a private working directory. The bundled extractor needs Python 3, `pdfplumber`, Pillow, Poppler `pdftoppm`, and optionally the Tesseract CLI with the source language models. The bundled renderer requires the supplied Codex JavaScript runtime with `@oai/artifact-tool` and `CODEX_PRIMARY_RUNTIME_NODE_MODULES`; it does not bundle that proprietary runtime. Do not invent universal compatibility or silently substitute a different backend. Read the available Presentations skill for runtime paths, native objects, finalization and delivery.

Check dependencies before a large job. Keep source files unchanged. Do not send private source documents to external OCR/conversion services without authorization. Password-protected or restricted documents require an authorized readable copy; do not bypass access controls.

## Workflow

1. Inspect representative source pages. Identify born-digital PDF text, raster scans, page sizes, rotation, language, density, photos, diagrams, tables and charts. Preserve page count unless the user chooses a subset. Start with one representative page before processing a large deck.
2. Extract evidence:
   - `python scripts/extract_layout.py input.pdf work/extracted --pages 1,2`
   - `python scripts/extract_layout.py slide.png work/extracted --lang jpn+eng`
   - If the required OCR language is unavailable, use `--no-ocr` for an image and transcribe visually; never claim English OCR read Japanese. For raster PDF pages, render first and use the image workflow. Missing tools are a blocker for that route, not permission to upload documents elsewhere.
3. Open every `page-*.png` and read `layout.draft.json`. Work in a copy named `layout.reviewed.json`. Use [the layout schema](references/layout-schema.md) for the supported native objects.
   - Check exact text against the source; fix OCR, order, punctuation, units and signs. Group word boxes into meaningful text objects without losing mixed styling.
   - Correct colors and fonts. PDF glyph boxes are not text-frame bounds. Leave real baseline/descent room, use zero default text insets, and inspect wrapping. Record every font substitution in `fontMap` and the review notes.
   - Reconstruct rectangles/lines and supported diagrams as native shapes. Use actual attached connectors when the source expresses connections. Preserve stacking order deliberately; PDF extraction does not recover it reliably.
   - Promote a verified grid to one native table. Remove its old line/rectangle/text objects to prevent duplicates. Preserve cell text, merged cells and proportions. Table candidates can be false positives, especially diagram boxes.
   - Create native charts only from exact source values, printed labels or supplied data. Require `dataVerified` and `dataSource`. If values are unknown, retain editable axes/labels/shapes as a visual approximation and disclose that the chart data was not recovered, or ask for source data. Do not invent precise values from unlabeled bars.
   - Keep photos/logos or irreducible artwork as cropped image objects, with `rasterReason`. Never insert the full slide as an image under editable labels or call that editable reconstruction. Explain any element still rasterized or omitted.
   - For unsupported Bézier paths, clipping, gradients, transparency, rotated/vertical scripts, formulas or dense infographics, make a deliberate visual reconstruction or flag the limitation. Do not silently drop content.
4. Set each page's `reviewed: true` only after reviewing the source and accounting for missing elements. Keep unresolved issues in `warnings` and `reviewNotes`. Write a short `reviewSummary`. Review does not imply that later rendering will be correct.
5. Build a candidate in a compatible environment:
   - `"$CODEX_PRIMARY_RUNTIME_NODE" scripts/build_pptx.mjs work/layout.reviewed.json work/candidate.pptx`
   - Use `--draft` only to inspect unreviewed extraction, never for delivery. The builder emits native objects, previews and a reconstruction report. It intentionally refuses nearly full-slide pictures and unsupported element types.
6. Validate independently:
   - `python scripts/inspect_editability.py work/candidate.pptx --reject-full-slide-images --require-text "expected title" --require-table`
   - Use `--require-chart` when needed. Check actual OOXML types, not just the preview. Finalize using the Presentations skill, including native table/chart slide requirements and exact slide dimensions. A bundled wrapper is available: set `PRESENTATIONS_SKILL_DIR` to that installed skill root, then run `"$CODEX_PRIMARY_RUNTIME_NODE" scripts/finalize_candidate.mjs work/layout.reviewed.json work/candidate.pptx work/output/final.pptx`. Both PPTX paths must be inside the reviewed JSON's directory, and the final path must be new. The wrapper deliberately materializes workbook snapshots for new charts with verified literal data; it does not preserve original spreadsheet formulas. If literal chart data must work across applications, use the finalizer's explicit workbook snapshot option; this does not recover original formulas.
   - Render the final PPTX using an available Office-compatible renderer. Compare every slide against the source at the same dimensions. Inspect text, Japanese glyphs, overflow, cells, connectors, layer order and missing content. Preview similarity and native-object checks prove different things; both are required. Fix and rerender.
7. Deliver the final PPTX. Briefly distinguish what is editable from raster/uncertain content, mention material font substitutions or unavailable target-application tests, and avoid calling synthetic-fixture tests validation on the user's actual file.

## Boundaries and reference material

- Automatic PDF extraction covers text, lines and rectangles; the agent-reviewed step supplies semantic grouping, tables, diagram connections and missing graphics. Image input does not automatically recover shape semantics.
- All pages in a PPTX share a canvas size. Deliberately letterbox/scale mixed page sizes or split them; never stretch without explanation.
- OCR needs adequate resolution, correct language and often per-region segmentation. Read [OCR and fidelity notes](references/ocr-and-fidelity.md) for Japanese, scanned PDFs and difficult layouts.
- Read [sources and licenses](references/sources-and-licenses.md) when choosing a different dependency or redistributing a workflow. No paid service, PyMuPDF or external upload is required by this implementation.

## Maintainer smoke test

Run `python scripts/test_workflow.py` after changing the renderer. It verifies native text/table/chart serialization and deliberate refusal of unreviewed, unsupported, nearly full-slide raster and unverified-chart inputs. It is a synthetic regression check, not validation on a user's document. Also exercise the PDF and image extraction routes and perform source-to-output visual review on representative inputs. For an independent Office render, invoke `soffice` directly to export PDF, then `pdftoppm`; a convenience render script may itself use artifact-tool and is not necessarily an independent Office engine.
