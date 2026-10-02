# 公式資料

確認日: 2026-10-02。実行時はクラスタと kubectl のバージョンに合わせて再確認する。

- [稼働中の Pod の調査](https://kubernetes.io/docs/tasks/debug/debug-application/debug-running-pod/): container 状態、Event、前回 container のログを使う切り分けを確認する。ページ中の変更操作は本スキルの範囲外。
- [kubectl logs](https://kubernetes.io/docs/reference/kubectl/generated/kubectl_logs/): container の指定、previous、since、tail、limit-bytes、timestamps の flags を確認する。
- [Probe の役割](https://kubernetes.io/docs/concepts/workloads/pods/probes/): startup、liveness、readiness を区別する。readiness の失敗だけを再起動の根拠にしない。
- [Service の調査](https://kubernetes.io/docs/tasks/debug/debug-application/debug-service/): selector、ports、EndpointSlice による経路確認の観点を確認する。exec やテスト用 Pod 作成を自動的に実行しない。

本スキルの採取件数・ログサイズ上限は保守的な調査方針であり、Kubernetes 自体の上限ではない。
