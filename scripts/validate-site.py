"""Check current published articles, internal links, feeds, and legacy assets."""
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit, urljoin
import yaml

from site_content import post_sources, front_matter, feed_errors

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / '_site'
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
sources = list(post_sources(ROOT))
published = [source for source, draft in sources if not draft]
article_pages = sorted({OUT / source.relative_to(ROOT).with_suffix('.html') for source in published})
if len(article_pages) != len(published):
  errors.append('Use only one index source file per article directory')
for source, draft in sources:
  html = OUT / source.relative_to(ROOT).with_suffix('.html')
  download = OUT / source.relative_to(ROOT)
  if draft:
    if html.exists() or (source.suffix == '.ipynb' and download.exists()):
      errors.append(f'Draft is exposed in output: {source.relative_to(ROOT)}')
  elif source.suffix == '.ipynb':
    if not download.exists():
      errors.append(f'Notebook download missing: {source.relative_to(ROOT)}')
    elif download.read_bytes() != source.read_bytes():
      errors.append(f'Notebook download differs from current source: {source.relative_to(ROOT)}')
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

configuration = yaml.safe_load((ROOT / '_quarto.yml').read_text())
site_url = configuration['website']['site-url'].rstrip('/') + '/'
expected_urls = [urljoin(site_url, path.relative_to(OUT).as_posix()) for path in article_pages]
feed_options = front_matter((ROOT / 'blog/index.md').read_text())['listing'].get('feed', True)
feed_limit = feed_options.get('items', 20) if isinstance(feed_options, dict) else 20
errors += feed_errors(OUT / 'blog/index.xml', expected_urls, feed_limit)
for name in ['feed.xml','jupyterblog/feed.xml']:
  if not (OUT / name).exists() or not (OUT / 'blog/index.xml').exists():
    errors.append(f'Missing feed: {name} or blog/index.xml')
  elif (OUT / name).read_bytes() != (OUT / 'blog/index.xml').read_bytes():
    errors.append(f'Legacy feed differs: {name}')
if errors:
  raise SystemExit('\n'.join(sorted(set(errors))))
print(f'Validated {len(pages)} pages, {len(published)} published posts, notebook downloads, RSS, and legacy assets.')
