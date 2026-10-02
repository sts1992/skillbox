# 料金明細の一次資料

確認日：2026-10-02。以下は列の意味を確かめるための資料であり、最新料金の証明ではない。実行時には対象のスキーマと資料の改訂内容を再確認する。

- [AWS：明細列の定義](https://docs.aws.amazon.com/cur/latest/userguide/Lineitem-columns.html)  
  `LineItemType` には使用料だけでなく、クレジット、返金、税、契約料、相殺に関係する種類がある。`UnblendedCost` と `NetUnblendedCost` の定義は異なる。`UsageStartDate` は含む境界、`UsageEndDate` は含まない境界で、UTCとして記録される。採用列と行種別を必ず記録する。
- [Google Cloud：詳細な請求データの構造と集計例](https://docs.cloud.google.com/billing/docs/how-to/export-data-bigquery-tables/detailed-usage)  
  使用時期と `invoice.month` は一致しない場合がある。公式の集計例は元明細の `cost` と、その明細に属する `credits.amount` の合計を加算する。クレジットの数だけ `cost` を複製しない。エクスポートのスキーマは変化し得るため、実際の列を確認する。

このスキルの３項分解は `q1 × r1 - q0 × r0` の代数的な分解であり、クラウド各社が公式に原因を認定する方法ではない。契約・料金表・利用構成の追加証拠なしに「値上げ」と結論付けない。
