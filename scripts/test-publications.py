"""Check ORCID selection, safe rendering, and preservation of the offline publication list."""
from copy import deepcopy
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest
from urllib.error import URLError

spec = importlib.util.spec_from_file_location('publications', Path(__file__).with_name('update-publications.py'))
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


def work(title='A paper', index='1', **extra):
  return {'title': {'title': {'value': title}}, 'display-index': index, 'type': 'journal-article', **extra}


class PublicationsTest(unittest.TestCase):
  def test_preferred_record_fallbacks_and_doi_deduplication(self):
    older = work(index='0', **{'journal-title': {'value': 'A Journal'},
                              'publication-date': {'year': {'value': '2025'}}})
    group = {'work-summary': [older, work('Preferred title', index='2')],
             'external-ids': {'external-id': [{'external-id-type': 'doi',
                                             'external-id-relationship': 'self',
                                             'external-id-value': 'https://doi.org/10.1234/TEST'}]}}
    payload = {'group': [group, deepcopy(group)]}
    before = deepcopy(payload)
    rows = module.publications(payload)
    self.assertEqual(len(rows), 1)
    self.assertEqual(rows[0]['title'], 'Preferred title')
    self.assertEqual(rows[0]['year'], '2025')
    self.assertEqual(rows[0]['venue'], 'A Journal')
    self.assertEqual(rows[0]['url'], 'https://doi.org/10.1234/test')
    self.assertEqual(payload, before)

  def test_missing_dates_and_untrusted_metadata(self):
    payload = {'group': [{'work-summary': [work('<script>alert(1)</script>',
                           url={'value': 'javascript:alert(1)'})]}]}
    rendered = module.render({'response': payload, 'fetched_at': '2026-09-08T10:00:00+00:00'})
    self.assertIn('## Undated', rendered)
    self.assertIn('alert(1)', rendered)
    self.assertNotIn('<script>', rendered)
    self.assertNotIn('javascript:', rendered)
    self.assertEqual(module.plain_text('The <i>Escherichia coli</i> study &amp; methods'),
                     'The Escherichia coli study & methods')

  def test_failed_or_empty_refresh_preserves_cache(self):
    saved = {'orcid': module.ORCID, 'fetched_at': '2026-09-08T10:00:00+00:00',
             'response': {'group': [{'work-summary': [work()]}]}}
    temporary_root = module.ROOT / '.local-state/tests'
    temporary_root.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(dir=temporary_root) as folder:
      cache = Path(folder) / 'works.json'
      cache.write_text(json.dumps(saved))
      original = cache.read_bytes()
      def unavailable():
        raise URLError('Service temporarily unavailable')
      for fetcher in [unavailable, lambda: {'group': []}, lambda: {'error': 'API error'}]:
        self.assertEqual(module.refresh_cache(cache, fetcher), saved)
        self.assertEqual(cache.read_bytes(), original)
      with self.assertRaises(RuntimeError):
        module.refresh_cache(Path(folder) / 'missing.json', unavailable)


if __name__ == '__main__':
  unittest.main()
