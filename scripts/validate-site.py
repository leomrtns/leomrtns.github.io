"""Check the built site, migrated notebook contents, feeds, and legacy assets."""
import argparse
import hashlib
from html.parser import HTMLParser
import json
from pathlib import Path
import re
from urllib.parse import unquote, urlsplit
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / '_site'
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--check-migration', action='store_true', help='Verify original C code and outputs are unchanged')
args = parser.parse_args()
errors = []

class Page(HTMLParser):
  def __init__(self):
    super().__init__()
    self.links = []
    self.ids = set()
    self.title_count = 0
  def handle_starttag(self, tag, pairs):
    attrs = dict(pairs)
    if tag == 'title':
      self.title_count += 1
    if attrs.get('id'):
      self.ids.add(attrs['id'])
    for key in ['href', 'src']:
      if attrs.get(key):
        self.links.append(attrs[key])

pages = [OUT / p for p in ['index.html','projects/index.html','blog/index.html','about/index.html',
                           'publications/index.html','doxygen/index.html','404.html']]
# Renamed post directories leave redirect pages behind. Count only current article sources.
article_pages = sorted({OUT / source.relative_to(ROOT).with_suffix('.html')
                        for source in (ROOT / 'posts').glob('*/index.*')
                        if source.suffix in {'.md', '.qmd', '.ipynb'}
                        and (OUT / source.relative_to(ROOT).with_suffix('.html')).exists()})
pages += article_pages
parsed = {}
for path in pages:
  if not path.exists():
    errors.append(f'Missing page: {path.relative_to(OUT)}')
    continue
  text = path.read_text()
  page = Page()
  page.feed(text)
  parsed[path] = page
  if page.title_count != 1:
    errors.append(f'Expected one title: {path.relative_to(OUT)}')
  if '{{site.' in text or '{% include' in text:
    errors.append(f'Unconverted Jekyll markup: {path.relative_to(OUT)}')
  footer = text.split('<footer', 1)[-1]
  if 'https://www.liverpool.ac.uk/people/leonardo-de-oliveira-martins' not in footer:
    errors.append(f'Missing Liverpool profile in footer: {path.relative_to(OUT)}')
  for icon in ['globe', 'envelope-fill', 'github', 'mastodon', 'bluesky', 'linkedin', 'rss-fill']:
    if f'bi-{icon}"' not in footer:
      errors.append(f'Missing footer icon {icon}: {path.relative_to(OUT)}')
for path, page in parsed.items():
  for value in page.links:
    url = urlsplit(value)
    if url.scheme or url.netloc or value.startswith('data:'):
      continue
    target = (OUT / unquote(url.path).lstrip('/')) if url.path.startswith('/') else path.parent / unquote(url.path)
    if not url.path:
      target = path
    target = target.resolve()
    if target.is_dir():
      target /= 'index.html'
    if not target.exists():
      errors.append(f'{path.relative_to(OUT)} → missing {value}')
    if not url.path and url.fragment and not url.fragment.startswith('category='):
      if unquote(url.fragment) not in page.ids:
        errors.append(f'{path.relative_to(OUT)} → missing fragment {value}')

mapping = json.loads((ROOT / 'scripts/migration-map.json').read_text())
blog = (OUT / 'blog/index.html').read_text()
if blog.count('class="thumbnail-image"') != len(article_pages):
  errors.append('Each published post should have one blog listing thumbnail')
if 'category=Binfie' in (OUT / 'projects/index.html').read_text():
  errors.append('The removed Binfie category shortcut is still on Projects')
for relative, count in [('projects/index.html', 14), ('index.html', 3)]:
  if (OUT / relative).read_text().count('class="project-art"') != count:
    errors.append(f'Missing project artwork: {relative}')
publications = (OUT / 'publications/index.html').read_text()
if '<li class="publication">' not in publications or 'https://orcid.org/0000-0001-5247-1320' not in publications:
  errors.append('Publications page is missing records or the ORCID source link')
if 'class="review-summary"' not in publications or '<summary>Reviewing by journal</summary>' not in publications:
  errors.append('Publications page is missing the peer-review summary or journal breakdown')
for item in mapping:
  current_page = OUT / Path(item['target']).with_suffix('.html')
  if not current_page.exists():
    errors.append(f'Missing migrated article: {item["target"]}')
  if item['target'].endswith('.ipynb'):
    source = ROOT / item['target']
    doc = json.loads(source.read_text())
    payload = [{'source':c['source'],'outputs':c.get('outputs',[]),'execution_count':c.get('execution_count')}
               for c in doc['cells'] if c['cell_type']=='code']
    digest = hashlib.sha256(json.dumps(payload,sort_keys=True).encode()).hexdigest()
    if args.check_migration and digest != item['code_outputs_sha256']:
      errors.append(f'Migrated code or output changed: {item["target"]}')
    if not (OUT / item['target']).exists():
      errors.append(f'Notebook download missing: {item["target"]}')
  for alias in item['aliases']:
    target = OUT / alias.lstrip('/')
    if alias.endswith('/'):
      target /= 'index.html'
    if not target.exists():
      errors.append(f'Missing old route: {alias}')
    else:
      redirect = Page()
      redirect.feed(target.read_text())
      if not any((target.parent / unquote(urlsplit(link).path)).resolve() == current_page.resolve()
                 for link in redirect.links):
        errors.append(f'Old route does not point to its current article: {alias}')
  current = current_page.parent
  for previous in item.get('previous_directories', []):
    for resource in current.rglob('*'):
      if not resource.is_file() or resource.suffix == '.html':
        continue
      old_resource = OUT / previous / resource.relative_to(current)
      if not old_resource.exists() or old_resource.read_bytes() != resource.read_bytes():
        errors.append(f'Renamed article resource missing/changed: {old_resource.relative_to(OUT)}')

for folder in ['doxygen-biomcmclib', 'SpecImage']:
  for source in (ROOT / folder).rglob('*'):
    if not source.is_file():
      continue
    destination = OUT / source.relative_to(ROOT)
    if not destination.exists() or source.read_bytes() != destination.read_bytes():
      errors.append(f'Legacy resource missing/changed: {source.relative_to(ROOT)}')

for forbidden in ['old','_drafts','_posts','_pages','authoring','scripts','.github','.local-state','publications/data']:
  if (OUT / forbidden).exists():
    errors.append(f'Nonpublic authoring directory in output: {forbidden}')

feed = ET.parse(OUT / 'blog/index.xml')
items = feed.findall('./channel/item')
if len(items) < len(mapping):
  errors.append(f'RSS contains only {len(items)} of {len(mapping)} migrated posts')
for name in ['feed.xml','jupyterblog/feed.xml']:
  if (OUT / name).read_bytes() != (OUT / 'blog/index.xml').read_bytes():
    errors.append(f'Legacy feed differs: {name}')
if errors:
  raise SystemExit('\n'.join(sorted(set(errors))))
print(f'Validated {len(pages)} pages, {len(mapping)} migrated posts, notebook downloads, RSS, and legacy assets.')

if args.check_migration:
  print('All five migrated C notebooks retain their original code and outputs.')
