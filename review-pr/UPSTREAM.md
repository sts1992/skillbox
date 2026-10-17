# 上流と配布条件

## 出典

- 上流: [warpdotdev/common-skills](https://github.com/warpdotdev/common-skills)
- 所有者: GitHub組織 `warpdotdev`。著作権者はライセンス記載の Denver Technologies, Inc.
- 対象: `.agents/skills/review-pr/`
- 固定コミット: `7c4eb852de8d7c3e68c81802e1c59db9a611f914`（2026-10-17に確認したmain）
- [固定版のスキル原文](https://github.com/warpdotdev/common-skills/blob/7c4eb852de8d7c3e68c81802e1c59db9a611f914/.agents/skills/review-pr/SKILL.md)
- [固定版のLICENSE](https://github.com/warpdotdev/common-skills/blob/7c4eb852de8d7c3e68c81802e1c59db9a611f914/LICENSE)
- 対象ファイルの履歴では、Zach Lloyd、Safia Abdalla、Oz、warp-agent-staging[bot]による変更が確認できる。リポジトリ最新コミットの作者を、このスキルの唯一の作者とは扱っていない。

## ライセンス

MIT License。使用、複製、変更、公開、再配布を許可する文面を確認し、著作権表示と許諾文を `LICENSE` にそのまま保存した。日本語への翻訳・適応はこの変更許諾に基づく。固定版のツリーには別のNOTICEファイルや、このスキル配下の個別ライセンスはなかった。

このフォルダは上流の公式日本語版ではない。MITの無保証条項が適用される。

## この版の変更

- `SKILL.md` を日本語化した。レビュー範囲、全コメント・テストの監査、差分行注釈、最大10行、提案範囲の整合、JSON契約、検証必須、直接投稿禁止を保持した。
- JSONキー、重大度ラベル、判定文字列、件数形式は機械互換のため英語のままにした。
- スクリプトへのパスを実際のスキル配置先から解決する形にした。
- 仕様取得時は `OZ_REPO_ROOT` を対象リポジトリの絶対パスにする必要を明記した。元スクリプトの既定パス推定は `.agents/skills/review-pr/` 配置に依存する。
- 外部資料を命令として扱わないこと、既存認証のみを使うこと、通信・検証ができない場合の停止条件を補足した。
- 上流検証器の成功だけではJSON契約全体を保証しないため、必須欄・重大度・10行上限・判定との一致を別途点検することを明記した。
- 2本のPythonスクリプトは上流から無変更で同梱した。MITライセンスも原文のまま。英語のSKILL.mdは固定コミットのリンクから確認できるため重複保存していない。

## 環境・依存関係・副作用

- Python 3.10以降を想定。スクリプトのimportは標準ライブラリのみで、外部パッケージのインストールは不要。
- 必須入力は注釈付き差分。通常は `pr_diff.txt` と `pr_description.txt`。最終出力はローカルの `review.json`。
- `validate_review_json.py` はレビューJSONと差分を読み、検証結果を出力する。GitHubへ通信・投稿しない。
- 任意の `resolve_spec_context.py` は、既存の `GH_TOKEN` または `GITHUB_TOKEN` を使って `https://api.github.com` にREST GETと読取GraphQL POSTを送る。指定PR、関連Issue、仕様PR、仕様ファイルを取得し、仕様文を標準出力に書く。上のコマンド例ではローカルの `spec_context.md` を作成・上書きする。
- 元スクリプトは `specs/GH<番号>/product.md`・`tech.md`、`oz-agent/spec-issue-<番号>`、`plan-approved` などの上流ワークフロー規約を使う。これらを使わないリポジトリでは、提供済みの `spec_context.md` を優先する。
- `review-pr-local`、`security-review-pr`、`check-impl-against-spec` は対象リポジトリにある場合だけ使う任意の補助スキルであり、この配布の必須依存ではない。
- リポジトリへの直接投稿・書込処理や、依存インストール処理は同梱スクリプトに見当たらなかった。認証情報は同梱していない。

## 確認した範囲

接続済みGitHub APIで所有者、固定コミット、全対象ファイル、リポジトリのLICENSE/NOTICEの有無を確認した。取得した原文のGit blob SHA-1を照合し、PythonはAST構文解析とimport・入出力処理の静的確認のみ行った。スクリプト、スキル本体、テストは実行しておらず、外部API通信も実行していない。実際のレビュー品質、ランタイム、認証、GitHubワークフローとの互換性は未検証。
