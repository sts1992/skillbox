# 公式資料と使用上の注意

確認日: 2026-10-02。各製品の最新版を対象環境へそのまま当てはめず、SDK・collector・backend の組合せとバージョンを確認する。

- [Google SRE: SLO の実装](https://sre.google/workbook/implementing-slos/): 利用者の結果を表す仕様と測定の実装を分け、good / total、目標、予算を検討する。教材の数値をサービスの正式目標にしない。
- [Prometheus: 計測の実践](https://prometheus.io/docs/practices/instrumentation/): label の組合せが系列を増やす性質を確認する。サイト上の経験則を普遍的な容量保証に変えない。
- [Prometheus: histogram と summary](https://prometheus.io/docs/practices/histograms/): 分位点の集計、bucket の設計、classic と native の違いを確認する。native の導入は互換性を調べてから提案する。
- [Prometheus: query 関数](https://prometheus.io/docs/prometheus/latest/querying/functions/): counter の rate を集計より先に行うこと、histogram 集計と補間の前提を確認する。
- [OpenTelemetry: sampling](https://opentelemetry.io/docs/concepts/sampling/): head と tail の判断時点と制約を確認する。上流で除外された trace や伝送時の損失を、tail 方針だけで補えるとはしない。

ここで使う上限見積り、優先度、受け入れ試験はレビューの設計であり、ベンダーの性能保証ではない。
