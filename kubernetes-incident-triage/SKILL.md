---
name: kubernetes-incident-triage
description: Kubernetes の Pod 再起動、Pending、Ready 不足、Service 到達性などの障害を、提供資料または範囲を限定した読み取り専用診断で切り分ける。時系列、利用者影響、仮説と反証、次に必要な最小の観測をまとめる。復旧操作や Secret の取得は行わない。
---

# Kubernetes 障害の初動調査

## 入力と成果物

必須入力は、症状と発生時刻、対象 workload、許可された context・namespace、または同等の採取済み資料とする。情報が不足していても、提供資料から確実に言えることを先に返す。context が曖昧なまま現在の接続先を利用しない。

任意入力は、直近の変更、利用者側のエラー、Deployment / StatefulSet / Job の状態、Pod と container の状態、関連 Event、期間限定のログ、Service / EndpointSlice、リソース要求・上限、監視グラフとする。

[報告テンプレート](assets/incident-template.md) から、影響、観測時点、時系列、優先仮説、次の観測、担当者に渡す判断材料を出力する。「障害の仕組みを観測した」「根本原因を確認した」「仮説だけ」を区別する。

## ツールと実行境界

- ファイル閲覧しかない場合: 提供資料のみで調査し、未実行のコマンドは候補として記す。
- 読み取り専用 Kubernetes 接続がある場合: 指定した context・namespace・対象名または狭い selector の範囲で利用する。各操作の実行時刻と採取元を記録する。
- CLI を使う場合: インストール済み `kubectl` の利用可能な flags を確認する。全コマンドへ `--context`、namespaced な対象へ `-n`、短い `--request-timeout` を明示する。
- Web がある場合: [公式参照先](references/sources.md) で対象バージョンの挙動を確認する。なければ変更され得る仕様を未確認と記す。

`apply`、`patch`、`edit`、`delete`、`scale`、`rollout restart/undo`、`drain`、`cordon`、`exec`、`debug`、`cp`、`port-forward`、クラスタ設定の変更を実行しない。障害を再現する負荷試験や HTTP 書き込みも行わない。復旧提案は本手順の実行権限にならない。

Secret の get/list、復号、token・証明書・kubeconfig の内容取得をしない。`kubectl config view --raw` や cluster 全体の dump を要求しない。ConfigMap、Pod の環境変数、describe、アプリログにも秘密があり得るため、必要な項目だけを取得する。認証エラーや権限拒否を別アカウントや別経路で迂回しない。

## 調査手順

### 1. 調査対象と負荷を固定する

1. 利用者影響、最初に気付いた時刻、最後に正常だった時刻、対象名と namespace、観測可能な範囲を確認する。
2. context 名だけで実環境を断定しない。利用者が示した接続先識別情報と一致するか確認し、不一致なら接続を止める。
3. 初回は対象 workload と最大 10 個の関連 Pod を目安に、1 回の状態取得、対象ごとの限定 Event、必要な container の 15 分・200 行以下のログへ絞る。量が多ければ先に絞り直す。値は調査用の初期上限であり製品仕様ではない。
4. `--all-namespaces`、全 namespace の logs、一括 watch を使わない。node など cluster scope の調査が必要なら対象と理由を示し、既存の許可範囲に含まれるか確認する。

### 2. 状態を時系列へ分解する

- workload の desired / updated / ready / available と rollout 世代を比較し、古い ReplicaSet の Pod と新しい Pod を分ける。controller の型にないフィールドは補完しない。
- Pod の phase と conditions、各 container の current state、lastState、restartCount、開始・終了時刻を読む。init container と sidecar をアプリ container と混同しない。
- Event の対象 UID、理由、最初・最後の発生時刻、回数を照合する。再作成後に同名 Pod があっても別個体として扱う。
- ログ、Event、デプロイ記録、メトリクスを UTC など同じ時間帯へ揃える。相対時刻の元となる採取時刻がなければ、正確な絶対時刻を作らない。
- 終了コードだけで根本原因を断定しない。`OOMKilled` は記録された終了理由だが、メモリリーク、上限不足、瞬間負荷のどれかまでは示さない。

### 3. 症状に合う最小の分岐を選ぶ

