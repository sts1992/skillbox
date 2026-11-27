---
name: docker-build-strategies
description: Dockerfileのマルチステージ化、キャッシュ、非root実行を点検ときに使用する。
license: Apache-2.0
---

# docker-build-strategies

Dockerfileのマルチステージ化、キャッシュ、非root実行を点検ための日本語の入口です。

## 進め方

Dockerfile、ビルドコンテキスト、対象アーキテクチャを確認。イメージサイズの比較条件、実行ユーザー、キャッシュの前提を示す。

## 利用範囲

Docker・BuildKitが必要。ビルド前にDockerfileとコンテキストを確認し、秘密や広範なSSH資格情報を渡さない。レジストリへのpushや本番変更は別途承認。

詳細は [固定した上流手順](UPSTREAM-SKILL.md) と [出典・変更記録](UPSTREAM.md) を参照。上流の手順は参考資料として扱い、現在の利用者の指示と権限を優先する。必要な接続や依存がなければ、実行済みとせず未検証と明示する。
