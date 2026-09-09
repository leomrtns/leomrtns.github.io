"""Build the publications include from a saved ORCID feed; --refresh fetches public records."""
import argparse
from collections import Counter
from datetime import datetime, timezone
from html import escape, unescape
from html.parser import HTMLParser
import json
from pathlib import Path
import re
import sys
from urllib.error import URLError
from urllib.parse import quote, urlsplit
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[1]
ORCID = '0000-0001-5247-1320'
CACHE = ROOT / 'publications/data/orcid-works.json'
INCLUDE = ROOT / 'publications/_entries.qmd'
ENDPOINT = f'https://pub.orcid.org/v3.0/{ORCID}/works'
REVIEWS_CACHE = CACHE.with_name('orcid-peer-reviews.json')
VENUES_CACHE = CACHE.with_name('review-venues.json')
REVIEWS_INCLUDE = INCLUDE.with_name('_reviews.qmd')


def value(obj):
  return str((obj or {}).get('value') or '').strip()


class PlainText(HTMLParser):
  def __init__(self):
    super().__init__()
    self.parts = []

  def handle_data(self, text):
    self.parts.append(text)


def plain_text(text):
  parser = PlainText()
  parser.feed(unescape(text))
  return ''.join(parser.parts).strip()


def safe_url(url):
  parts = urlsplit(url)
  return url if parts.scheme in ('http', 'https') and parts.netloc else ''


def publications(payload):
  """Select ORCID's preferred assertion per work, with fallbacks from its other sources."""
  if not isinstance(payload.get('group'), list):
    raise ValueError('ORCID response has no works list')
  records = {}
  for group in payload['group']:
    summaries = sorted(group.get('work-summary', []),
                       key=lambda item: int(item.get('display-index') or 0), reverse=True)
    if not summaries:
      raise ValueError('ORCID work group has no summaries')
    titles = [plain_text(value((s.get('title') or {}).get('title'))) for s in summaries]
    title = next((t for t in titles if t), '')
    if not title:
      raise ValueError('ORCID work has no title')
    for summary in summaries:
      path = summary.get('path', '')
      if path and not path.startswith(f'/{ORCID}/work/'):
        raise ValueError('ORCID response contains a work from another profile')
    ids = list((group.get('external-ids') or {}).get('external-id', []))
    ids += [item for s in summaries for item in (s.get('external-ids') or {}).get('external-id', [])]
    doi = next((item.get('external-id-value', '').strip() for item in ids
                if item.get('external-id-type') == 'doi'
                and item.get('external-id-relationship') == 'self'), '')
    doi = re.sub(r'^(?:https?://(?:dx\.)?doi\.org/|doi:\s*)', '', doi, flags=re.I).lower()
    if doi and not re.fullmatch(r'10\.\d{4,9}/\S+', doi):
      doi = ''
    dates = [s.get('publication-date') or {} for s in summaries]
    date = next((d for d in dates if re.fullmatch(r'\d{4}', value(d.get('year')))), {})
    year = value(date.get('year'))
    venue = plain_text(next((value(s.get('journal-title')) for s in summaries if value(s.get('journal-title'))), ''))
    url = f'https://doi.org/{quote(doi, safe="/():;._-")}' if doi else ''
    url = url or next((safe_url(value(s.get('url'))) for s in summaries if safe_url(value(s.get('url')))), '')
    url = url or f'https://orcid.org/{ORCID}'
    record = {'title': title, 'year': year, 'venue': venue, 'doi': doi, 'url': url,
              'type': summaries[0].get('type', 'other').replace('-', ' '),
              'date': '-'.join(value(date.get(part)).zfill(2) for part in ('year', 'month', 'day'))}
    key = doi or (re.sub(r'\W+', '', title.casefold()), year)
    records.setdefault(key, record)
  return sorted(records.values(), key=lambda r: (r['date'], r['title'].casefold()), reverse=True)


