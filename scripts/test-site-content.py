"""Regression checks for editorial changes and RSS validation."""
import json
from pathlib import Path
import tempfile
import unittest
import xml.etree.ElementTree as ET

from site_content import feed_errors, post_sources


class SiteContentTests(unittest.TestCase):
  def setUp(self):
    temporary_root = Path(__file__).resolve().parents[1] / '.local-state' / 'tests'
    temporary_root.mkdir(parents=True, exist_ok=True)
    self.temporary = tempfile.TemporaryDirectory(dir=temporary_root)
    self.addCleanup(self.temporary.cleanup)
    self.root = Path(self.temporary.name)
    (self.root / '_quarto.yml').write_text('website: {}\n')
    self.feed = self.root / 'feed.xml'

  def post(self, name, text='---\ntitle: Post\n---\n', extension='md'):
    path = self.root / 'posts' / name / ('index.' + extension)
    path.parent.mkdir(parents=True, exist_ok=True)
    if extension == 'ipynb':
      text = json.dumps({'cells': [{'cell_type': 'raw', 'source': text.splitlines(keepends=True)}]})
    path.write_text(text)
    return path

  def rss(self, links):
    root = ET.Element('rss')
    channel = ET.SubElement(root, 'channel')
    for link in links:
      ET.SubElement(ET.SubElement(channel, 'item'), 'link').text = link
    ET.ElementTree(root).write(self.feed)

  def urls(self):
    return ['https://example.com/' + source.relative_to(self.root).with_suffix('.html').as_posix()
            for source, draft in post_sources(self.root) if not draft]

  def test_delete_and_rename_need_no_inventory_update(self):
    first = self.post('first')
    second = self.post('second')
    self.rss(self.urls())
    self.assertEqual(feed_errors(self.feed, self.urls()), [])
    second.unlink()
    self.rss(self.urls())
    self.assertEqual(feed_errors(self.feed, self.urls()), [])
    first.parent.rename(first.parent.with_name('renamed'))
    self.rss(self.urls())
    self.assertEqual(feed_errors(self.feed, self.urls()), [])

  def test_drafts_in_all_formats_and_inherited_metadata(self):
    for extension in ('md', 'qmd', 'ipynb'):
      self.post(extension, '---\ndraft: true\n---\n', extension)
    inherited = self.post('group/inherited')
    (inherited.parent.parent / '_metadata.yml').write_text('draft: true\n')
    published = self.post('group/published', '---\ndraft: false\n---\n')
    self.assertEqual([source for source, draft in post_sources(self.root) if not draft], [published])

  def test_wrong_post_with_correct_count_is_rejected(self):
    self.post('first')
    self.rss(['https://example.com/posts/deleted/'])
    errors = '\n'.join(feed_errors(self.feed, self.urls()))
    self.assertIn('unknown or unpublished', errors)
    self.assertIn('missing published post', errors)

  def test_duplicate_cannot_replace_missing_post(self):
    self.post('first')
    self.post('second')
    self.rss([self.urls()[0]] * 2)
    errors = '\n'.join(feed_errors(self.feed, self.urls()))
    self.assertIn('duplicate', errors)
    self.assertIn('missing published post', errors)

  def test_directory_urls_and_configured_limit(self):
    for number in range(21):
      self.post(str(number))
    links = [url.removesuffix('index.html') for url in self.urls()]
    self.rss(links[:20])
    self.assertEqual(feed_errors(self.feed, self.urls()), [])
    self.rss(links[:5])
    self.assertEqual(feed_errors(self.feed, self.urls(), limit=5), [])
    self.assertTrue(feed_errors(self.feed, self.urls()))

  def test_missing_malformed_and_empty_feeds(self):
    self.assertTrue(feed_errors(self.feed, []))
    self.feed.write_text('<rss>')
    self.assertTrue(feed_errors(self.feed, []))
    self.feed.write_text('<html/>')
    self.assertTrue(feed_errors(self.feed, []))
    self.rss([])
    self.assertEqual(feed_errors(self.feed, []), [])


if __name__ == '__main__':
  unittest.main()
