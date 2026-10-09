import io
import re
import unicodedata
import logging
from collections import Counter
from typing import Any

import fitz
import numpy as np
import pytesseract
from PIL import Image
from pytesseract import Output
import os
import shutil

# Automatically discover Tesseract binary across Linux, macOS, and Windows
_TESSERACT_CANDIDATES = [
    shutil.which("tesseract"),
    shutil.which("tesseract.exe"),
    "/usr/bin/tesseract",
    "/usr/local/bin/tesseract",
    "/opt/homebrew/bin/tesseract",
    r"C:\Program Files\Tesseract-OCR\tesseract.exe",
    r"C:\Program Files (x86)\Tesseract-OCR\tesseract.exe",
]
for _candidate in _TESSERACT_CANDIDATES:
    if _candidate and os.path.isfile(_candidate) and os.access(_candidate, os.X_OK):
        pytesseract.pytesseract.tesseract_cmd = _candidate
        break

logger = logging.getLogger(__name__)


def _clean_text(text: str) -> str:
    if not text:
        return ""
    text = unicodedata.normalize("NFKC", text)
    # Remove null bytes, replacement characters
    text = text.replace("\x00", " ").replace("\ufffd", " ")
    # Fix HTML entities if present
    text = text.replace("&amp;", "&").replace("&lt;", "<").replace("&gt;", ">").replace("&#39;", "'").replace("&quot;", '"')
    # Remove leading bullet characters and symbols (•, ·, ●, ○, ■, ◆, ▪, ▫, ‣, ⁃, *, -, –)
    text = re.sub(r"(?m)^[\s•·●○■◆▪▫‣⁃\u2022\u00b7\u25cf\u25cb\u25aa\u25ab\u25b8\u2043\u2219\u25c6*–—\-]+\s*", "", text)
    # Replace inline bullet symbols separating clauses with a period/space
    text = re.sub(r"\s*[•·●○■◆▪▫‣⁃\u2022\u00b7\u25cf\u25cb\u25aa\u25ab\u25b8\u2043\u2219\u25c6]\s*", ". ", text)
    # Fix broken hyphenation at line breaks or word gaps
    text = re.sub(r"(?<=\w)-\s*\n\s*(?=\w)", "", text)
    text = re.sub(r"(?<=[A-Za-z])-\s+(?=[a-z])", "", text)
    # Fix broken apostrophes/possessives with gaps (e.g. "Linnaeus ' s" -> "Linnaeus’s")
    text = re.sub(r"([A-Za-z0-9])\s*['’]\s*(s|d|ll|re|ve|m|t)\b", r"\1’\2", text, flags=re.I)
    # Fix spacing before punctuation
    text = re.sub(r"\s+([.,;:!?])", r"\1", text)
    # Fix repeated punctuation
    text = re.sub(r"\.{2,}", ".", text)
    # Fix spacing inside brackets and parentheses
    text = re.sub(r"\(\s+", "(", text)
    text = re.sub(r"\s+\)", ")", text)
    text = re.sub(r"\[\s+", "[", text)
    text = re.sub(r"\s+\]", "]", text)
    # Fix broken decimal numbers (e.g. "1 . 1" -> "1.1")
    text = re.sub(r"\b(\d+)\s*\.\s*(\d+)\b", r"\1.\2", text)
    # Fix spaced out single-letter gaps (e.g. "l i n n a e u s" -> "linnaeus")
    text = re.sub(r"\b([a-zA-Z])\s+([a-zA-Z])\s+([a-zA-Z])\s+([a-zA-Z])\b", r"\1\2\3\4", text)
    lines = [re.sub(r"\s+", " ", line).strip() for line in text.splitlines()]
    kept: list[str] = []
    for line in lines:
        if not line:
            if kept and kept[-1] != "":
                kept.append("")
            continue
        # Drop obvious OCR debris while retaining short headings and list items.
        alnum = sum(ch.isalnum() for ch in line)
        if len(line) > 3 and alnum / len(line) < 0.35:
            continue
        if kept and line.casefold() == kept[-1].casefold():
            continue
        kept.append(line)
    return "\n".join(kept).strip()