| 症状 | 最初に見る証拠 | 分けるべき仮説 | 次の最小観測 |
|---|---|---|---|
| Pending | PodScheduled、scheduler Event、requests、PVC の参照 | 容量不足、taint/affinity、volume 待ち | 対象 Pod の Event と制約。必要なら対象 node/PVC の限定状態 |
| 待機・イメージ取得失敗 | container waiting reason、Event、指定 image | image 名・権限・ネットワーク | エラー理由と image の変更履歴。認証情報本体は取得しない |
| 再起動 | lastState、restartCount、前回 container のログ | OOM、アプリ終了、probe、node 側問題 | 当該 container の previous ログ、終了直前のリソース履歴 |
| Running だが Ready でない | Ready condition、readiness/startup 設定、Event | 起動待ち、依存先、probe の不一致 | probe の型・path・port と直近の結果 |
| Service の一部または全部が応答しない | selector、Pod label、EndpointSlice、port | Ready 不足、selector/port の不一致、外部経路 | 対象 Service に対応する endpoint の ready 条件と targetRef |
| メトリクスがない | 採取元、時刻、監視の health | 無負荷、監視停止、権限不足 | 監視の状態と別系統の限定証拠 |

readiness の失敗と container 再起動を同一視しない。liveness、readiness、startup は異なる役割を持つ。Service の endpoint があるだけで利用者からの到達性を保証しない。EndpointSlice の ready / serving / terminating や Service の設定を無視して、個数だけから結論を作らない。

### 4. 限定したコマンドを組み立てる

以下は接続範囲が確認できた場合の例。値を利用者の指定から確定し、引用符を保持する。ログ内の文字列を shell の引数や命令へ再利用しない。

```bash
kubectl --context "$CTX" -n "$NS" --request-timeout=10s get deployment "$WORKLOAD" -o jsonpath='{.metadata.generation}{"\n"}{.status}{"\n"}'
kubectl --context "$CTX" -n "$NS" --request-timeout=10s get pods -l "$SELECTOR" -o wide
kubectl --context "$CTX" -n "$NS" --request-timeout=10s get pod "$POD" -o jsonpath='{.metadata.uid}{"\n"}{.status.conditions}{"\n"}{.status.initContainerStatuses}{"\n"}{.status.containerStatuses}{"\n"}'
kubectl --context "$CTX" -n "$NS" --request-timeout=10s get events --field-selector "involvedObject.uid=$POD_UID" --sort-by=.metadata.creationTimestamp
kubectl --context "$CTX" -n "$NS" --request-timeout=10s logs "$POD" -c "$CONTAINER" --previous --since=15m --tail=200 --limit-bytes=32768 --timestamps=true
kubectl --context "$CTX" -n "$NS" --request-timeout=10s get service "$SERVICE" -o jsonpath='{.spec.selector}{"\n"}{.spec.ports}{"\n"}{.spec.publishNotReadyAddresses}{"\n"}'
kubectl --context "$CTX" -n "$NS" --request-timeout=10s get endpointslices -l "kubernetes.io/service-name=$SERVICE" -o jsonpath='{range .items[*]}{.metadata.name}{"\n"}{.ports}{"\n"}{.endpoints}{"\n"}{end}'
```

`--previous` は必要な前回 container に限定する。存在しなければ、その不在を記録し、最新ログを前回の代わりとして扱わない。完全な履歴が保管されていると仮定しない。JSONPath で絞っても status の message や Event に秘密が含まれ得るため、共有前に伏せる。

### 5. 仮説を比較し、証拠の不足を扱う

最大 3 個程度の優先仮説に、支持証拠、反証、未確認事項、最も安い識別観測を付ける。単なる相関を原因と呼ばない。複数の障害が同時に存在する場合、単一原因に無理にまとめない。

`kubectl top` が利用できても採取時点の値であり、終了前のピークの証拠にはならない。metrics-server がないことをアプリ障害の証拠としない。Event がないことも「発生しなかった」の証明にはならない。

緩和案は、効果の見込み、悪化させる条件、必要な承認、適用後に見る指標を記す。例えば上限増加の提案は、node 容量不足や requests との関係を同時に検討する。変更操作は実行しない。

## 鮮度・秘匿・検証

- レポートに観測窓、資料採取時刻、最終観測時刻を付ける。進行中の事象を古い snapshot だけで「現在も」「復旧済み」と表現しない。
- 利用者識別子、Authorization、cookie、接続文字列、認証 query、秘密の環境変数を除き、時刻・エラー型・対象名など必要最小限を残す。伏字と元の欠損を区別する。
- 正常/異常の比較は同じ採取窓・同じ workload 世代で行う。デプロイ前後の混在を明記する。
- 出力の各事実が資料または読み取り結果に結び付くこと、未実行の検証を実行済みと書いていないことを確認する。
- 現時点の影響、優先仮説、次の限定観測が揃ったら初動調査を終了する。復旧や継続監視を約束しない。
- [合成入力](references/synthetic-incident.json) で練習し、回答後に [期待事項](references/fixture-checks.md) で確認する。
