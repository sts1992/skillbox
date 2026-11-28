import {test} from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs/promises';
import os from 'node:os';
import path from 'node:path';
import {spawnSync} from 'node:child_process';
import {fileURLToPath} from 'node:url';
import {resolveLocalImage} from '../rebuild-editable-slides/scripts/local_image_path.mjs';

test('restricts image scope to regular PNG/JPEG paths in the layout directory', async (t) => {
  const tmp = await fs.mkdtemp(path.join(os.tmpdir(), 'skillbox-test-'));
  t.after(() => fs.rm(tmp, {recursive: true, force: true}));
  const workspace = path.join(tmp, 'layout');
  await fs.mkdir(path.join(workspace, 'crops'), {recursive: true});
  const inside = path.join(workspace, 'crops', 'fixture.PNG');
  const sibling = path.join(tmp, 'layout-other');
  await fs.mkdir(sibling);
  const outside = path.join(sibling, 'fixture.png');
  await fs.writeFile(inside, 'synthetic fixture (path test only)');
  await fs.writeFile(outside, 'synthetic fixture (path test only)');
  assert.equal(await resolveLocalImage(workspace, 'crops/fixture.PNG'), await fs.realpath(inside));
  assert.equal(await resolveLocalImage(workspace, inside), await fs.realpath(inside));
  await assert.rejects(resolveLocalImage(workspace, outside), /layout directory/);
  await assert.rejects(resolveLocalImage(workspace, path.relative(workspace, outside)), /layout directory/);
  await fs.mkdir(path.join(workspace, 'dir.png'));
  await assert.rejects(resolveLocalImage(workspace, 'dir.png'), /regular file/);
  try {
    await fs.symlink(outside, path.join(workspace, 'link.png'));
  } catch (err) {
    if (!['EPERM', 'ENOSYS'].includes(err.code)) throw err;
    t.diagnostic('symlink check unavailable on this host');
    return;
  }
  await assert.rejects(resolveLocalImage(workspace, 'link.png'), /layout directory/);
});

test('rejects a non-PPTX output name before reading input', () => {
  const builder = fileURLToPath(new URL('../rebuild-editable-slides/scripts/build_pptx.mjs', import.meta.url));
  const result = spawnSync(process.execPath, [builder, 'not-read.json', 'not-pptx.png'], {encoding: 'utf8'});
  assert.equal(result.status, 1);
  assert.match(result.stderr, /Output must have a \.pptx extension/);
});
