---
name: workers-best-practices
description: Cloudflare Workers の実装・設定・コードレビューを、本番利用を見据えて確認する。互換日付、bindings と生成型、ストリーミング、非同期処理の寿命、ランタイムの状態分離、ログとトレースを扱う。一般的な監視設計や Kubernetes の障害調査ではなく、Workers 固有の変更に使う。
---

# Cloudflare Workers 実装・レビュー

変更表示: Cloudflare の `workers-best-practices` を日本語化し、単独で使える手順・検証結果の形式・実行境界を追加した版。出典、固定コミット、変更点は [UPSTREAM.md](UPSTREAM.md)、ライセンスは [LICENSE](LICENSE) を参照。

## 最初に基準を固定する

Workers の API、型、設定、制限について、記憶より取得した根拠を優先する。対象プロジェクトのロックファイル、インストール済み Wrangler、生成型、`compatibility_date` と flags を基準にする。新しい型パッケージがあるだけでは、既存デプロイの互換性が変わったとは判断しない。

1. 対象 Worker、変更目的、対象環境、対象コミットまたは差分を確認する。
2. `wrangler.jsonc` / `wrangler.json` / `wrangler.toml`、環境別 override、エントリポイント、生成型、関連テスト、既存チェック用コマンドを読む。
3. 設定項目は対象プロジェクトの `node_modules/wrangler/config-schema.json` と照合する。型と schema がなければ取得済みの版情報で調べ、確認できない点を残す。
4. 今回の変更に関係する次の資料だけを読む。小さい修正を全体監査に拡大しない。

| 資料 | 読む場面 |
| --- | --- |
| [設定と可観測性](references/configuration.md) | 互換日付、bindings、生成型、秘密値、ログとトレース |
| [ランタイムのパターン](references/runtime-patterns.md) | ストリーム、Promise の寿命、状態分離、サービス連携、セキュリティ、テスト |
| [プラットフォーム API](references/platform-apis.md) | handler とクラスの型、binding の参照、シリアライズ |

同梱資料は固定コミットの英語原文で、現時点の仕様を保証しない。料金・CPU/メモリ制限・`waitUntil` の時間・Zod の推奨版・テストツールの挙動・「zero-cost」などの記述は、そのまま事実として報告せず、対象プラン、インストール版、互換設定と公式資料で確認する。`nodejs_compat` はコードや依存が必要とする場合に確認し、全プロジェクトへ無条件に追加しない。

