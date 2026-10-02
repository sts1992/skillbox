# Kubernetesを扱う際の一次資料

確認日：2026-10-02。以下は一般的な注意点の根拠。実際の手順書では対象のKubernetesとkubectlの版を特定し、その版の資料で再確認する。ここにある説明を他の製品へ流用しない。

- [Kubernetes API：非変更の検証](https://kubernetes.io/docs/reference/using-api/api-concepts/#dry-run)  
  `dry-run` 要求は永続化前までの段階を検証する。認可は通常の要求と同じである。副作用を伴う入場制御がある場合などは失敗し得る。エラーを本実行に切り替えて回避しない。
- [kubectl applyの仕様](https://kubernetes.io/docs/reference/kubectl/generated/kubectl_apply/)  
  `--dry-run=client` と `--dry-run=server` を区別する。後者はサーバーへ要求を送るが、リソースを永続化しない。出力できたことはアプリの実稼働成功を示さない。
- [Deploymentの更新と切戻し](https://kubernetes.io/docs/concepts/workloads/controllers/deployment/#rolling-back-a-deployment)  
  DeploymentのリビジョンはPodテンプレートの変更に関係する。旧リビジョンへの切戻しが戻すのはPodテンプレート部分であり、外部DBや別オブジェクトまで一括復元するものではない。
- [kubectl rollout statusの仕様](https://kubernetes.io/docs/reference/kubectl/generated/kubectl_rollout/kubectl_rollout_status/)  
  既定では最新の展開を監視し、途中で新しい展開が始まると追跡対象が変わり得る。`--revision` による固定と `--timeout` による待機上限を検討する。待機終了と変更の取消は別である。

## 文書に示せる観測コマンドの形

以下は手順の表記例であり、このスキルで実行する命令ではない。値と対象版を確認するまで実行用として配布しない。

```sh
kubectl --context="$CONTEXT" --namespace="$NAMESPACE" \
  rollout status "deployment/$DEPLOYMENT" \
  --revision="$EXPECTED_REVISION" --timeout=180s
```

`180s` は例示値であり、実際の待機上限として自動採用しない。期待リビジョンを現在値＋１と決め付けず、対象変更と結び付いた確認済みの値を使う。この観測だけでは、利用者向け指標や永続データの整合性を確認できない。
