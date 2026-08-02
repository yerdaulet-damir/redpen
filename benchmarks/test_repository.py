import json
import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class RepositoryIntegrityTest(unittest.TestCase):
    def test_skill_has_required_frontmatter(self):
        skill = (ROOT / "skills/redpen/SKILL.md").read_text(encoding="utf-8")
        match = re.match(r"---\n(.*?)\n---\n", skill, re.S)
        self.assertIsNotNone(match)
        frontmatter = match.group(1)
        self.assertRegex(frontmatter, r"(?m)^name:\s*redpen\s*$")
        self.assertRegex(frontmatter, r"(?m)^description:\s*>\s*$")

    def test_benchmark_cases_are_complete_and_unique(self):
        cases = json.loads((ROOT / "benchmarks/cases.json").read_text(encoding="utf-8"))
        required = {"id", "surface", "brief", "truth", "reader", "desired_action"}
        ids = [case["id"] for case in cases]
        self.assertEqual(len(ids), len(set(ids)))
        self.assertGreaterEqual(len(cases), 6)
        for case in cases:
            self.assertTrue(required <= case.keys())
            self.assertTrue(case["truth"])

    def test_structured_data_is_valid_and_visible(self):
        html = (ROOT / "docs/index.html").read_text(encoding="utf-8")
        blocks = re.findall(
            r'<script type="application/ld\+json">\s*(.*?)\s*</script>',
            html,
            re.S,
        )
        self.assertTrue(blocks)
        documents = [json.loads(block) for block in blocks]
        self.assertFalse(any(document.get("@type") == "FAQPage" for document in documents))
        application = next(
            document for document in documents if document.get("@type") == "SoftwareApplication"
        )
        self.assertIn(application["name"], html)
        self.assertIn(application["author"]["name"], html)


if __name__ == "__main__":
    unittest.main()