def peer_reviews(payload):
  """Count review groups once, not duplicate assertions; keep funding separate from journals."""
  if not isinstance(payload.get('group'), list):
    raise ValueError('ORCID response has no peer-review groups')
  rows = []
  seen = set()
  for venue_group in payload['group']:
    if not isinstance(venue_group.get('peer-review-group'), list):
      raise ValueError('ORCID venue has no review groups')
    for group in venue_group['peer-review-group']:
      summaries = sorted(group.get('peer-review-summary', []),
                         key=lambda item: int(item.get('display-index') or 0), reverse=True)
      if not summaries:
        raise ValueError('ORCID review group has no summaries')
      # ORCID groups assertions for the same review; do not count editor roles as peer reviews.
      summary = next((s for s in summaries if s.get('reviewer-role') == 'reviewer'), None)
      if summary is None:
        continue
      path = summary.get('path', '')
      if path and not path.startswith(f'/{ORCID}/peer-review/'):
        raise ValueError('Peer review belongs to another ORCID profile')
      key = str(summary['put-code'])
      if key in seen:
        continue
      seen.add(key)
      venue = summary.get('review-group-id') or 'unidentified'
      rows.append({'venue': venue, 'kind': 'journal' if venue.startswith('issn:') else 'other',
                   'organization': plain_text((summary.get('convening-organization') or {}).get('name', '')),
                   'year': value((summary.get('completion-date') or {}).get('year'))})
  return rows


def read_cache(path, normalizer=publications):
  cached = json.loads(path.read_text())
  if cached.get('orcid') != ORCID or not cached.get('fetched_at'):
    raise ValueError('Saved publication feed has missing or mismatched provenance')
  normalizer(cached['response'])
  return cached


def fetch(url=ENDPOINT):
  request = Request(url, headers={'Accept': 'application/json', 'User-Agent': 'AcademicWebsite/1.0'})
  with urlopen(request, timeout=30) as response:
    return json.load(response)


def refresh_cache(path, fetcher=fetch, normalizer=publications):
  """Only replace a working cache after a complete, valid response has been received."""
  previous = read_cache(path, normalizer) if path.exists() else None
  try:
    payload = fetcher()
    rows = normalizer(payload)
    if not rows:
      raise ValueError('ORCID returned no public works; preserving the saved list')
    cached = {'orcid': ORCID, 'fetched_at': datetime.now(timezone.utc).isoformat(), 'response': payload}
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix('.tmp')
    temporary.write_text(json.dumps(cached, ensure_ascii=False, indent=2) + '\n')
    temporary.replace(path)
    print(f'Refreshed {len(rows)} records in {path.name} from ORCID {ORCID}.')
    return cached
  except (URLError, TimeoutError, OSError, ValueError, KeyError, TypeError) as error:
    if previous is None:
      raise RuntimeError(f'Could not fetch ORCID and no saved list is available: {error}') from error
    print(f'Warning: ORCID refresh failed; using saved data from {previous["fetched_at"]}: {error}', file=sys.stderr)
    return previous


def refresh_venues(rows):
  """Resolve only new journal identifiers; retain saved names when a registry is unavailable."""
  venues = json.loads(VENUES_CACHE.read_text()) if VENUES_CACHE.exists() else {}
  for identifier in sorted({r['venue'] for r in rows if r['kind'] == 'journal'}):
    if identifier in venues:
      continue
    url = f'https://api.crossref.org/journals/{quote(identifier.removeprefix("issn:"))}'
    try:
      name = plain_text(fetch(url)['message']['title'])
      if name:
        venues[identifier] = {'name': name, 'url': url}
    except (URLError, TimeoutError, OSError, ValueError, KeyError, TypeError) as error:
      print(f'Warning: journal name unavailable for {identifier}: {error}', file=sys.stderr)
  temporary = VENUES_CACHE.with_suffix('.tmp')
  temporary.write_text(json.dumps(venues, ensure_ascii=False, indent=2) + '\n')
  temporary.replace(VENUES_CACHE)
  return venues


