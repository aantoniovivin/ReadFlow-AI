import sys
import unittest
from pathlib import Path

LOCAL_BACKEND = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(LOCAL_BACKEND))

from ai_service import local_briefing
from schemas import BriefingSection, MechanicalBlock, ComprehensionCheck


class ComprehensiveBriefingTests(unittest.TestCase):
    def test_local_briefing_has_comprehensive_blocks(self):
        text = "\n".join(
            f"Paragraph {index}: this extracted source supports a detailed concept, mechanism, and practical implication."
            for index in range(1, 8)
        )

        briefing = local_briefing(text, 3)

        self.assertTrue(bool(briefing.executive_summary))
        for section in briefing.sections:
            self.assertIsInstance(section, BriefingSection)
            self.assertTrue(bool(section.foundational_overview or section.body))
            self.assertTrue(isinstance(section.mechanical_deep_dive, list))
            self.assertTrue(isinstance(section.quick_comprehension_checks, list))
            self.assertEqual(section.comparison_analysis, [])
            self.assertEqual(section.important_rules, [])

    def test_comprehensive_fields_are_optional_for_existing_responses(self):
        section = BriefingSection(title="Compatibility")

        self.assertEqual(section.foundational_overview, "")
        self.assertEqual(section.mechanical_deep_dive, [])
        self.assertEqual(section.quick_comprehension_checks, [])

    def test_module_template_fields_are_supported(self):
        section = BriefingSection(
            title="Systematics",
            process_hierarchy=["Characterize", "Identify", "Classify"],
            comparison_analysis=[
                {"feature": "Purpose", "nomenclature": "Standardized naming", "classification": "Grouping"}
            ],
            important_rules=["Use the author citation at the end."],
        )

        self.assertEqual(section.process_hierarchy, ["Characterize", "Identify", "Classify"])
        self.assertEqual(len(section.comparison_analysis), 1)
        self.assertEqual(section.important_rules, ["Use the author citation at the end."])

    def test_large_content_is_split_into_subtopics(self):
        section = BriefingSection(
            title="Large topic",
            subtopics=[
                {"title": "First topic", "body": "First explanation"},
                {"title": "Second topic", "body": "Second explanation"},
            ],
        )

        self.assertEqual(len(section.subtopics), 2)
        self.assertEqual(section.subtopics[0].title, "First topic")


if __name__ == "__main__":
    unittest.main()
