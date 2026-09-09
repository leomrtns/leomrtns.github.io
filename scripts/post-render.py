"""Keep earlier blog indexes, feeds and downloadable attachments accessible."""
from html import escape
from pathlib import Path
import json
import os
import shutil
import yaml

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / os.environ.get('QUARTO_PROJECT_OUTPUT_DIR', '_site')
OUTPUT.mkdir(exist_ok=True)
(OUTPUT / '.nojekyll').touch()

redirects = {
  'posts/index.html': 'blog/index.html',
  'categories/index.html': 'blog/index.html',
  'jupyterblog/index.html': 'blog/index.html',
  'jupyterblog/about.html': 'about/index.html',
  'jupyterblog/search.html': 'blog/index.html',
  'jupyterblog/categories/index.html': 'blog/index.html',
  'jupyterblog/tags.html': 'blog/index.html',
  'misc/welcome/index.html': 'posts/260104-welcome/index.html',
  'personal/back-to-blogging/index.html': 'posts/260105-back-to-blogging/index.html',
}
mapping = json.loads((ROOT / 'scripts/migration-map.json').read_text())
for item in mapping:
  target = str(Path(item['target']).with_suffix('.html'))
  for alias in item['aliases']:
    alias = alias.lstrip('/')
    redirects[alias + 'index.html' if alias.endswith('/') else alias] = target
for old, new in redirects.items():
  if not (OUTPUT / new).exists():
    continue
  destination = OUTPUT / old
  destination.parent.mkdir(parents=True, exist_ok=True)
  relative = os.path.relpath(OUTPUT / new, destination.parent)
  destination.write_text(
    '<!doctype html><html lang="en"><meta charset="utf-8">'
    '<meta name="viewport" content="width=device-width,initial-scale=1">'
    '<meta name="robots" content="noindex">'
    f'<meta http-equiv="refresh" content="0;url={escape(relative, quote=True)}">'
    '<title>Page moved · Leo Martins</title>'
    f'<p>This page has moved. <a href="{escape(relative, quote=True)}">Continue to the new page</a>.</p>'
    f'<script>location.replace({json.dumps(relative)} + location.search + location.hash);</script></html>\n'
  )
feed = OUTPUT / 'blog/index.xml'
if feed.exists():
  for name in ['feed.xml', 'jupyterblog/feed.xml']:
    destination = OUTPUT / name
    destination.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(feed, destination)
asset = OUTPUT / 'posts/220816-invariant-sites/20220816.blogentry.txz'
if asset.exists():
  destination = OUTPUT / 'jupyterblog/assets/20220816.blogentry.txz'
  destination.parent.mkdir(parents=True, exist_ok=True)
  shutil.copy2(asset, destination)

# Copy downloadable notebooks only for published articles.
# A draft notebook must not be exposed as a raw resource.
for source in (ROOT / 'posts').glob('*/index.*'):
  if source.suffix not in {'.ipynb', '.md', '.qmd'}:
    continue
  if source.suffix == '.ipynb':
    notebook = json.loads(source.read_text())
    header = ''.join(notebook['cells'][0].get('source', []))
  else:
    header = source.read_text()
  metadata = yaml.safe_load(header.split('---', 2)[1]) if header.startswith('---') else {}
  destination = OUTPUT / source.parent.relative_to(ROOT)
  if (metadata or {}).get('draft') is True:
    if destination.is_dir():
      shutil.rmtree(destination)  # Generated output only; source drafts are retained.
  elif source.suffix == '.ipynb' and (destination / 'index.html').exists():
    shutil.copy2(source, destination / source.name)

# Keep directly shared notebook/figure/download URLs working after a directory rename.
# HTML at the previous URL is a redirect; non-HTML resources retain their original bytes.
for item in mapping:
  current = OUTPUT / Path(item['target']).parent
  if not (current / 'index.html').exists():
    continue
  for previous in item.get('previous_directories', []):
    for source in current.rglob('*'):
      if not source.is_file() or source.suffix == '.html':
        continue
      destination = OUTPUT / previous / source.relative_to(current)
      destination.parent.mkdir(parents=True, exist_ok=True)
      shutil.copy2(source, destination)
