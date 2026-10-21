"""Fail-closed tests for the public package; no original archive required."""
from copy import deepcopy
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest

ROOT=Path(__file__).resolve().parents[1]
SPEC=importlib.util.spec_from_file_location('verify_release',ROOT/'scripts/verify_release.py')
V=importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(V)

class ReleaseTests(unittest.TestCase):
    def records(self):
        return [json.loads((ROOT/path).read_text(encoding='utf-8')) for path in
                ('data/draft_summary.json','data/draft_picks.json','data/team_scores.json','data/source_receipts.json','PROVENANCE.json')]

    def test_real_package(self):
        self.assertEqual(V.verify()['files'],18)

    def test_release_version_and_recorded_lineup_time(self):
        citation=(ROOT/'CITATION.cff').read_text(encoding='utf-8')
        self.assertIn('version: "1.0-minimal"',citation)
        self.assertNotIn('candidate',citation)
        for name in ('README.md','METHODS.md'):
            text=(ROOT/name).read_text(encoding='utf-8')
            self.assertIn('23:38:49 UTC on September 9, 2026',text)
            self.assertIn('about 41 minutes before the first kickoff',text)

    def test_duplicate_pick(self):
        records=self.records();records[1]['picks'][1]['pick']=records[1]['picks'][0]['pick']
        with self.assertRaisesRegex(ValueError,'Unique picks'):V.validate_records(*records)

    def test_duplicate_player(self):
        records=self.records();records[1]['picks'][1]['player_id']=records[1]['picks'][0]['player_id']
        with self.assertRaisesRegex(ValueError,'Unique player'):V.validate_records(*records)

    def test_missing_player_name(self):
        records=self.records();records[1]['picks'][0]['player_name']=''
        with self.assertRaisesRegex(ValueError,'Player names'):V.validate_records(*records)

    def test_fallback_cannot_become_ai(self):
        records=self.records()
        pick=next(p for p in records[1]['picks'] if p['origin']!='AI');pick['origin']='AI'
        with self.assertRaises(ValueError):V.validate_records(*records)

    def test_missing_score_does_not_become_zero(self):
        records=self.records();records[2]['teams'][0]['weeks_milli']['5']=None
        with self.assertRaisesRegex(ValueError,'invalid score'):V.validate_records(*records)

    def test_provisional_cannot_become_final(self):
        records=self.records();records[2]['week_states']['5']='FINAL'
        with self.assertRaisesRegex(ValueError,'Finality'):V.validate_records(*records)

    def test_receipt_cannot_gain_header_or_signed_url(self):
        records=self.records();records[3]['receipts'][0]['headers']={'example':'withheld'}
        with self.assertRaisesRegex(ValueError,'allowlist'):V.validate_records(*records)
        records=self.records();records[3]['receipts'][0]['download_url']+='?signature=example'
        with self.assertRaisesRegex(ValueError,'Unsafe'):V.validate_records(*records)

    def test_order_must_follow_exact_totals(self):
        records=self.records();records[2]['provisional_cumulative_order'].reverse()
        with self.assertRaisesRegex(ValueError,'order'):V.validate_records(*records)

    def test_unlisted_file_is_refused(self):
        # A fresh temp directory proves file-list rejection without modifying
        # this candidate or the original experiment.
        with tempfile.TemporaryDirectory() as directory:
            path=Path(directory);(path/'unexpected.txt').write_text('example',encoding='utf-8')
            with self.assertRaisesRegex(ValueError,'Unexpected'):V.verify(path)