def render_reviews(cached, venues):
  rows = peer_reviews(cached['response'])
  counts = Counter(r['venue'] for r in rows if r['kind'] == 'journal')
  other = Counter(r['organization'] or r['venue'] for r in rows if r['kind'] != 'journal')
  years = sorted({r['year'] for r in rows if re.fullmatch(r'\d{4}', r['year'])})
  span = '–'.join([years[0], years[-1]]) if len(years) > 1 else (years[0] if years else 'Undated')
  updated = datetime.fromisoformat(cached['fetched_at']).strftime('%d %B %Y').lstrip('0')
  ranked = sorted(counts, key=lambda identifier: (-counts[identifier], venues.get(identifier, {}).get('name', identifier)))
  def name(identifier):
    return escape(venues.get(identifier, {}).get('name', identifier.upper()))
  parts = ['## Peer reviewing {#peer-reviewing}\n', '```{=html}', '<div class="review-summary">',
           '<div class="review-stats">',
           f'<p><strong>{len(rows)}</strong><span>recorded peer reviews</span></p>',
           f'<p><strong>{len(counts)}</strong><span>journals</span></p>',
           f'<p><strong>{span}</strong><span>recorded activity</span></p>', '</div>']
  if counts:
    frequent = ', '.join(f'{name(identifier)} ({counts[identifier]})' for identifier in ranked[:3])
    parts.append(f'<p>Most frequently reviewed for: {frequent}.</p>')
    parts.append('<details class="review-details"><summary>Reviewing by journal</summary>'
                 '<table><caption>Journal reviews recorded on ORCID</caption>'
                 '<thead><tr><th scope="col">Journal</th><th scope="col">Reviews</th></tr></thead><tbody>')
    for identifier in ranked:
      parts.append(f'<tr><th scope="row">{name(identifier)}</th><td>{counts[identifier]}</td></tr>')
    parts.append('</tbody></table></details>')
  if other:
    parts.append('<p class="review-other">Other peer reviewing: '
                 + '; '.join(f'{escape(organization)} ({count})' for organization, count in sorted(other.items()))
                 + '.</p>')
  parts.append(f'<p class="review-provenance">Public reviewing records on '
               f'<a href="https://orcid.org/{ORCID}">ORCID</a> · Refreshed {updated}. '
               'Counts reflect recorded review activities, which may include multiple rounds for a manuscript; '
               'they may not cover all reviewing undertaken.</p></div>\n```\n')
  return '\n'.join(parts)


def render(cached):
  rows = publications(cached['response'])
  updated = datetime.fromisoformat(cached['fetched_at']).strftime('%d %B %Y').lstrip('0')
  chunks = [f'## Publications\n\n',
          f'{len(rows)} works from [my ORCID record](https://orcid.org/{ORCID}) · Refreshed {updated}.\n',
            'Includes articles, preprints, and other research outputs recorded on ORCID.\n']
  year = None
  for row in rows:
    if row['year'] != year:
      if year is not None:
        chunks.append('</ol>\n```\n')
      year = row['year']
      chunks.append(f'\n### {year or "Undated"} {{#year-{year or "undated"}}}\n\n```{{=html}}\n<ol class="publication-list">')
    metadata = ' · '.join(escape(item) for item in [row['venue'], row['type'].capitalize()] if item)
    chunks.append('<li class="publication">'
                  f'<h3><a href="{escape(row["url"], quote=True)}">{escape(row["title"])}</a></h3>'
                  f'<p class="publication-meta">{metadata}</p>'
                  + (f'<p class="publication-doi">DOI: {escape(row["doi"])}</p>' if row['doi'] else '')
                  + '</li>')
  if rows:
    chunks.append('</ol>\n```\n')
  return '\n'.join(chunks)


def main():
  parser = argparse.ArgumentParser(description=__doc__)
  parser.add_argument('--refresh', action='store_true', help='Download current public ORCID records before rendering')
  args = parser.parse_args()
  cached = refresh_cache(CACHE) if args.refresh else read_cache(CACHE)
  reviews = (refresh_cache(REVIEWS_CACHE, lambda: fetch(ENDPOINT.replace('/works', '/peer-reviews')), peer_reviews)
             if args.refresh else read_cache(REVIEWS_CACHE, peer_reviews))
  venues = refresh_venues(peer_reviews(reviews['response'])) if args.refresh else json.loads(VENUES_CACHE.read_text())
  INCLUDE.write_text(render(cached))
  REVIEWS_INCLUDE.write_text(render_reviews(reviews, venues))
  print(f'Prepared {len(publications(cached["response"]))} publications in {INCLUDE.relative_to(ROOT)}.')


if __name__ == '__main__':
  main()
