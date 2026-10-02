# 公式資料と再確認箇所

確認日: 2026-10-02。以下は参照先であり、最新の表示バージョンを対象環境のバージョンと同一視しない。

- [Terraform の JSON 出力仕様](https://developer.hashicorp.com/terraform/internals/json-format): actions の順序、unknown / sensitive のマスク、resource_drift、移動・取り込み、形式バージョンを確認する。未知の major は解釈を止める。新しい action を古い分類に押し込まない。
- [terraform show](https://developer.hashicorp.com/terraform/cli/commands/show): plan と state の表示、および JSON が機密値を平文で含み得ることを確認する。本スキルでは CLI の実行を許可する根拠として使わない。

provider 固有の属性の意味、既定値、置換条件は対象 provider の固定バージョンの公式資料で別途確認する。合成入力の example provider は架空であり、実在 provider の仕様を代用しない。