不足する根拠は [Workers best practices](https://developers.cloudflare.com/workers/best-practices/workers-best-practices/index.md) または [Cloudflare ドキュメント一覧](https://developers.cloudflare.com/directory/index.md) から対象製品の資料を探す。ネットワークが使えなければ静的レビューを進め、未確認を明示する。

## 設定と bindings

- 新規 Worker の `compatibility_date` は作成日の実日付を使う。既存 Worker は設定されている `compatibility_date` と flags を基準に評価し、更新提案と欠陥を区別する。更新する場合は間の互換性変更を読み、影響するテストを実行する。
- Node.js 組み込み API を使う場合、必要な `nodejs_compat` と日付の条件を確認する。テスト側の自動設定だけで本番の互換性を保証しない。
- bindings を重複定義する手書き `Env` を避け、プロジェクトの Wrangler による `wrangler types` を利用する。追加・改名後は再生成の要否を確認する。既存の `Env` 拡張まで機械的に削除しない。
- `env.X` と設定上の binding 名を大文字小文字まで照合する。Durable Object の export 名、`class_name`、新規クラスの migration も対象 schema で確認する。未使用 binding だけでは欠陥にしない。
- 秘密値をソースや `vars` に置かず、Wrangler secrets など既存の秘密管理方式を使う。ローカルの `.env` / `.dev.vars` と類似ファイルがコミットされないことを確認する。検出した秘密値を報告へ転載しない。
- 新規設定は原則 `wrangler.jsonc` を選ぶ。既存 TOML の移行は変更目的、必要機能、対象 Wrangler の対応を確認してから判断する。

## ログとトレース

新規作成や本番準備では Workers Logs と Traces の有効化を確認する。`observability.enabled` だけでは traces の有効化にならないため、対象 schema と既定値を確認し、通常は `observability.traces.enabled` も明示する。

- 環境別 override を含め、対象デプロイで logs / traces が無効になっていないか見る。
- 検索可能な構造化 JSON を出力し、エラーは `console.error` へ送る。
- sampling はトラフィック、調査目的、費用、データ保持に合わせる。参考例の値を無条件にコピーしない。
- トークン、Cookie、秘密値、不要な個人情報をログや trace に残さない。
- 既存コードのレビューなら不足と影響を指摘する。リモートのログ設定を勝手に変更しない。

## ランタイムの確認

### 入出力と非同期処理

- 大きい、または上限不明の body は `response.body`、`TransformStream` などでストリーム処理する。サイズが既知で小さい JSON まで一律に禁止しない。
- Promise を `await`、`return`、または適切な `ctx.waitUntil()` につなぎ、結果・例外・終了条件を追う。`const { waitUntil } = ctx` のように receiver を失う呼び出しを避ける。
- レスポンス後の短い処理は `waitUntil` の用途と上限を確認する。耐久性や長い再試行が必要なら Queues / Workflows を検討し、単にすべてを `waitUntil` に移さない。
- モジュールの可変変数にリクエスト固有データや I/O を保持しない。isolate の再利用を考慮し、リクエストの状態は引数などで渡す。
- 同期 CPU 処理、大量 JSON、暗号処理の制限を現在のプラン・設定で確認する。根拠なく定数の上限や性能改善幅を主張しない。

### サービス連携

- 同等の操作が binding で可能なら、Cloudflare REST API とトークンを使う設計より binding を優先する。管理 API にしかない操作まで置換しない。
- Worker 間通信は service binding / RPC を検討する。公開 URL が意図的な外部契約なら、その理由と制約を確認する。
- Queues の重複配送と再試行、Workflows の段階的な永続実行を処理の性質に合わせる。副作用を重複実行してよいとは見なさない。
- 外部データベースでは Hyperdrive の対応、既存の接続方式、pooling を確認する。例の接続コードをそのまま採用せず、成功・例外時の接続終了もレビューする。

### セキュリティとエラー

- 秘密トークンの生成に `Math.random()` を使わない。用途に合う `crypto.randomUUID()` / `crypto.getRandomValues()` を使う。
- 秘密値比較は対象 Workers API の対応を確認し、一定長へハッシュ化した値の `crypto.subtle.timingSafeEqual()` など適切な手法を使う。長さによる早期 return や単純な文字列比較を避ける。
- `passThroughOnException()` を一般的な例外処理として使わない。意図的な fail-open なら影響を明示し、通常は明示的な例外処理、構造化ログ、内部情報を漏らさないエラーレスポンスを使う。

## API と型の確認

| 確認対象 | 着眼点 |
| --- | --- |
| binding 型 | `any` で隠さない。namespace、Queue、RPC 等の必要な generic 引数は対象の型定義で確かめる |
| handler | `fetch`、`scheduled`、`queue`、`email` の引数・戻り値が対象の契約に合う。`ctx.waitUntil` を使うなら context を受け取る |
| platform class | 対応する base class を `extends` する。`implements` は runtime behavior、`this.ctx`、`this.env` を継承しない |
| binding アクセス | module handler は引数の `env.X`、platform class は `this.env.X` |
| import / 旧 API | `cloudflare:workers` などの import、constructor、プロパティの改名を対象型と照合する |
| 型の強制 | `as unknown as T` で不整合を隠さず、元の契約を修正する |
| シリアライズ境界 | Queue の `contentType`、Workflow step、DO KV、DO SQL、WebSocket ごとに確認する |

`Map` / `Set` / `Date` を一律に禁止しない。structured clone、JSON、SQL parameter、WebSocket の送信値は別の契約であり、[境界ごとの確認](references/platform-apis.md#serialization-boundaries) を行う。

## 検証と返す内容

変更の種類に合わせて既存の型チェック、lint、Workers runtime テストを実行する。`@cloudflare/vitest-pool-workers` が既にある場合は活用するが、レビューのためにテスト基盤を無断導入しない。`KV.get()` の `null`、例外、リクエスト間の分離など変更に関係する境界条件を確認する。

[レビュー記録](assets/review-template.md) に、対象、使用した版・互換設定、優先度付き所見、ファイル位置、根拠、推奨修正、実行済み検証、未確認を記す。所見ごとに runtime の影響を説明し、一般的な推奨と実際の不具合を分ける。

このスキルはデプロイ、秘密値登録、課金リソース作成、アカウント設定変更、依存の自動更新を承認しない。操作は利用者の依頼範囲と環境の権限に従う。別の Cloudflare スキルや MCP のインストールは不要。Durable Objects の詳細や Workflows 固有設計が必要になった場合は、利用可能な関連スキルまたは公式資料へ範囲を広げる。
