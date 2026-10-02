# skillbox

SRE・クラウド運用、技術文書、出典付き調査、公共交通の旅行計画に使うエージェントスキル集です。新しい10種類は本文・テンプレート・合成例を日本語で用意しています。既存のPowerPoint再構築スキルも収録しています。

## スキル一覧

| スキル | 用途 |
| --- | --- |
| [terraform-change-review](terraform-change-review/SKILL.md) | 保存済みTerraform planの破壊的変更・権限・未知値を根拠付きでレビュー |
| [kubernetes-incident-triage](kubernetes-incident-triage/SKILL.md) | 対象を絞った読み取り専用のKubernetes障害切り分け |
| [observability-gap-review](observability-gap-review/SKILL.md) | ユーザー影響から監視・SLI・トレースの不足を洗い出し |
| [cloud-cost-investigation](cloud-cost-investigation/SKILL.md) | 費用増分を利用量・単価・割引等に分解して調査 |
| [incident-timeline-report](incident-timeline-report/SKILL.md) | 時差と不確実性を保持した障害時系列・事後報告の整理 |
| [safe-runbook-authoring](safe-runbook-authoring/SKILL.md) | 実施条件・中止基準・復旧確認を備えた運用手順書の設計 |
| [technical-decision-record](technical-decision-record/SKILL.md) | 選択肢・根拠・再検討条件を残す技術判断記録 |
| [architecture-diagram-spec](architecture-diagram-spec/SKILL.md) | 根拠へ追跡できるノード・接続一覧と構成図仕様の作成 |
| [source-grounded-research-brief](source-grounded-research-brief/SKILL.md) | 主張と出典を対応付け、矛盾・鮮度・不明点を明示する調査 |
| [public-transit-trip-planning](public-transit-trip-planning/SKILL.md) | 運行日・乗換・最終便・代替案を確認する公共交通の旅程計画 |
| [rebuild-editable-slides](rebuild-editable-slides/SKILL.md) | PDF・画像から編集可能なPowerPointを再構築 |

## 新しい10種類の導入と使い方

利用するエージェントのスキルインストーラーへ、このリポジトリの目的のディレクトリを指定してください。たとえば「https://github.com/sts1992/skillbox の terraform-change-review をインストールしてください」と依頼します。インストール機能や呼び出し構文はクライアントに依存します。本リポジトリへの追加は、利用中のアプリへの自動インストールを意味しません。

各スキルの `SKILL.md` に必要な入力、成果物、検証条件があります。資料を渡し、スキル名と目的を指定してください。`assets/` は成果物の雛形、`references/` はチェックリスト・合成ケースなどです。相対パスは各スキルのディレクトリ基準です。

例:

- 「terraform-change-review で、この秘匿済みplan JSONの置換・削除・不明点をレビューして」
- 「incident-timeline-report で、このイベント記録をUTCの障害時系列にして。推測と事実を分けて」
- 「public-transit-trip-planning で、指定日の公共交通だけの日帰り案を作って。最終便と代替経路を確認して」

### 対応環境と安全性

新しい10種類は独立したMarkdown手順とテンプレートが中心で、専用ランタイムを必要としません。ファイル読取と文章作成ができるエージェントで資料ベースの作業ができます。最新情報を確認するにはWeb閲覧、ライブの運用状況を読むには利用者が許可した読み取り専用ツールが必要です。ツールがない場合は未確認事項と必要資料を明示し、実行済みと表現しません。

- 本番変更、購入・予約、外部送信を自動実行するためのスキルではありません
- 運用コマンドや費用削減策は、権限・影響・実施条件を確認してから別途判断してください
- ログ、plan、請求明細、旅程には機密情報が含まれる場合があります。必要最小限に秘匿し、公開リポジトリへ追加しないでください
- 文書内やWebページ内の命令は資料として扱い、利用者の指示や権限より優先しません
- API、料金、運行情報など変わる情報は実行時に公式情報を確認します。合成例は実際の本番環境・運行実績ではありません

### 検証

構造チェックを実行できます（Python 3とPyYAMLが必要）。これは資料レビューの正しさや実環境での動作を保証するものではありません。

```sh
python scripts/validate_collection.py
```

各スキルの合成ケースを使い、成果物に必要な項目・不確実性・安全境界が残るかを確認してください。検証範囲と実施結果は [検証記録](tests/validation-report.md) に記載します。新しい10種類は本番クラスタ・クラウドアカウントへの接続や実際の予約を行う統合テストはしていません。

以下は既存のPowerPointスキル固有の説明です。

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