def _digital_page(page: fitz.Page) -> tuple[str, list[dict[str, Any]]]:
    rect = page.rect
    blocks = [b for b in page.get_text("blocks") if len(b) > 4 and str(b[4]).strip()]
    page_width = max(1.0, rect.width)
    ordered = sorted(blocks, key=lambda b: (b[1], b[0]))

    # Switch to column reading only when the page really has two narrow text
    # columns. A large gap between block centers alone can mistake a centered
    # heading or a normal single-column page for a column break.
    centers = sorted((float(block[0]) + float(block[2])) / 2 for block in blocks)
    gaps = [(right - left, (left + right) / 2) for left, right in zip(centers, centers[1:])]
    if gaps:
        gap, split = max(gaps)
        left_column = [b for b in blocks if (b[0] + b[2]) / 2 < split and b[2] - b[0] <= page_width * 0.52]
        right_column = [b for b in blocks if (b[0] + b[2]) / 2 >= split and b[2] - b[0] <= page_width * 0.52]
        spans_body = any(
            b[1] > rect.height * 0.12 and b[3] < rect.height * 0.88 and b[2] - b[0] > page_width * 0.58
            for b in blocks
        )
        if gap > page_width * 0.12 and len(left_column) >= 2 and len(right_column) >= 2 and not spans_body:
            top_blocks = [b for b in blocks if b[3] <= min(x[1] for x in left_column + right_column)]
            bottom_blocks = [b for b in blocks if b[1] >= max(x[3] for x in left_column + right_column)]
            ordered = (
                sorted(top_blocks, key=lambda b: (b[1], b[0]))
                + sorted(left_column, key=lambda b: (b[1], b[0]))
                + sorted(right_column, key=lambda b: (b[1], b[0]))
                + sorted(bottom_blocks, key=lambda b: (b[1], b[0]))
            )
    text_parts = []
    words_out = []
    # PyMuPDF's word records include the source block number. Index once so
    # pages with many words do not rescan the full word list for every block.
    words_by_block: dict[int, list[tuple]] = {}
    for word in page.get_text("words"):
        words_by_block.setdefault(int(word[5]), []).append(word)
    for block in ordered:
        x0, y0, x1, y1, raw = block[:5]
        clean = _clean_text(str(raw))
        if clean:
            text_parts.append(clean)
        block_words = words_by_block.get(int(block[5]), ()) if len(block) > 5 else ()
        for word in block_words:
            wx0, wy0, wx1, wy1, token = word[:5]
            words_out.append({"text": token, "x": wx0 / rect.width, "y": wy0 / rect.height,
                              "width": (wx1 - wx0) / rect.width, "height": (wy1 - wy0) / rect.height})
    return "\n\n".join(text_parts), words_out


def _ocr_page(page: fitz.Page) -> tuple[str, list[dict[str, Any]], float]:
    rect = page.rect
    # 1. Primary Engine: Pytesseract with high-res preprocessed grayscale image
    try:
        pix = page.get_pixmap(matrix=fitz.Matrix(2, 2), alpha=False)
        image = Image.open(io.BytesIO(pix.tobytes("png"))).convert("RGB")
        rgb = np.asarray(image)
        gray = (0.299 * rgb[..., 0] + 0.587 * rgb[..., 1] + 0.114 * rgb[..., 2]).astype("uint8")
        data = pytesseract.image_to_data(gray, output_type=Output.DICT, config="--psm 3", timeout=30)
        lines: dict[tuple[int, int, int], list[str]] = {}
        words: list[dict[str, Any]] = []
        confidences = []
        for i, token in enumerate(data["text"]):
            token = token.strip()
            try:
                confidence = float(data["conf"][i])
            except (ValueError, TypeError):
                confidence = -1
            if not token or confidence < 0:
                continue
            line_key = (int(data["block_num"][i]), int(data["par_num"][i]), int(data["line_num"][i]))
            lines.setdefault(line_key, []).append(token)
            confidences.append(confidence)
            words.append({"text": token, "x": data["left"][i] / pix.width, "y": data["top"][i] / pix.height,
                          "width": data["width"][i] / pix.width, "height": data["height"][i] / pix.height,
                          "confidence": confidence})
        ocr_text = "\n".join(" ".join(tokens) for tokens in lines.values())
        if ocr_text.strip():
            return _clean_text(ocr_text), words, (sum(confidences) / len(confidences) if confidences else 0.0)
    except Exception as exc:
        logger.warning("Pytesseract OCR encountered an issue: %s. Trying PyMuPDF OCR fallback.", exc)

    # 2. Secondary Fallback Engine: PyMuPDF native OCR textpage
    try:
        tp = page.get_textpage_ocr(flags=fitz.TEXT_PRESERVE_WHITESPACE, dpi=150, full=True)
        fallback_text = page.get_text("text", textpage=tp)
        raw_words = page.get_text("words", textpage=tp)
        fallback_words = []
        for w in raw_words:
            wx0, wy0, wx1, wy1, token = w[:5]
            fallback_words.append({
                "text": token,
                "x": wx0 / rect.width,
                "y": wy0 / rect.height,
                "width": (wx1 - wx0) / rect.width,
                "height": (wy1 - wy0) / rect.height,
                "confidence": 80.0
            })
        if fallback_text.strip():
            return _clean_text(fallback_text), fallback_words, 80.0
    except Exception as exc:
        logger.warning("PyMuPDF OCR fallback encountered an issue: %s", exc)

    return "", [], 0.0


