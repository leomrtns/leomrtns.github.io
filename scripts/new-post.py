"""Create a draft without changing or publishing existing files."""
import argparse
from datetime import date
import json
from pathlib import Path
import re

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('slug', help='Short lowercase name with hyphens, without a date prefix')
parser.add_argument('--title', required=True)
parser.add_argument('--format', choices=['md', 'ipynb', 'qmd'], default='md')
parser.add_argument('--date', type=date.fromisoformat, default=date.today(), metavar='YYYY-MM-DD',
                    help='Post date and directory prefix (defaults to today)')
args = parser.parse_args()
if not re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*', args.slug):
  parser.error('Use lowercase letters, numbers, and hyphens for the slug.')
if re.match(r'^\d{6}-', args.slug):
  parser.error('Leave the YYMMDD prefix out of the slug; use --date YYYY-MM-DD to choose its date.')
root = Path(__file__).resolve().parents[1]
folder = root / 'posts' / f'{args.date:%y%m%d}-{args.slug}'
folder.mkdir(parents=True, exist_ok=False)
source = root / 'authoring/templates' / ('post.' + args.format)
text = source.read_text()
if args.format == 'ipynb':
  notebook = json.loads(text)
  header = ''.join(notebook['cells'][0]['source'])
  header = re.sub(r'^title:.*$', lambda _: 'title: ' + json.dumps(args.title), header, flags=re.M)
  header = re.sub(r'^date:.*$', 'date: ' + args.date.isoformat(), header, flags=re.M)
  notebook['cells'][0]['source'] = header.splitlines(keepends=True)
  text = json.dumps(notebook, indent=1) + '\n'
else:
  text = re.sub(r'^title:.*$', lambda _: 'title: ' + json.dumps(args.title), text, flags=re.M)
  text = re.sub(r'^date:.*$', 'date: ' + args.date.isoformat(), text, flags=re.M)
target = folder / ('index.' + args.format)
target.write_text(text)
print(f'Created draft: {target}')
print('Set draft: false when the post is ready to appear in the site.')
