import importlib.util
import unittest
from pathlib import Path


MODULE_PATH = Path(__file__).with_name("eval.py")
SPEC = importlib.util.spec_from_file_location("redpen_eval", MODULE_PATH)
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC.loader
SPEC.loader.exec_module(MODULE)


class EvalHelpersTest(unittest.TestCase):
    @staticmethod
    def report(winner, a_failures=None, b_failures=None):
        return {
            "winner": winner,
            "a": {"hard_failures": a_failures or []},
            "b": {"hard_failures": b_failures or []},
        }

    def test_parse_json_ignores_wrapper_text(self):
        parsed = MODULE.parse_json('result: {"winner":"A"}\n')
        self.assertEqual(parsed["winner"], "A")

    def test_mirrored_redpen_win(self):
        forward = self.report("B")
        reversed_order = self.report("A")
        self.assertEqual(MODULE.mirrored_winner(forward, reversed_order), "redpen")

    def test_mirrored_baseline_win(self):
        forward = self.report("A")
        reversed_order = self.report("B")
        self.assertEqual(MODULE.mirrored_winner(forward, reversed_order), "baseline")

    def test_disagreement_is_unstable(self):
        forward = self.report("A")
        reversed_order = self.report("A")
        self.assertEqual(MODULE.mirrored_winner(forward, reversed_order), "unstable")

    def test_redpen_hard_failure_disqualifies_redpen(self):
        forward = self.report("B", b_failures=["invented fact"])
        reversed_order = self.report("A", a_failures=["invented fact"])
        self.assertEqual(MODULE.mirrored_winner(forward, reversed_order), "baseline")

    def test_baseline_hard_failure_disqualifies_baseline(self):
        forward = self.report("A", a_failures=["fake customer voice"])
        reversed_order = self.report("B", b_failures=["fake customer voice"])
        self.assertEqual(MODULE.mirrored_winner(forward, reversed_order), "redpen")

    def test_both_candidates_failing_is_invalid(self):
        forward = self.report("B", ["unclear"], ["invented fact"])
        reversed_order = self.report("A", ["invented fact"], ["unclear"])
        self.assertEqual(MODULE.mirrored_winner(forward, reversed_order), "invalid")

    def test_run_metadata_identifies_every_evaluation_input(self):
        metadata = MODULE.run_metadata("test skill")
        self.assertEqual(metadata["skill_sha256"], MODULE.hashlib.sha256(b"test skill").hexdigest())
        self.assertEqual(len(metadata["harness_sha256"]), 64)
        self.assertEqual(len(metadata["cases_sha256"]), 64)
        self.assertIn("generated_at", metadata)
        self.assertIn("commit", metadata)


if __name__ == "__main__":
    unittest.main()