def _quality(text: str) -> float:
    words = re.findall(r"[\w'-]+", text)
    if not words:
        return 0
    plausible = sum(bool(re.search(r"[aeiouy]", w, re.I)) or len(w) <= 2 or w.isupper() for w in words)
    return min(len(words), 200) + 2 * plausible - max(0, len(re.findall(r"[^\w\s.,;:!?()'\"%-]", text)) - 4)


def _needs_ocr(text: str) -> bool:
    words = re.findall(r"[\w'-]+", text)
    if len(words) < 24 or len(re.sub(r"\s", "", text)) < 140:
        return True
    if not words:
        return True
    letters = sum(character.isalpha() for character in text)
    useful_words = sum(bool(re.search(r"[A-Za-z]{2,}", word)) for word in words)
    unusual = len(re.findall(r"[^\w\s.,;:!?()'\"/%&+–—-]", text))
    return useful_words / len(words) < 0.42 or letters / max(1, len(text)) < 0.35 or unusual / max(1, len(text)) > 0.08


def _remove_repeated_margins(pages: list[dict[str, Any]]) -> None:
    counts: Counter[str] = Counter()
    for page in pages:
        lines = [line.strip() for line in page["text"].splitlines() if line.strip()]
        edge = lines[:2] + lines[-2:]
        normalized = [re.sub(r"\d+", "#", re.sub(r"\s+", " ", line.casefold())).strip() for line in edge]
        counts.update(set(normalized))
    threshold = max(2, int(len(pages) * 0.5))
    repeated = {line for line, count in counts.items() if count >= threshold and len(line) >= 4}
    for page in pages:
        lines = page["text"].splitlines()
        cleaned = []
        for idx, line in enumerate(lines):
            normalized = re.sub(r"\d+", "#", re.sub(r"\s+", " ", line.casefold())).strip()
            at_edge = idx < 3 or idx >= len(lines) - 3
            if at_edge and normalized in repeated:
                continue
            cleaned.append(line)
        page["text"] = "\n".join(cleaned).strip()


def extract_pdf(data: bytes) -> dict[str, Any]:
    doc = fitz.open(stream=data, filetype="pdf")
    if doc.is_encrypted:
        raise ValueError("Password-protected PDFs are not supported.")
    pages: list[dict[str, Any]] = []
    try:
        for i, page in enumerate(doc):
            rect = page.rect
            text, words = _digital_page(page)
            ocr_used = False
            ocr_confidence = None
            if _needs_ocr(text):
                try:
                    ocr_text, ocr_words, ocr_confidence = _ocr_page(page)
                    if _quality(ocr_text) > _quality(text) * 1.12:
                        text, words, ocr_used = ocr_text, ocr_words, True
                except Exception as exc:
                    logger.warning("OCR skipped on page %d due to: %s", i + 1, exc)
            render = page.get_pixmap(matrix=fitz.Matrix(1.65, 1.65), alpha=False)
            pages.append({"number": i + 1, "width": rect.width, "height": rect.height,
                          "text": _clean_text(text), "words": words, "ocr_used": ocr_used,
                          "ocr_confidence": ocr_confidence, "png": render.tobytes("png")})
        _remove_repeated_margins(pages)
        # Verify if all pages ended up with 0 readable text
        total_text = "".join(p["text"] for p in pages).strip()
        if not total_text:
            raise RuntimeError(
                "Could not extract any readable text from this document. "
                "If this is a scanned document, please ensure Tesseract OCR is installed (`sudo apt-get install -y tesseract-ocr`)."
            )
    finally:
        doc.close()
    return {"pages": pages}


