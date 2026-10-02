# 日本語スキル10種類の検証記録

実施日: 2026-10-02 UTC

## 対象と方法

各スキルの合成資料を使って実際にレポートを作成し、期待事項と照合しました。入力はすべて架空の教材です。本番環境・個人資料・請求アカウントを使用していません。作成した成果物と検証過程は下表のリンクから確認できます。

| スキル | 代表的な確認内容 | 成果物 |
| --- | --- | --- |
| terraform-change-review | 置換順序、unknownとnull、秘密値の非転載、drift、targetと鮮度 | [レビュー](walkthroughs/terraform-change-review.md) |
| kubernetes-incident-triage | OOMとPendingの区別、UID・採取時刻・endpoint、秘密値の非転載 | [調査結果](walkthroughs/kubernetes-incident-triage.md) |
| observability-gap-review | SLIの母集団、参考burn rate、系列上限、samplingの偏り、欠測 | [監視レビュー](walkthroughs/observability-gap-review.md) |
| cloud-cost-investigation | Decimal計算、130→230 USD、差額100、配列・通貨・残差 | [費用調査](walkthroughs/cloud-cost-investigation.md) |
| incident-timeline-report | 時差・時計補正・夏時間の２候補、矛盾と因果の保留 | [時系列](walkthroughs/incident-timeline-report.md) |
| safe-runbook-authoring | 実施条件・中止基準・復旧手段の不足を安全側へ判断 | [手順書レビュー](walkthroughs/safe-runbook-authoring.md) |
| technical-decision-record | 必須条件による除外、同点、感度変更による逆転 | [意思決定記録](walkthroughs/technical-decision-record.md) |
| architecture-diagram-spec | 宣言・観測・提案の分離、根拠逆引き、Graphviz実描画と目視 | [構成図仕様](walkthroughs/architecture-diagram-spec.md) |
| source-grounded-research-brief | 主張台帳、適用範囲、矛盾・出典の独立性 | [調査結果](walkthroughs/source-grounded-research-brief.md) |
| public-transit-trip-planning | 深夜の運行日・暦日、徒歩・乗換、帰路の切替条件 | [旅程](walkthroughs/public-transit-trip-planning.md) |

## 構造・保全検証

- 10種類すべてにSKILL.md、日本語説明、成果物テンプレート、合成資料、表示メタデータがあります
- 全11種類のSKILL.mdの前書き形式を検証しました。新規本文はすべて500行未満です
- `python scripts/validate_collection.py` で期待するスキル集合、内部リンク、テンプレート、メタデータを検査します
- 新規のPython構造検査スクリプトの構文を確認しました
- 既存の `rebuild-editable-slides/` の全ファイルをGit blob hashで比較し、元の公開版と同一であることを確認しました
- 公開候補の機密情報・内部パスを確認しました。合成テストには明示的な架空秘密値を含みますが、成果物にその値を転載しないことを確認しています

## 検証上の制約

合成ケースによる机上レビューは、実クラスタ・本番監視・クラウドAPI・実際の契約単価・運行状況に対する統合テストではありません。スキルは調査や文書作成の手順であり、対象環境における正しさ、安全性、費用削減、乗換成功を保証しません。

構造検査は文章の意味まで自動判定しません。実行時には各スキルの鮮度確認・不足情報・承認境界に従う必要があります。API仕様・時刻表等は利用の都度、対象の版・日付の一次資料で再確認してください。

構成図はローカルでGraphvizによる描画まで確認しました。Terraform、kubectl、監視設定、課金対象のクエリ、予約・購入・外部通知は実行していません。既存PPTスキルの機能試験は今回再実行していません。CIワークフローは追加していません。
