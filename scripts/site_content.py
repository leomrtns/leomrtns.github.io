"""Discover current articles and check RSS without a historical migration inventory."""
from collections import Counter
import json
from urllib.parse import unquote, urlsplit, urlunsplit
import xml.etree.ElementTree as ET

import yaml


def front_matter(text):
  if text.startswith('---'):
    return yaml.safe_load(text.split('---', 2)[1]) or {}
  return {}


def post_sources(root):
  """Yield sources and draft flags, including inherited directory metadata."""
  defaults = yaml.safe_load((root / '_quarto.yml').read_text()) or {}
  for source in sorted((root / 'posts').rglob('index.*')):
    if source.suffix not in {'.md', '.qmd', '.ipynb'}:
      continue
    metadata = dict(defaults)
    for folder in reversed(source.parent.relative_to(root).parents):
      for name in ('_metadata.yml', '_metadata.yaml'):
        path = root / folder / name
        if path.exists():
          metadata.update(yaml.safe_load(path.read_text()) or {})
    for name in ('_metadata.yml', '_metadata.yaml'):
      path = source.parent / name
      if path.exists():
        metadata.update(yaml.safe_load(path.read_text()) or {})
    text = source.read_text()
    if source.suffix == '.ipynb':
      cells = json.loads(text)['cells']
      text = ''.join(cells[0].get('source', [])) if cells else ''
    metadata.update(front_matter(text))
    yield source, metadata.get('draft') is True


def canonical_url(value):
  url = urlsplit(value.strip())
  path = unquote(url.path)
  if path.endswith('/index.html'):
    path = path[:-len('index.html')]
  return urlunsplit((url.scheme, url.netloc, path.rstrip('/'), '', ''))


def feed_errors(path, expected_urls, limit=20):
  """Require current article URLs, no duplicates, and the configured feed size."""
  try:
    feed = ET.parse(path)
  except (OSError, ET.ParseError) as error:
    return [f'Cannot read RSS: {error}']
  if feed.getroot().tag != 'rss' or feed.find('./channel') is None:
    return ['RSS must contain an rss root and channel']
  expected = {canonical_url(url) for url in expected_urls}
  links = [canonical_url(item.findtext('link', '')) for item in feed.findall('./channel/item')]
  errors = []
  for link, count in Counter(links).items():
    if link not in expected:
      errors.append(f'RSS contains an unknown or unpublished post: {link or "(missing link)"}')
    if count > 1:
      errors.append(f'RSS contains a duplicate post: {link}')
  wanted = min(len(expected), limit)
  if len(links) != wanted:
    errors.append(f'RSS contains {len(links)} posts; expected {wanted} current published posts (limit {limit})')
  if len(expected) <= limit:
    for link in sorted(expected - set(links)):
      errors.append(f'RSS is missing published post: {link}')
  return errors