def extract_docx(data: bytes) -> dict[str, Any]:
    """Extract paragraphs and tables from a Word (.docx/.doc) file and render formatted pages."""
    import zipfile
    import xml.etree.ElementTree as ET

    paragraphs: list[str] = []

    # 1. Standard modern .docx (ZIP archive containing XML)
    if zipfile.is_zipfile(io.BytesIO(data)) or data.startswith(b"PK\x03\x04"):
        try:
            with zipfile.ZipFile(io.BytesIO(data)) as zf:
                names = zf.namelist()
                xml_targets = [n for n in names if n.startswith("word/") and n.endswith(".xml")]
                doc_xmls = [n for n in xml_targets if "document" in n]
                other_xmls = [n for n in xml_targets if n not in doc_xmls]
                ordered_xmls = doc_xmls + other_xmls

                for xml_name in ordered_xmls:
                    try:
                        xml_content = zf.read(xml_name)
                        tree = ET.fromstring(xml_content)
                        for elem in tree.iter():
                            if elem.tag.endswith("p"):
                                texts = [node.text for node in elem.iter() if node.tag.endswith("t") and node.text]
                                if texts:
                                    full_p = "".join(texts).strip()
                                    if full_p and len(full_p) >= 2:
                                        paragraphs.append(full_p)
                            elif elem.tag.endswith("tbl"):
                                for tr in elem.iter():
                                    if tr.tag.endswith("tr"):
                                        cell_texts = []
                                        for tc in tr.iter():
                                            if tc.tag.endswith("tc"):
                                                t_list = [node.text for node in tc.iter() if node.tag.endswith("t") and node.text]
                                                c_txt = "".join(t_list).strip()
                                                if c_txt:
                                                    cell_texts.append(c_txt)
                                        if cell_texts:
                                            paragraphs.append(" • ".join(cell_texts))
                    except Exception as parse_err:
                        logger.debug("Skipping non-parsable xml element in %s: %s", xml_name, parse_err)
        except Exception as exc:
            logger.warning("DOCX zip parsing encountered issue: %s", exc)

    # 2. Legacy binary .doc (OLE2 Compound Document) or raw stream fallback
    if not paragraphs:
        raw_text = ""
        try:
            utf16_matches = re.findall(r"[\u0020-\u007E\u00A0-\u00FF\n\r\t]{4,}", data.decode("utf-16-le", errors="ignore"))
            if utf16_matches:
                raw_text = "\n".join(utf16_matches)
        except Exception:
            pass
        if not raw_text or len(raw_text.split()) < 10:
            ascii_matches = re.findall(r"[A-Za-z0-9 ,.;:!?'\"()\-–—\n\r\t]{4,}", data.decode("latin-1", errors="ignore"))
            raw_text = "\n".join(ascii_matches)

        for line in raw_text.splitlines():
            line = line.strip()
            if len(line.split()) >= 2:
                paragraphs.append(line)

    if not paragraphs:
        raise ValueError("The uploaded Word document does not contain any readable text.")

    # Paginate paragraphs into clean A4 document pages in memory
    doc = fitz.open()
    page_paragraphs: list[list[str]] = []
    current_page: list[str] = []
    current_word_count = 0

    for p in paragraphs:
        wcount = len(p.split())
        if current_word_count + wcount > 300 and current_page:
            page_paragraphs.append(current_page)
            current_page = [p]
            current_word_count = wcount
        else:
            current_page.append(p)
            current_word_count += wcount

    if current_page:
        page_paragraphs.append(current_page)

    for p_list in page_paragraphs:
        page = doc.new_page(width=595, height=842)
        text_content = "\n\n".join(p_list)
        rect = fitz.Rect(48, 52, 547, 790)
        rc = page.insert_textbox(rect, text_content, fontsize=11, fontname="helv", color=(0.15, 0.20, 0.25))
        if rc < 0:
            page.insert_textbox(rect, text_content, fontsize=9, fontname="helv", color=(0.15, 0.20, 0.25))

    pdf_bytes = doc.tobytes()
    doc.close()
    return extract_pdf(pdf_bytes)


def extract_txt(data: bytes) -> dict[str, Any]:
    """Extract text from plain text file and render formatted pages."""
    text = data.decode("utf-8", errors="replace")
    paragraphs = [p.strip() for p in text.split("\n\n") if p.strip()]
    if not paragraphs:
        paragraphs = [text.strip()] if text.strip() else ["(Empty text document)"]

    doc = fitz.open()
    page_paragraphs: list[list[str]] = []
    current_page: list[str] = []
    current_word_count = 0

    for p in paragraphs:
        wcount = len(p.split())
        if current_word_count + wcount > 340 and current_page:
            page_paragraphs.append(current_page)
            current_page = [p]
            current_word_count = wcount
        else:
            current_page.append(p)
            current_word_count += wcount

    if current_page:
        page_paragraphs.append(current_page)

    for p_list in page_paragraphs:
        page = doc.new_page(width=595, height=842)
        text_content = "\n\n".join(p_list)
        rect = fitz.Rect(48, 52, 547, 790)
        page.insert_textbox(rect, text_content, fontsize=11, fontname="helv", color=(0.15, 0.20, 0.25))

    pdf_bytes = doc.tobytes()
    doc.close()
    return extract_pdf(pdf_bytes)

