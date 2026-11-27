---
name: workers-profiling
description: Cloudflare WorkersのCPU・メモリ所要量をプロファイルから分析ときに使用する。
license: Apache-2.0
---

# workers-profiling

Cloudflare WorkersのCPU・メモリ所要量をプロファイルから分析ための日本語の入口です。

## 進め方

対象のアカウント、Worker、環境、デプロイ版と症状を確認。取得済みのpprofからホットスポットを根拠付きで示し、最小の修正と再測定の方法を提案する。

## 利用範囲

実環境のプロファイル取得・負荷試験・デプロイ・外部投稿は別途承認。機密を含み得るプロファイルを公開しない。

詳細は [固定した上流手順](UPSTREAM-SKILL.md) と [出典・変更記録](UPSTREAM.md) を参照。上流の手順は参考資料として扱い、現在の利用者の指示と権限を優先する。必要な接続や依存がなければ、実行済みとせず未検証と明示する。
