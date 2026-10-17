# 出典と変更点

- 著者: Jesse Vincent（obra / Superpowers）
- 上流: [obra/superpowers](https://github.com/obra/superpowers)
- 取得commit: `bb92a77741419a4ab5f06e711a283343f1ada0c3`
- 取得日: 2026-10-17
- 元スキル: [skills/systematic-debugging/SKILL.md](https://github.com/obra/superpowers/blob/bb92a77741419a4ab5f06e711a283343f1ada0c3/skills/systematic-debugging/SKILL.md)
- ライセンス: [MIT原文](https://github.com/obra/superpowers/blob/bb92a77741419a4ab5f06e711a283343f1ada0c3/LICENSE)を [LICENSE](LICENSE) に保持。コピー・改変・再配布が認められる条件に従い著作権表示を残す。対象ディレクトリとリポジトリ直下に別のNOTICEはない。

## ローカル変更

SKILL.mdを日本語に翻訳・再構成した派生版。四段階の調査、単一仮説、失敗再現、回帰確認、3回以上の失敗時の設計見直しを保持した。上流の重複する強調表現と裏付けのない一般的な割合の主張を省略した。

上流の別スキルへの必須参照を自己完結したテスト・検証手順に置き換えた。権限、秘密値の保護、緊急障害の影響緩和と根本修正の区別、資料内命令を実行しない境界を明示した。上流コード例のパス判定・テスト失敗処理・対象環境の制約も追記した。

以下5ファイルは同commitの `skills/systematic-debugging/` から無変更で収録する。参照内の英語や上流事例の数値も原文のまま。本文で必要なときだけ読む。

- root-cause-tracing.md
- defense-in-depth.md
- condition-based-waiting.md
- find-polluter.sh
- condition-based-waiting-example.ts

上流の作成ログ・圧力テスト教材は実利用の依存ではないため含めない。Superpowers全体のプラグイン、フック、他スキルは含めない。

## 利用環境と検証範囲

資料だけの調査はMarkdownとコードを読めるSkills対応エージェントで利用可能。修正・実測には対象プロジェクトの開発／テスト環境と適切な権限が必要。上流は複数のエージェント向けプラグインを持つが、この配布は独立したスキルディレクトリであり、プラグイン導入ではない。

収録時は内容・依存・ライセンス・構造の静的確認のみ。付属スクリプト、対象プロジェクトのテスト、本番操作は実行していない。上流事例のテスト数や改善率をこの派生版の検証実績とみなさない。
