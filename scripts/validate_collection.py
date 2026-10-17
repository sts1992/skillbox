#!/usr/bin/env python3
"""公開スキル集の構造・内部リンク・表示メタデータを検査する。内容の正しさは保証しない。"""
from pathlib import Path
import ast
import hashlib
import json
import re
import sys
try:
    import yaml
except ImportError:
    sys.exit('PyYAMLが必要です。許可された環境へ導入して再実行してください。')

ROOT = Path(__file__).resolve().parents[1]
EXPECTED = {
    'terraform-change-review', 'kubernetes-incident-triage',
    'observability-gap-review', 'cloud-cost-investigation',
    'incident-timeline-report', 'safe-runbook-authoring',
    'technical-decision-record', 'architecture-diagram-spec',
    'source-grounded-research-brief', 'public-transit-trip-planning',
}
IMPORTED = {
    'systematic-debugging', 'workers-best-practices',
    'benchmark-checklist', 'review-pr', 'yomiyasu',
}
errors = []

def check(ok, message):
    if not ok:
        errors.append(message)

actual = {p.parent.name for p in ROOT.glob('*/SKILL.md')}
check(actual == EXPECTED | IMPORTED | {'rebuild-editable-slides'}, f'スキル一覧が想定と異なる: {sorted(actual)}')
for name in sorted(EXPECTED | IMPORTED):
    base = ROOT / name
    path = base / 'SKILL.md'
    if not path.exists():
        check(False, f'{name}: SKILL.mdがない')
        continue
    text = path.read_text(encoding='utf-8')
    parts = text.split('---', 2)
    check(len(parts) == 3 and not parts[0].strip(), f'{name}: frontmatterがない')
    if len(parts) != 3:
        continue
    meta = yaml.safe_load(parts[1])
    check(isinstance(meta, dict), f'{name}: frontmatterが辞書ではない')
    if not isinstance(meta, dict):
        continue
    check(meta.get('name') == name, f'{name}: name不一致')
    check(bool(meta.get('description')), f'{name}: descriptionがない')
    check(bool(re.search(r'[ぁ-んァ-ン一-龯]', parts[2])), f'{name}: 日本語本文がない')
    check(len(text.splitlines()) < 500, f'{name}: 本文が500行以上')
    if name in EXPECTED:
        check(any((base / 'assets').glob('*')), f'{name}: 成果物テンプレートがない')
        check(any((base / 'references').glob('*')), f'{name}: 補足資料がない')
    if name in IMPORTED:
        check((base / 'LICENSE').is_file(), f'{name}: ライセンス原文がない')
        upstream = base / 'UPSTREAM.md'
        check(upstream.is_file(), f'{name}: 上流取得記録がない')
        if upstream.is_file():
            check(bool(re.search(r'\b[0-9a-f]{40}\b', upstream.read_text(encoding='utf-8'))), f'{name}: 取得commitがない')
        for py in base.rglob('*.py'):
            try:
                ast.parse(py.read_bytes(), filename=str(py))
            except SyntaxError as exc:
                check(False, f'{py.relative_to(ROOT)}: Python構文エラー: {exc}')
        for entry in base.rglob('*'):
            check(not entry.is_symlink(), f'{name}: symlinkは収録しない: {entry}')
    ui_path = base / 'agents/openai.yaml'
    if name in EXPECTED:
        check(ui_path.exists(), f'{name}: 表示メタデータがない')
    if ui_path.exists():
        ui = yaml.safe_load(ui_path.read_text(encoding='utf-8')).get('interface', {})
        check(25 <= len(ui.get('short_description', '')) <= 64, f'{name}: 表示説明の文字数不正')
        check('$' + name in ui.get('default_prompt', ''), f'{name}: 呼び出し例にスキル名がない')
    for md in base.rglob('*.md'):
        for target in re.findall(r'\[[^\]]*\]\(([^)]+)\)', md.read_text(encoding='utf-8')):
            if '://' in target or target.startswith('#') or target.startswith('mailto:'):
                continue
            local = target.split('#', 1)[0]
            check((md.parent / local).exists(), f'{md.relative_to(ROOT)}: リンク先がない: {target}')
manifest_path = ROOT / 'tests/imported-sources.json'
check(manifest_path.is_file(), '上流原文ファイルの照合manifestがない')
if manifest_path.is_file():
    manifest = json.loads(manifest_path.read_text(encoding='utf-8'))
    check(set(manifest['skills']) == IMPORTED, 'manifestのスキル一覧が不一致')
    for item in manifest['files']:
        path = ROOT / item['local_path']
        check(path.is_file(), f"上流ファイルがない: {item['local_path']}")
        if path.is_file():
            data = path.read_bytes()
            blob = b'blob ' + str(len(data)).encode('ascii') + b'\0' + data
            check(hashlib.sha1(blob).hexdigest() == item['blob_sha'], f"上流原文から変更されたファイル: {item['local_path']}")
for target in re.findall(r'\[[^\]]*\]\(([^)]+)\)', (ROOT / 'README.md').read_text(encoding='utf-8')):
    if '://' not in target and not target.startswith('#'):
        check((ROOT / target.split('#', 1)[0]).exists(), f'README: リンク先がない: {target}')
if errors:
    print('\n'.join(errors))
    sys.exit(1)
print(f'PASS: 独自{len(EXPECTED)}種類・上流由来{len(IMPORTED)}種類・既存1種類、構造・リンク・ライセンス・上流原文hash・Python構文')
