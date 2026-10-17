# 出典・ライセンス・変更記録

## 固定した上流

- リポジトリ: [cursor/plugins](https://github.com/cursor/plugins)
- 公開主体: GitHub 所有組織 `cursor`
- 原著者: Lauren Tan。固定コミットの [pstack/.cursor-plugin/plugin.json](https://github.com/cursor/plugins/blob/101b274dd991f694e1f7024be2157e5f3adf07de/pstack/.cursor-plugin/plugin.json) の author と `pstack/LICENSE` の著作権表示で確認。
- 取得日: 2026-10-17 UTC
- 取得時の既定ブランチ: `main`
- 固定コミット: `101b274dd991f694e1f7024be2157e5f3adf07de`
- 原文: [pstack/skills/benchmark-checklist/SKILL.md](https://github.com/cursor/plugins/blob/101b274dd991f694e1f7024be2157e5f3adf07de/pstack/skills/benchmark-checklist/SKILL.md)
- 原文 SKILL.md の Git blob: `e901d1fdbc9ffce53e94d6514be7d9a22e771a1a`
- pstack plugin の表示バージョン: `0.15.25`。再現性の基準は上記コミット。

## ライセンス

`cursor/plugins` の root には共通ライセンスがなかったが、対象が属する [pstack/LICENSE](https://github.com/cursor/plugins/blob/101b274dd991f694e1f7024be2157e5f3adf07de/pstack/LICENSE) に MIT License と `Copyright (c) 2026 Lauren Tan` がある。plugin manifest の `license` も MIT。複製・修正・配布を許諾する条件に従い、著作権表示と許諾文を含む全原文を [LICENSE](LICENSE) に変更せず収録した。対象スキル配下に別ライセンスはなく、root / pstack に NOTICE は確認されなかった。他 plugin や third_party のライセンスは本スキルに流用していない。

## ローカルでの変更

- 元の 7 質問、概算時の限定例外、最低 5 回の交互実行、中央値と範囲、判断不能の条件、報告方法を日本語化。
- Linux 専用コマンドを必要時の例にし、計測環境に合う同等手段を許容した。
- 実行済み結果のレビューだけでも利用できるようにし、測っていない項目を未確認として残すようにした。
- 実測前のスクリプト内容確認、データ・費用・共有環境への影響、無断のプロセス停止やツール導入を避ける境界を補足。
- 速度向上率と所要時間短縮率、実行内の p50 と実行間の中央値の混同を避ける説明を追加。
- 上流の Opening a PR / Perf issue / Hillclimb playbook への前提を、単独で実行できる報告・baseline 検証・計測基盤固定の説明に置き換えた。他 playbook の実行やインストールを要求しない。
- `assets/benchmark-report.md` に日本語の測定記録テンプレートを追加。
- 上流の `disable-model-invocation: true` に対応する明示呼び出し方針を、Codex の `agents/openai.yaml` の `policy.allow_implicit_invocation: false` で保持。Codex 用 SKILL.md の frontmatter には `name` と `description` のみを使用。
- 日本語の表示情報と呼び出し例を追加。pstack plugin 全体、agent、hook、実行スクリプトは含めない。

日本語化・追加資料も同梱 MIT License の条件で配布する。

## 必要な環境と依存

固定された必須パッケージ、MCP、アカウント、スクリプトはない。提供済みの測定記録・ソースを読むだけなら追加ツールは不要。実測時は対象プロジェクトの既存ベンチマークと、その言語・OS に対応する利用可能な観測手段を使う。`uptime` / `nproc` / `top` / `pidstat` / `node --cpu-prof` / `py-spy` / `perf` / `strace` は状況に応じた例であり、一括導入しない。

## 検証の範囲

固定コミットの原文・author・LICENSE・依存記述を読み、パッケージ構造、相対リンク、frontmatter、日本語本文、ライセンスの同一性を静的に確認するためのパッケージ。ベンチマーク、上流の skill / script、プロファイラは実行しておらず、ツールのインストールや外部環境への負荷試験も行っていない。特定のソフトウェアの性能評価や統計上の有意差を保証するものではない。
