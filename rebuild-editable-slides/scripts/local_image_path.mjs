import fs from 'node:fs/promises';
import path from 'node:path';

const imageExtensions = new Set(['.png', '.jpg', '.jpeg']);

function isInside(root, candidate) {
  const relative = path.relative(root, candidate);
  return relative !== '' && relative !== '..'
    && !relative.startsWith('..' + path.sep) && !path.isAbsolute(relative);
}

export async function resolveLocalImage(layoutDir, imagePath) {
  if (typeof imagePath !== 'string' || !imagePath.trim()) {
    throw new Error('Image crop path is required.');
  }
  const requestedRoot = path.resolve(layoutDir);
  const requested = path.resolve(requestedRoot, imagePath);
  if (!isInside(requestedRoot, requested)) {
    throw new Error('Image crop must stay in the layout directory.');
  }
  const root = await fs.realpath(requestedRoot);
  const file = await fs.realpath(requested);
  if (!isInside(root, file) || !imageExtensions.has(path.extname(file).toLowerCase())) {
    throw new Error('Image crop must resolve to a PNG/JPEG inside the layout directory.');
  }
  if (!(await fs.stat(file)).isFile()) {
    throw new Error('Image crop must be a regular file.');
  }
  return file;
}
