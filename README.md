# skillbox

PDF・スクリーンショット・スライド画像から、編集可能なPowerPointを再構築するスキル集です。

## rebuild-editable-slides

[スキル本体](rebuild-editable-slides/SKILL.md) | [中間レイアウト仕様](rebuild-editable-slides/references/layout-schema.md)

文字、図形、接続線、表、確認済みの数値に基づくグラフをPowerPointのネイティブオブジェクトにします。抽出結果をエージェントが目視で確認・補完する方式で、ワンクリックの完全復元ではありません。写真や複雑なイラストは画像として残る場合があります。

### 対応環境と依存関係

- 抽出: Python 3、pdfplumber、Pillow、Popplerの `pdftoppm`
- OCRを使う場合: Tesseract CLIと言語モデル。日本語は `jpn`、必要に応じて `eng` / `jpn_vert`
- PPTX生成: `@oai/artifact-tool` を提供する対応Codexランタイム
- 最終検証ラッパー: 対応環境のPresentationsスキルとそのヘルパー
- 最終表示確認: PowerPointまたはLibreOfficeなどのOffice互換レンダラー

重要: このリポジトリはCodexの専用ランタイムやPresentationsヘルパーを同梱しません。通常のNode.js環境へコピーするだけではPPTX生成は動きません。抽出・OOXML検査用Pythonスクリプトは、それぞれの依存関係があれば単独で利用できます。

### 導入

対応するエージェントのスキルインストーラーに、このリポジトリの `rebuild-editable-slides` ディレクトリを指定してください。GitHubからスキルを導入できるインストーラーでは、次のように依頼できます。

> https://github.com/sts1992/skillbox の rebuild-editable-slides をインストールしてください。

インストール先や対応機能は利用するクライアントに従ってください。スキルの導入だけでは専用ランタイムは追加されません。既存の同名スキルを上書きする前に内容を確認してください。

### 使い方

PDFまたは画像を添付し、例えば次のように依頼します。

> rebuild-editable-slides を使って、このPDFを文字・図形・表が編集できるPowerPointにしてください。画像として残る箇所と不確かな箇所も教えてください。

スクリプトの相対パスはスキルディレクトリを基準にします。

```sh
cd rebuild-editable-slides
python scripts/extract_layout.py input.pdf work/extracted --pages 1,2
# 各ページの画像と抽出結果を確認し、work/layout.reviewed.json を作成
# reviewed:true は確認後にのみ設定
"$CODEX_PRIMARY_RUNTIME_NODE" scripts/build_pptx.mjs work/layout.reviewed.json work/candidate.pptx
python scripts/inspect_editability.py work/candidate.pptx --reject-full-slide-images
```

最終化の設定・コマンドと全手順は [SKILL.md](rebuild-editable-slides/SKILL.md) を参照してください。最終PPTXは必ず描画し、元資料と比較します。

### テスト

専用ランタイムがある環境で実行します。

```sh
python rebuild-editable-slides/scripts/test_workflow.py
```

合成データでネイティブの文字・表・グラフ、表罫線、未確認レイアウト・未対応要素・全面画像・未検証グラフの拒否を検査します。ユーザー資料の精度やPowerPoint本体の操作を保証するテストではありません。

### 制約とプライバシー

- OCR、読み順、フォント、文字の折り返し、複雑な図形には確認・調整が必要です
- 元データ不明のグラフから正確な数値や数式は復元しません
- ソース資料や生成物をこの公開リポジトリへコミットしないでください。抽出JSON・検証レポートにも元資料の文字やローカルパスが含まれます
- 外部OCR・変換サービスへの自動アップロードは行いません
- [依存関係とライセンスの参照](rebuild-editable-slides/references/sources-and-licenses.md)。リポジトリ独自のライセンスは未指定です
