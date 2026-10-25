#!/usr/bin/env python3
"""K2 source-approval regression tests (offline, no network or playlists)."""
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from scripts import k2_source_approval_audit as gate


class SourceApprovalTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.registry = Path(self.tmp.name) / "approvals.json"
        self.sources = {"test-TR": "https://example.org/test.m3u"}
        self.patch_registry = patch.object(gate, "REGISTRY", self.registry)
        self.patch_sources = patch.object(gate, "declared_sources", return_value=self.sources)
        self.patch_registry.start()
        self.patch_sources.start()
        self.addCleanup(self.patch_registry.stop)
        self.addCleanup(self.patch_sources.stop)

    def write(self, entries, schema=1):
        self.registry.write_text(json.dumps({"schema_version": schema, "sources": entries}), encoding="utf-8")

    def test_missing_approval_stays_pending(self):
        self.write({})
        result = gate.audit()
        self.assertEqual(result["approved"], 0)
        self.assertEqual(result["pending"], 1)
        self.assertFalse(result["approval_complete"])

    def test_valid_evidence_is_accepted(self):
        self.write({"test-TR": {"url": self.sources["test-TR"], "status": "ONAYLI",
                                "approved_by": "reviewer", "approved_at": "2026-10-25",
                                "evidence": "review-reference"}})
        self.assertTrue(gate.audit()["approval_complete"])

    def test_missing_evidence_is_rejected(self):
        self.write({"test-TR": {"url": self.sources["test-TR"], "status": "ONAYLI",
                                "approved_by": "reviewer", "approved_at": "2026-10-25"}})
        self.assertTrue(gate.audit()["errors"])

    def test_changed_url_is_rejected(self):
        self.write({"test-TR": {"url": "https://other.example/test.m3u", "status": "BEKLIYOR"}})
        self.assertTrue(gate.audit()["errors"])

    def test_unknown_source_is_rejected(self):
        self.write({"other": {"url": "https://example.org/other.m3u", "status": "BEKLIYOR"}})
        self.assertTrue(gate.audit()["errors"])

    def test_workflow_checks_approval_before_install(self):
        workflow = (gate.ROOT / ".github/workflows/madsc-birlesik-kesif.yml").read_text(encoding="utf-8")
        self.assertLess(workflow.index("K2 onaylı kaynaklar olmadan otomatik keşfi engelle"),
                        workflow.index("Yayın kontrol aracını kur"))
        self.assertLess(workflow.index("K2 onaylı kaynaklar olmadan otomatik keşfi engelle"),
                        workflow.index("Kaynakları tara, tekrarları ayıkla ve adayları test et"))

    def test_duplicate_source_url_is_rejected(self):
        with patch.object(gate, "declared_sources", return_value={
            "test-TR": self.sources["test-TR"],
            "test-TR-copy": self.sources["test-TR"],
        }):
            self.write({})
            self.assertIn("duplicate source URLs declared", gate.audit()["errors"])

    def test_scanner_uses_repository_relative_registry(self):
        scanner = (gate.ROOT / "madsc_akilli_kesif.py").read_text(encoding="utf-8")
        self.assertIn('pathlib.Path(__file__).resolve().with_name("k2_kaynak_onaylari.json")', scanner)
        self.assertNotIn('pathlib.Path("k2_kaynak_onaylari.json").read_text', scanner)

    def test_scanner_rejects_duplicate_endpoints_directly(self):
        scanner = (gate.ROOT / "madsc_akilli_kesif.py").read_text(encoding="utf-8")
        self.assertIn('raise RuntimeError("Duplicate K2 discovery source URLs")', scanner)

    def test_non_http_source_is_rejected(self):
        with patch.object(gate, "declared_sources", return_value={"unsafe": "file:///etc/passwd"}):
            self.write({})
            self.assertTrue(gate.audit()["errors"])

    def test_http_scheme_without_hostname_is_rejected(self):
        with patch.object(gate, "declared_sources", return_value={"unsafe": "https:///missing-host.m3u"}):
            self.write({})
            self.assertTrue(gate.audit()["errors"])

    def test_invalid_schema_is_rejected(self):
        self.write({}, schema=2)
        with self.assertRaises(ValueError):
            gate.audit()


if __name__ == "__main__":
    unittest.main()
