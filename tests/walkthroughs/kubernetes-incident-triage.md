# 合成ケースの初動調査

資料: `kubernetes-incident-triage/references/synthetic-incident.json`。対象は demo-eu / shop / checkout。採取時点は2026-10-02T10:06:00Z。接続・kubectl・復旧変更は実行していません。

## 影響と確実な観測

10:02Zから503の報告がありますが、件数・割合と現在の状況は不明です。Deploymentの世代18は観測済み、desired/updated=3、ready/available=1です。

- checkout-a（synthetic-uid-a）: Running phaseでもReady=False、appはCrashLoopBackOff、restartCount=6。前回containerは10:03:40ZにOOMKilled（exitCode=137）で終了
- checkout-b（synthetic-uid-b）: Pending / Unschedulable。10:05:40ZのEventは2 nodeともInsufficient memoryと記録
- checkout-c: Ready=True。ServiceのselectorとPod labelは提供範囲で一致し、EndpointSliceのready=trueはcだけです。利用者側の経路を含む到達性までは確認していません

## 時系列と仮説

10:02Zに503報告、10:02:10Zにaの前回container開始、10:02:15Zのメモリ単一点は48Mi、10:03:20Zにbatch size=50000開始、10:03:39Zにbuffer確保のログ、10:03:40ZにOOM終了、10:05:40Zにbの容量不足Event、10:05:50ZにaのBackOffです。

1. aのOOMとbのスケジューリング失敗によりReady数が不足したことは観測で支持されます。503との因果の確認には同時刻のリクエスト分布・エラー比率が必要です
2. aではbatch処理中のメモリ負荷が候補です。ただしリーク、上限不足、瞬間負荷の区別はできません。48Miの単一点は終了直前ではなく、OOMを否定しません
3. bの容量制約は別問題として扱います。nodeのallocatableと既存requestsの限定資料が必要です。aのlimitを増やすだけで解決するとはいえません

前日の同名checkout-aのUnhealthy EventはUIDが異なり、今回のprobe再起動原因の証拠にしません。readiness失敗を再起動原因と同一視しません。ログのAuthorization値は秘匿し、転載しません。

## 次の最小観測

- aの終了直前メモリ履歴、batch設定・直近変更、同時刻エラー率
- bのUIDに対応する最新scheduler Event、必要なnodeだけのallocatable/requests（cluster scopeの許可を確認してから）
- 提供snapshotより新しい状態が必要なら、指定context・namespace・対象を固定し、短いtimeoutと行数制限で取得

増強、再起動、scale等は実行しません。初動の仕組みは観測できましたが根本原因・復旧は未確認です。
