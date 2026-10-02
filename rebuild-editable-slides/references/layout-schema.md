# Reviewed layout schema v1

Coordinates are CSS pixels, top-left origin. PDF points multiply by 96/72. A raster image's pixel dimensions form its default canvas. Normalize all pages deliberately before combining. Element order is paint order; connectors are added last.

```json
{
  "schemaVersion": 1,
  "units": "px",
  "source": "input.pdf",
  "sourceSha256": "actual SHA-256 from extractor",
  "fontMap": {"Helvetica": "Arial"},
  "reviewSummary": "Describe review and material differences",
  "slides": [{
    "page": 1, "width": 960, "height": 540,
    "sourceImage": "page-001.png", "background": "#FFFFFF",
    "reviewed": true, "warnings": [], "reviewNotes": "Checked source",
    "elements": [
      {"id":"title", "type":"text", "x":48,"y":36,"w":860,"h":60,
       "text":"Exact source title", "font":"Arial", "fontSize":36,
       "bold":true,"color":"#152536"},
      {"id":"a", "type":"shape", "geometry":"rect", "x":60,"y":170,"w":240,"h":100,
       "fill":"#E6EFF7", "stroke":"#273E50","strokeWidth":1.5,
       "text":"Editable node", "font":"Arial","fontSize":24,
       "align":"center","verticalAlign":"middle"},
      {"id":"b", "type":"shape", "geometry":"rect", "x":480,"y":170,"w":240,"h":100,
       "fill":"#E6EFF7", "text":"Next node","font":"Arial","fontSize":24},
      {"id":"table", "type":"table", "x":48,"y":330,"w":860,"h":120,
       "values":[["Phase","Status"],["Review","Ready"]],
       "columnWidths":[430,430], "rowHeights":[60,60],
       "font":"Arial","fontSize":22,"padding":10,
       "stroke":"#CCCCCC","strokeWidth":1,
       "cellStyles":[{"row":0,"column":0,"fill":"#152536","color":"#FFFFFF","bold":true}]}
    ],
    "connectors":[{"from":"a","to":"b","kind":"straight","arrow":true,"color":"#273E50","width":2}]
  }]
}
```

## Supported fields

- Every non-line element: `id,type,x,y,w,h`. `w/h` must be positive. Shapes/text accept optional `rotation` degrees, `fill`, `stroke`, `strokeWidth`, `font`, `fontSize` pixels, `bold`, `italic`, `color`, `align`, `verticalAlign`, `padding`, `wrap` boolean. `autoFit` intentionally stays off so overflow is visible.
- `text`: exact `text`, or `runs:[{text,font,fontSize,bold,italic,color}]` for one rich-text paragraph. Use multiple text elements for separately positioned paragraphs. Prefer logical paragraphs over per-character boxes.
- `shape`: `geometry` is an artifact-tool supported preset, e.g. rect, roundRect, ellipse, triangle, rightArrow. Simple native shapes do not recover original SmartArt.
- `line`: `x1,y1,x2,y2,stroke,strokeWidth`; direction and negative slopes are retained.
- `table`: rectangular `values` matrix; optional pixel `columnWidths,rowHeights`; `cellStyles:[{row,column,fill,color,bold}]`; `merges:[{startRow,endRow,startColumn,endColumn}]`. Remove duplicate extracted text/lines under a reconstructed table. Merged cells require visual inspection.
- `chart`: `chartType` (e.g. bar/line/pie), `categories`, `series:[{name,values,fill}]`, `dataVerified:true`, and `dataSource` describing exact source. A nonempty source-backed `title` is currently required because the runtime emits an empty title part for untitled charts, which fails final validation. Optional `hasLegend,barOptions,xAxis,yAxis,dataLabels,legend`. Series lengths must match categories. Chart editability and rendering must be checked; original spreadsheet formulas are not recovered.
- `image`: relative or absolute local `path` to a PNG/JPEG crop and `rasterReason`; no hidden background slide. Files covering over 80% of the canvas are rejected; this is a safety heuristic, not a proof that all content is editable. Do not evade it by splitting screenshots.
- Connectors: `from,to` are shape IDs, optional `kind,fromSide,toSide,color,width,arrow`. Use actual connectors for connected diagrams. Connector stacking is last, so adjust if the source requires otherwise.
- Slide `notes` are optional audience-facing provenance, not private diagnostics. Keep internal review details in the reconstruction report.

The builder does not claim a general JSON Schema validator. Check off-canvas objects, unexpected enums, missing fonts, complex cell styles and source completeness during QA. Failed validation must not be bypassed by simply setting `reviewed:true`.
