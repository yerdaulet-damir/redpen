import importlib.util
import unittest
from pathlib import Path


MODULE_PATH = Path(__file__).with_name("eval.py")
SPEC = importlib.util.spec_from_file_location("redpen_eval", MODULE_PATH)
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC.loader
SPEC.loader.exec_module(MODULE)


class EvalHelpersTest(unittest.TestCase):
    def test_parse_json_ignores_wrapper_text(self):
        parsed = MODULE.parse_json('result: {"winner":"A"}\n')
        self.assertEqual(parsed["winner"], "A")

    def test_mirrored_redpen_win(self):
        forward = {"winner": "B"}
        reversed_order = {"winner": "A"}
        self.assertEqual(MODULE.mirrored_winner(forward, reversed_order), "redpen")

    def test_mirrored_baseline_win(self):
        forward = {"winner": "A"}
        reversed_order = {"winner": "B"}
        self.assertEqual(MODULE.mirrored_winner(forward, reversed_order), "baseline")

    def test_disagreement_is_unstable(self):
        forward = {"winner": "A"}
        reversed_order = {"winner": "A"}
        self.assertEqual(MODULE.mirrored_winner(forward, reversed_order), "unstable")


if __name__ == "__main__":
    unittest.main()
