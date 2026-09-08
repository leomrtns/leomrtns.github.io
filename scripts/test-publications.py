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
  def test_review_groups_roles_and_funding_are_counted_separately(self):
    review = {'reviewer-role': 'reviewer', 'put-code': 12, 'display-index': '1',
              'review-group-id': 'issn:1367-4811', 'completion-date': {'year': {'value': '2025'}}}
    duplicate = {**review, 'put-code': 13, 'display-index': '0'}
    funding = {**review, 'put-code': 14, 'review-group-id': 'fundref:10.13039/100010269',
               'convening-organization': {'name': 'Wellcome Trust'}}
    editor = {**review, 'put-code': 15, 'reviewer-role': 'editor'}
    payload = {'group': [{'peer-review-group': [
      {'peer-review-summary': [duplicate, review]}, {'peer-review-summary': [review]},
      {'peer-review-summary': [funding]}, {'peer-review-summary': [editor]}]}]}
    before = deepcopy(payload)
    rows = module.peer_reviews(payload)
    self.assertEqual(len(rows), 2)
    self.assertEqual([r['kind'] for r in rows], ['journal', 'other'])
    self.assertEqual(payload, before)
    html = module.render_reviews({'response': payload, 'fetched_at': '2026-09-08T10:00:00+00:00'},
                                 {'issn:1367-4811': {'name': 'Bioinformatics'}})
    self.assertIn('Bioinformatics (1)', html)
    self.assertIn('Wellcome Trust (1)', html)
    self.assertIn('<strong>1</strong><span>journals</span>', html)
    self.assertIn('<strong>2</strong><span>recorded peer reviews</span>', html)

  def test_review_cache_fallback_and_profile_validation(self):
    payload = {'group': [{'peer-review-group': [{'peer-review-summary': [{
      'reviewer-role': 'reviewer', 'put-code': 1, 'review-group-id': 'issn:1234-5678',
      'path': f'/{module.ORCID}/peer-review/1'}]}]}]}
    invalid = deepcopy(payload)
    invalid['group'][0]['peer-review-group'][0]['peer-review-summary'][0]['path'] = '/another-profile/peer-review/1'
    with self.assertRaises(ValueError):
      module.peer_reviews(invalid)
    saved = {'orcid': module.ORCID, 'fetched_at': '2026-09-08T10:00:00+00:00', 'response': payload}
    root = module.ROOT / '.local-state/tests'
    root.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(dir=root) as folder:
      cache = Path(folder) / 'reviews.json'
      cache.write_text(json.dumps(saved))
      self.assertEqual(module.refresh_cache(cache, lambda: invalid, module.peer_reviews), saved)

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
