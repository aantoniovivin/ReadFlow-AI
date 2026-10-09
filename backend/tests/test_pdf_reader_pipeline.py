import io
import os
import sys
import unittest
from pathlib import Path

import fitz
from PIL import Image, ImageDraw

BACKEND = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(BACKEND))

from extractor import extract_pdf
from ai_service import explain_term, local_briefing


def sample_pdf(kind: str) -> bytes:
    document = fitz.open()
    page = document.new_page(width=612, height=792)
    if kind == "multipage":
        page.insert_text((55, 35), "Repeated course header")
        for row in range(15):
            page.insert_text((55, 80 + row * 42), f"Page one evidence sentence {row}: energy transfer supports organisms.")
    if kind == "scan":
        image = Image.new("RGB", (1000, 1300), "white")
        ImageDraw.Draw(image).multiline_text(
            (70, 100),
            "BIOLOGY: Photosynthesis\nPlants use chlorophyll to convert sunlight, water, and carbon dioxide into glucose and oxygen.",
            fill="black", spacing=18,
        )
        stream = io.BytesIO()
        image.save(stream, format="PNG")
        page.insert_image(page.rect, stream=stream.getvalue())
    elif kind == "columns":
        for row in range(15):
            y = 55 + row * 42
            page.insert_text((50, y), f"Left column {row}: Photosynthesis occurs in chloroplasts.")
            page.insert_text((330, y), f"Right column {row}: Respiration releases energy from glucose.")
    else:
        source = (
            "Computer science: A database index speeds query processing. A B-tree organizes records for efficient retrieval."
            if kind == "technical" else
            "Biology: Photosynthesis converts sunlight into chemical energy in plants. Chlorophyll absorbs light."
        )
        for row in range(20):
            page.insert_text((55, 55 + row * 32), source, fontsize=12)
    if kind == "multipage":
        page = document.new_page(width=612, height=792)
        page.insert_text((55, 35), "Repeated course header")
        for row in range(15):
            page.insert_text((55, 80 + row * 42), f"Page two evidence sentence {row}: energy transfer supports organisms.")
    return document.tobytes()


class PdfReaderPipelineTests(unittest.TestCase):
    def test_digital_biology_and_technical_pdfs_extract_text_and_boxes(self):
        for kind, expected in (("biology", "Photosynthesis"), ("technical", "database")):
            with self.subTest(kind=kind):
                page = extract_pdf(sample_pdf(kind))["pages"][0]
                self.assertIn(expected.casefold(), page["text"].casefold())
                self.assertTrue(page["words"])
                self.assertEqual(page["number"], 1)

    def test_scanned_page_uses_ocr_when_available(self):
        page = extract_pdf(sample_pdf("scan"))["pages"][0]
        self.assertTrue(page["text"])
        self.assertTrue(page["ocr_used"])

    def test_two_column_page_preserves_both_columns_in_reading_order(self):
        text = extract_pdf(sample_pdf("columns"))["pages"][0]["text"]
        self.assertIn("Left column 0", text)
        self.assertIn("Right column 0", text)
        self.assertLess(text.index("Left column 0"), text.index("Right column 0"))

    def test_multiple_pages_keep_page_numbers_and_summaries_are_source_based(self):
        pages = extract_pdf(sample_pdf("multipage"))["pages"]
        self.assertEqual([page["number"] for page in pages], [1, 2])
        self.assertNotIn("Repeated course header", " ".join(page["text"] for page in pages))
        briefing = local_briefing("[PAGE 1]\nPhotosynthesis uses chlorophyll.\n[PAGE 2]\nLight energy becomes chemical energy.", 2)
        self.assertTrue(briefing.sections)
        self.assertTrue(all(section.source_pages_referenced for section in briefing.sections))
        self.assertFalse(any("nomenclature" in str(row).casefold() for s in briefing.sections for row in s.comparison_analysis))

    def test_contextual_definition_fallback_uses_only_given_document_context(self):
        async def run():
            previous = os.environ.get("GROQ_API_KEY")
            os.environ["GROQ_API_KEY"] = ""
            try:
                return await explain_term("index", {
                    "page": 2, "section_title": "Database structures",
                    "sentence": "A database index speeds query processing.",
                    "paragraph": "A database index speeds query processing by organizing records for efficient retrieval.",
                })
            finally:
                if previous is None:
                    os.environ.pop("GROQ_API_KEY", None)
                else:
                    os.environ["GROQ_API_KEY"] = previous
        import asyncio
        result = asyncio.run(run())
        self.assertEqual(result["page"], 2)
        self.assertTrue("index" in result["definition"].casefold() or "database" in result["definition"].casefold())
        self.assertNotIn("organizing records", result["definition"].casefold())

    def test_upload_to_term_explanation_endpoint_path(self):
        # Exercise the same extraction → local analysis → stored page context →
        # explanation route used by the API without making an external AI call.
        os.environ["GROQ_API_KEY"] = ""
        import asyncio
        import main
        from schemas import TermExplainRequest

        pages = extract_pdf(sample_pdf("technical"))["pages"]
        full_text = "\n\n".join(f"[PAGE {p['number']}]\n{p['text']}" for p in pages)
        briefing = local_briefing(full_text, len(pages))
        briefing_data = briefing.model_dump()
        database_term = next((term for term in briefing_data["terms"] if term["term"].casefold() == "database"), None)
        if database_term:
            database_term["definition"] = "A database is an organized collection of records that can be queried."
        main.DOCUMENTS["pipeline-test"] = {
            "pages_data": [{k: v for k, v in page.items() if k != "png"} for page in pages],
            "briefing": briefing_data, "term_explanation_cache": {},
        }
        try:
            result = asyncio.run(main.explain_document_term(
                "pipeline-test", TermExplainRequest(term="database", page=1, sentence="A database index speeds query processing.")
            ))
        finally:
            main.DOCUMENTS.pop("pipeline-test", None)
        self.assertEqual(result["term"], "database")
        self.assertEqual(result["page"], 1)
        self.assertTrue(len(result["definition"]) > 0)


if __name__ == "__main__":
    unittest.main()
