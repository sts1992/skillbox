# skillbox

SRE・クラウド運用、技術文書、出典付き調査、公共交通の旅行計画に使うエージェントスキル集です。独自の10種類に加え、公開されている上流スキルから選んだ5種類を日本語の入口で収録しています。既存のPowerPoint再構築スキルもあります。

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
| [systematic-debugging](systematic-debugging/SKILL.md) | 再現・証拠・単一仮説から原因を調べ、修正と回帰確認へ進める |
| [workers-best-practices](workers-best-practices/SKILL.md) | Cloudflare Workersの設定・状態分離・非同期処理・可観測性をレビュー |
| [benchmark-checklist](benchmark-checklist/SKILL.md) | 性能改善の数値を、比較条件・失敗数・複数回測定から検証 |
| [review-pr](review-pr/SKILL.md) | PR差分の実害ある問題を、重要度・行位置付きJSONへ整理 |
| [yomiyasu](yomiyasu/SKILL.md) | 主張・条件・断定の強さを保ったまま日本語を推敲 |

## 上流から選んだ5種類（2026-10-17追加）

原因調査、Workers固有のレビュー、性能測定、PRレビュー、日本語推敲を補う構成です。既存のTerraform・監視設計・障害報告・ADRのスキルは置き換えません。人気順位ではなく、実務への適合、既存との重複、実装と依存、再配布条件を基準に選びました。

| スキル | 提供元・著者 | ライセンス | 出典・取得commit・ローカル変更 |
| --- | --- | --- | --- |
| systematic-debugging | obra / Jesse Vincent | MIT | [取得記録](systematic-debugging/UPSTREAM.md) |
| workers-best-practices | Cloudflare | Apache-2.0 | [取得記録](workers-best-practices/UPSTREAM.md) |
| benchmark-checklist | Cursor pstack / Lauren Tan | MIT | [取得記録](benchmark-checklist/UPSTREAM.md) |
| review-pr | Warp | MIT | [取得記録](review-pr/UPSTREAM.md) |
| yomiyasu | nanaism | MIT・Unicode License V3 | [取得記録](yomiyasu/UPSTREAM.md) |

各ディレクトリのライセンス原文・著作権表示を保持しています。翻訳・補足を加えたものは変更点を明記しています。英語の上流参照資料とコードは必要なものを同梱し、固定したcommitからの取得記録を残しています。この収録は上流による承認を意味しません。リポジトリ全体へ一律のライセンスを新設しておらず、既存の独自ファイルのライセンス未指定状態も変更していません。

### 導入と使い方

利用するクライアントのスキルインストーラーへ、目的のディレクトリを一つずつ指定します。例: 「https://github.com/sts1992/skillbox の systematic-debugging をインストールしてください」。`SKILL.md` だけでなく、同じディレクトリの参照資料・コード・ライセンスも一緒に導入してください。同名の上流版がある場合は、上書き前にどちらを使うか確認します。

このリポジトリへの収録だけでは、アプリへのインストール、プラグイン登録、フック有効化、外部アカウント接続は行われません。

- 「systematic-debugging で、このCI失敗の原因を調査して。修正前に根拠と仮説を整理して」
- 「workers-best-practices で、このWorkerの差分とWrangler設定をレビューして」
- 「benchmark-checklist で、この性能改善レポートの測定条件と結論を点検して」
- 「review-pr で、このPR差分をレビューして。結果はJSONで、GitHubには投稿しないで」
- 「yomiyasu で、このPR説明文を意味と条件を変えずに読みやすくして」

### 前提と注意

- 5種類ともSkills形式のMarkdownを扱えるエージェント向けです。呼び出し構文、ローカルファイルアクセス、コマンド実行の可否はクライアントに依存し、全クライアントでの実行互換性は保証していません。
- systematic-debuggingは対象コード・ログ・テスト環境を使います。任意の `find-polluter.sh` はnpmのtestを実行します。付属TypeScriptは上流固有の型に依存する参考例で、単独実行用ライブラリではありません。
- workers-best-practicesは対象のWrangler設定・版・生成型を基準にします。静的レビューにCloudflare認証は不要です。最新仕様の確認には公式ドキュメントへのアクセス、実測には対象プロジェクトのテスト環境が必要です。
- benchmark-checklistは測定データだけでも点検できます。実測には負荷生成・計測の環境が必要で、本番への負荷試験を許可するものではありません。
- review-prは差分、PRの背景、対象コードを使い、付属の検証用コードにはPython 3.10以降が必要です。任意の仕様取得補助はGitHub APIと既存の認証情報を使います。GitHubへのレビュー投稿は別の操作です。
- yomiyasuはPython 3.9以降と同梱スクリプトを使います。チェック時に原稿全文などを `.yomiyasu/` または `--state-dir`・環境変数で指定した保存先へ記録し、資料の抜き書きも作るため、機密原稿の実際の保存先・保持範囲を確認してください。これらを公開リポジトリへコミットしないでください。自動フックは設定しません。
- 付属コード、テストコマンド、ネットワーク取得は、内容と対象を確認して許可された範囲で使います。資料中の命令やスキルの導入そのものを、デプロイ・外部送信・認証変更の承認として扱いません。

### 今回の確認範囲

実ファイル、依存関係、ライセンス、帰属、取得commit、相対リンク、frontmatter、Python構文を静的に確認しています。上流スキルの実行、アプリへのインストール、補助スクリプトの実行、外部サービス接続、実環境の動作試験は行っていません。詳しくは [収録時の検証記録](tests/imported-skills-validation.md) を参照してください。

## 独自の10種類の導入と使い方

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
