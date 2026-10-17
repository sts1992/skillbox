# 出典・ライセンス・変更記録

## 固定した上流

- リポジトリ: [cloudflare/skills](https://github.com/cloudflare/skills)
- 原著者・公開主体: Cloudflare。GitHub の所有組織および固定コミットの [.codex-plugin/plugin.json](https://github.com/cloudflare/skills/blob/86505e44f87d801aa1864a3c4109e9a8ae5c409f/.codex-plugin/plugin.json) の author を確認。
- 取得日: 2026-10-17 UTC
- 取得時の既定ブランチ: `main`
- 固定コミット: `86505e44f87d801aa1864a3c4109e9a8ae5c409f`
- 原文: [skills/workers-best-practices](https://github.com/cloudflare/skills/tree/86505e44f87d801aa1864a3c4109e9a8ae5c409f/skills/workers-best-practices)
- 原文 SKILL.md の Git blob: `a669596e421f1945bd6a37d5f4dc012752428919`

## ライセンス

リポジトリ直下の [LICENSE](https://github.com/cloudflare/skills/blob/86505e44f87d801aa1864a3c4109e9a8ae5c409f/LICENSE) は Apache License 2.0。複製・派生物の作成・配布を許諾する条件に従い、本文をこのフォルダの [LICENSE](LICENSE) に変更せず収録した。対象スキル内の別ライセンスおよび上流ツリーの NOTICE ファイルは確認されなかった。日本語化・編集した `SKILL.md` には変更表示を置いた。Cloudflare による本版の承認や商標使用許諾を意味しない。

## 収録ファイルと変更

- `SKILL.md`: 上流の実質的な手順を日本語化・再構成。Workers 固有の入口、入力、出力、権限境界、未検証の扱いを追加。
- `references/configuration.md`: 原文を変更せず収録。Git blob `96590b1d1fcad31a9c62d33174ed68ca3adf1c07`。
- `references/platform-apis.md`: 原文を変更せず収録。Git blob `68af36add31e223ea9ac41d8895de7370e80201e`。
- `references/runtime-patterns.md`: 原文を変更せず収録。Git blob `bdb8c03882b6ecd658d91b3cd44a1b5203ddd3fc`。
- `assets/review-template.md`: 日本語のレビュー記録用テンプレートを追加。
- `agents/openai.yaml`: 日本語の表示情報を追加。上流と同様に通常のスキル選択を許可。
- 他の Cloudflare スキルへの必須依存をなくし、必要時は公式資料で補えるようにした。上流プラグインの MCP、インストール設定、ロゴ等は含めない。
- 古い制限値、料金・性能表現、Zod の版、テストツールの挙動は固定原文だけで断定しない旨を追記。Node.js 互換フラグ、TOML 移行、Hyperdrive、fail-open の採否を対象コードと設定に照らすよう補足。

日本語化・追加資料は同梱 Apache-2.0 の条件で配布する。

## 必要な環境と依存

資料の閲覧だけなら追加ツールは不要。実装・検証には対象プロジェクトの JavaScript / TypeScript 環境、Wrangler、生成型、既存のテスト環境を使う。ネットワークは最新の公式資料を照合する際に使用する。Cloudflare アカウント、API token、Cloudflare MCP、他のスキルは本スキルの閲覧・静的レビューの必須条件ではない。

## 検証の範囲

固定コミットの GitHub ファイルとライセンスを読み、ファイル構造、相対リンク、frontmatter、日本語本文、原文ファイルの同一性を静的に確認するためのパッケージ。上流のスキル・コード例・スクリプトは実行しておらず、依存のインストール、Cloudflare への接続、テスト用 Worker の作成やデプロイも行っていない。現在の全 API・制限・料金の実機検証、性能保証、セキュリティ保証は含まれない。
