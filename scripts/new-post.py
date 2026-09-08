"""Create a draft without changing or publishing existing files."""
import argparse
from datetime import date
import json
from pathlib import Path
import re

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('slug', help='Short lowercase name with hyphens')
parser.add_argument('--title', required=True)
parser.add_argument('--format', choices=['md', 'ipynb', 'qmd'], default='md')
args = parser.parse_args()
if not re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*', args.slug):
  parser.error('Use lowercase letters, numbers, and hyphens for the slug.')
root = Path(__file__).resolve().parents[1]
folder = root / 'posts' / args.slug
folder.mkdir(parents=True, exist_ok=False)
source = root / 'authoring/templates' / ('post.' + args.format)
text = source.read_text()
if args.format == 'ipynb':
  notebook = json.loads(text)
  header = ''.join(notebook['cells'][0]['source'])
  header = re.sub(r'^title:.*$', lambda _: 'title: ' + json.dumps(args.title), header, flags=re.M)
  header = re.sub(r'^date:.*$', 'date: ' + date.today().isoformat(), header, flags=re.M)
  notebook['cells'][0]['source'] = header.splitlines(keepends=True)
  text = json.dumps(notebook, indent=1) + '\n'
else:
  text = re.sub(r'^title:.*$', lambda _: 'title: ' + json.dumps(args.title), text, flags=re.M)
  text = re.sub(r'^date:.*$', 'date: ' + date.today().isoformat(), text, flags=re.M)
target = folder / ('index.' + args.format)
target.write_text(text)
print(f'Created draft: {target}')
print('Set draft: false when the post is ready to appear in the site.')
