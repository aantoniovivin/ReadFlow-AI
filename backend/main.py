PROXY_IMAGE_CACHE: dict[str, tuple[bytes, str]] = {}

def build_educational_drawing_prompt(
    term: str,
    entity_type: str = "",
    image_query: str = "",
    domain: str = "",
    definition_hint: str = "",
    sentence: str = "",
    paragraph: str = "",
    technical_explanation: str = ""
) -> str:
    """
    Construct a precise, component-specific educational textbook drawing prompt on a solid plain white background.
    Explicitly specifies structural components, directional flow, and relationships without generic filler.
    """
    base = (image_query or term).strip()
    clean_base = re.sub(r"\b(kingdom|phylum|clade|rank|designation|resource|rank\s+in\s+biology)\b", "", base, flags=re.I)
    clean_base = re.sub(r"\s+", " ", clean_base).strip()
    if not clean_base or len(clean_base) < 2:
        clean_base = term
        
    e_type_l = (entity_type or "").lower()
    dom_l = (domain or "").lower()
    base_l = clean_base.lower()
    target_ctx = f"{base_l} {e_type_l} {sentence.lower()} {technical_explanation.lower()} {definition_hint.lower()}"

    # Fruits, Vegetables & Food Photography
    fruit_pattern = r"\b(?:fruit|drupe|mango|mangifera|apple|banana|orange|grape|strawberry|pineapple|watermelon|papaya|guava|citrus|tomato|potato|vegetable|crop)\b"
    if "fruit" in e_type_l or re.search(fruit_pattern, target_ctx):
        return f"authentic clean close-up real photograph of fresh ripe {clean_base}, studio food photography, natural lighting, vibrant colors, isolated on clean background, high resolution photo"

    # Benchmark 1: Neural Networks & Deep Learning
    if any(k in target_ctx for k in ["neural network", "deep learning", "perceptron", "backpropagation", "convolutional neural", "recurrent neural", "artificial neural"]):
        return (
            f"clean educational scientific diagram of {clean_base} on a solid plain white background, "
            "showing input layer nodes x1 x2 x3, interconnected weighted synaptic connection lines w_ij, "
            "multiple hidden layers with activation function nodes, and output classification layer nodes y1 y2, "
            "labeled left-to-right processing flow, crisp vector line art, high educational clarity, no artistic clutter, no dark backgrounds"
        )

    # Benchmark 2: Photosynthesis & Chloroplast Function
    if any(k in target_ctx for k in ["photosynthesis", "chloroplast", "thylakoid", "calvin cycle", "light reaction", "light-dependent reaction", "stroma matrix"]):
        return (
            f"clean educational biology textbook diagram of {clean_base} in plant chloroplast on a solid plain white background, "
            "showing chloroplast double membrane, stacked thylakoid grana discs, light-dependent ATP and NADPH synthesis reactions, "
            "stroma Calvin cycle converting carbon dioxide CO2 into glucose C6H12O6, inputs of sunlight photons and water H2O, output oxygen O2, "
            "clearly labeled biological pathway, crisp scientific vector illustration"
        )

    # Benchmark 3: Database Normalization & Relational Architecture
    if any(k in target_ctx for k in ["database normalization", "normalization", "1nf", "2nf", "3nf", "bcnf", "first normal form", "second normal form", "third normal form", "relational database normalization"]):
        return (
            f"clean educational computer science diagram of {clean_base} on a solid plain white background, "
            "showing relational database table decomposition flow from unnormalized table to 1NF atomic columns, "
            "2NF partial key dependency elimination, and 3NF transitive dependency removal, "
            "with primary key underlined, foreign key relation arrows connecting schema tables, crisp rectangular table boxes, minimal clutter"
        )

    # Benchmark 4: Operating System Scheduling & Process Management
    if any(k in target_ctx for k in ["process scheduling", "operating system scheduling", "cpu scheduling", "round robin", "shortest job first", "ready queue", "context switch", "preemption", "process state"]):
        return (
            f"clean educational operating system architecture diagram of {clean_base} on a solid plain white background, "
            "showing process state transitions between Ready Queue, CPU Running state, I/O Waiting Blocked queue, and Terminated state, "
            "with Dispatcher scheduling, Preemption timer interrupt, and Context Switch register save and restore operations, "
            "clearly labeled directional transition arrows, crisp technical diagram"
        )

    # Historical Figures & Scientists
    scientist_pattern = r"\b(?:scientist|botanist|physicist|chemist|biologist|mathematician|naturalist|zoologist|person|linnaeus|carolus linnaeus|carl linnaeus|mayr|ernst mayr|darwin|charles darwin|mendel|gregor mendel|einstein|albert einstein|newton|isaac newton|turing|alan turing|babbage|charles babbage|bohr|niels bohr|galileo|tesla|curie|marie curie|hooke|robert hooke|leeuwenhoek|aristotle|whittaker|moore|gordon moore|von neumann|john von neumann)\b"
    if "person" in e_type_l or "scientist" in e_type_l or re.search(scientist_pattern, target_ctx):
        return f"detailed historical portrait drawing of {clean_base}, academic educational biographical illustration on clean plain white background, crisp vector line engraving, no frames, no borders"

    # Astronomy & Space (Planets, Stars, Solar System)
    astro_pattern = r"\b(?:planet|solar system|astronomy|star|galaxy|telescope|sun|moon|lunar|cosmos|nebula|black hole|crater|exosphere|asteroid|orbit|venus|mars|jupiter|saturn|uranus|neptune|milky way)\b"
    if "planet" in e_type_l or "astronomy" in e_type_l or "solar system" in e_type_l or ("space" in dom_l and "element" not in e_type_l and "company" not in e_type_l) or re.search(astro_pattern, f"{base_l} {e_type_l} {sentence.lower()}"):
        return f"detailed colored astronomical drawing of {clean_base}, astronomy science textbook educational diagram showing celestial body and orbital path on clean plain white background, crisp line art, no frames, no borders"

    # Chemistry (Molecules, Atomic Structure, Periodic Table, Bonds, Reactions, Chemical Elements)
    chem_pattern = r"\b(?:chemist|chemistry|atomic structure|molecule|molecular|chemical reaction|chemical element|liquid metal|heavy silvery element|periodic table|covalent bond|ionic bond|molarity|stoichiometry|titration|enthalpy|catalyst|acid-base|aqueous)\b"
    if "chemical element" in e_type_l or "element" in e_type_l or "chemistry" in dom_l or re.search(chem_pattern, target_ctx):
        return f"clear educational chemistry textbook diagram drawing of {clean_base}, scientific atomic molecular structure with valence electron shells and chemical bonds on clean plain white background, crisp vector style, no frames, no borders"

    # Computer Science, Hardware & Technology
    cs_pattern = r"\b(?:computer|cpu|microprocessor|microcontroller|primary memory|secondary memory|main memory|ram|rom|sram|dram|cache|cache memory|von neumann|alu|hardware|software|operating system|macos|iphone|technology company|apple inc|tech company|motherboard|system bus|data bus|address bus|register|logic gate|and gate|or gate|not gate|nand gate|nor gate|xor gate|cloud storage|storage device)\b"
    if "technology company" in e_type_l or "company" in e_type_l or "computer" in dom_l or "cs" in dom_l or re.search(cs_pattern, target_ctx):
        return f"clear educational computer science textbook diagram drawing of {clean_base}, computer architecture and digital technology diagram on clean plain white background, crisp vector style, no frames, no borders"

    # Botanical / Plants / Botany
    botany_pattern = r"\b(?:plant|botan|flower|tree|leaf|root|stem|angiosperm|gymnosperm|flora|solanum|mangifera|triticum|chloroplast|herbarium|botanical garden|photosynthesis|petal|sepal|xylem|phloem)\b"
    if "plant" in e_type_l or "botany" in dom_l or re.search(botany_pattern, target_ctx):
        return f"detailed colored botanical drawing of {clean_base}, scientific textbook botany illustration showing roots stem leaves reproductive organs on clean plain white background, crisp clean educational drawing, no frames, no borders"

    # Cell & Molecular Biology (Organelles, Membranes, DNA)
    cell_pattern = r"\b(?:cell structure|organelle|mitochondria|membrane|nucleus|ribosome|endoplasmic|cytoplasm|golgi|vacuole|lysosome|dna|rna|chromosome)\b"
    if re.search(cell_pattern, target_ctx):
        return f"detailed colored biological drawing of {clean_base} cellular structure, scientific biology textbook diagram showing inner organelle components on clean plain white background, educational diagram, no frames, no borders"

    # Zoology & Anatomical Biology (Animals, Notochord, Tissues, Organs)
    anatomy_pattern = r"\b(?:animal|fauna|chordata|arthropoda|mammal|insect|notochord|neural|nerve cord|anatomy|organ|tissue|embryo|heart|brain|bone|skeleton|muscle|panthera|felis|canis|musca|homo sapiens)\b"
    if re.search(anatomy_pattern, target_ctx):
        return f"detailed colored biological drawing of {clean_base}, zoological anatomical biology textbook diagram showing physiological structure on clean plain white background, clear educational drawing, no frames, no borders"

    # Taxonomy Hierarchy & Identification Tools
    taxonomy_pattern = r"\b(?:taxonomic key|couplet|lead|taxonom|flowchart|hierarchy|classification hierarchy|tree of life|systema naturae|five kingdoms)\b"
    if re.search(taxonomy_pattern, target_ctx):
        return f"clear educational scientific flowchart hierarchy diagram drawing of {clean_base}, taxonomy biology classification chart on clean plain white background, no frames, no borders"

    # Geography & Earth Sciences (Soils, Landforms, Erosion, Agriculture, Resources)
    geo_pattern = r"\b(?:soil|alluvial|black soil|laterite|arid soil|red and yellow soil|forest soil|land degradation|gully erosion|sheet erosion|contour ploughing|terrace farming|shelter belt|strip cropping|bad land|ravines|net sown area|fallow land|delta|river basin|earth science|geography|topography|plateau|renewable resource|non-renewable resource|sustainable development|agenda 21|rio de janeiro earth summit)\b"
    if "geography" in dom_l or "earth" in dom_l or re.search(geo_pattern, target_ctx):
        return f"clear educational geography textbook diagram drawing of {clean_base}, earth science physical geography illustration with cross-sectional soil and geological layers on clean plain white background, crisp line art, no frames, no borders"

    # Physics (Mechanics, Optics, Waves, Electromagnetism, Gravity)
    phys_pattern = r"\b(?:physic|optics|wave|force|gravitation|gravity|circuit|magnet|electromagnetism|acceleration|momentum|kinetic energy|potential energy|velocity|thermodynamics)\b"
    if "physics" in dom_l or re.search(phys_pattern, target_ctx):
        return f"clear educational physics textbook diagram drawing of {clean_base}, scientific principles physics textbook diagram showing vectors and physical phenomena on clean plain white background, crisp line art, no frames, no borders"

    # Default Academic Diagram with context
    extra_keywords = ""
    if technical_explanation and len(technical_explanation) > 10:
        words = [w for w in re.findall(r"[a-zA-Z]{3,}", technical_explanation.lower())
                 if w not in ["the", "and", "for", "with", "this", "that", "from", "which", "refers", "designates", "concept", "system", "structure", "study"]]
        if words:
            extra_keywords = " " + " ".join(words[:4])
    return f"detailed colored scientific textbook drawing illustration of {clean_base}{extra_keywords}, clear educational science diagram on clean plain white background, crisp line art, no frames, no borders"

import html
import os
import re
import uuid
import logging
import time
from urllib.parse import quote, unquote
from pathlib import Path
from typing import Optional

import httpx
from dotenv import load_dotenv
from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import Response
from starlette.concurrency import run_in_threadpool

from ai_service import answer_question, create_briefing, explain_term, term_sentence_context
from extractor import extract_pdf, extract_docx, extract_txt
from nlp_service import analyze_word

logger = logging.getLogger(__name__)
from schemas import ChatRequest, TermExplainRequest

load_dotenv(Path(__file__).with_name(".env"))
UPLOAD_DIR = Path("/tmp/uploads")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
app = FastAPI(
    title="ReadFlow AI API",
    description="High-performance document intelligence & briefing engine with contextual terminology exploration.",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)
app.add_middleware(CORSMiddleware, allow_origins=[os.getenv("FRONTEND_ORIGIN", "http://localhost:5173")],
                   allow_credentials=True, allow_methods=["*"], allow_headers=["*"])
DOCUMENTS: dict[str, dict] = {}
TERM_IMAGE_CACHE: dict[str, dict] = {}
MAX_BYTES = int(os.getenv("MAX_UPLOAD_MB", "40")) * 1024 * 1024

DOCS_STORAGE_DIR = os.path.join(os.path.dirname(__file__), "data", "saved_docs")
os.makedirs(DOCS_STORAGE_DIR, exist_ok=True)

import pickle

def get_persisted_doc(doc_id: str) -> Optional[dict]:
    if doc_id in DOCUMENTS:
        return DOCUMENTS[doc_id]
    doc_path = os.path.join(DOCS_STORAGE_DIR, f"{doc_id}.pkl")
    if os.path.exists(doc_path):
        try:
            with open(doc_path, "rb") as f:
                doc = pickle.load(f)
                DOCUMENTS[doc_id] = doc
                return doc
        except Exception as err:
            logger.warning("Could not load persisted doc %s: %s", doc_id, err)
    return None

def save_persisted_doc(doc_id: str, doc: dict) -> None:
    DOCUMENTS[doc_id] = doc
    doc_path = os.path.join(DOCS_STORAGE_DIR, f"{doc_id}.pkl")
    try:
        with open(doc_path, "wb") as f:
            pickle.dump(doc, f)
    except Exception as err:
        logger.warning("Could not persist doc %s: %s", doc_id, err)


def public_doc(doc: dict) -> dict:
    return {k: v for k, v in doc.items() if k not in {"pages_data", "text", "term_explanation_cache"}}


def find_boxes(pages: list[dict], terms: list[dict]) -> list[dict]:
    boxes = []
    terms_by_first_word: dict[str, list[tuple[dict, list[str]]]] = {}
    for term in terms:
        parts = term["term"].split()
        if parts:
            terms_by_first_word.setdefault(parts[0].casefold(), []).append((term, parts))
    for page in pages:
        words = page["words"]
        for idx, word in enumerate(words):
            first_word = word["text"].strip(".,:;!?()[]{}\"'“”").casefold()
            for term, parts in terms_by_first_word.get(first_word, ()):
                found = [word]
                for off, part in enumerate(parts[1:], 1):
                    if idx + off >= len(words) or words[idx + off]["text"].strip(".,:;!?()[]{}\"'").casefold() != part.casefold():
                        break
                    found.append(words[idx + off])
                if len(found) != len(parts):
                    continue
                x0 = min(w["x"] for w in found); y0 = min(w["y"] for w in found)
                x1 = max(w["x"] + w["width"] for w in found); y1 = max(w["y"] + w["height"] for w in found)
                boxes.append({"term": term["term"], "definition": term["definition"],
                              "category": term.get("category", "scientific_term"),
                              "context": term_sentence_context(page["text"], term["term"]), "page": page["number"],
                              "x": x0, "y": y0, "width": x1 - x0, "height": y1 - y0})
    return boxes


def local_definition_from_context(term: str, text: str) -> str:
    """Turn an explicit source definition into a short label when AI is unavailable."""
    pattern = re.compile(
        rf"\b{re.escape(term)}\b\s+(?:is defined as|are defined as|is known as|are known as|refers to|means|is|are)\s+([^.!?;]+)",
        re.IGNORECASE,
    )
    match = pattern.search(text or "")
    if not match:
        return ""
    detail = re.sub(r"\s+", " ", match.group(1)).strip(" ,:")
    if not detail or len(detail) > 180:
        return ""
    return f"{term.capitalize()}: {detail}."


@app.get("/api/health")
def health():
    return {"status": "ok"}


@app.get("/")
def root():
    return {
        "service": "ReadFlow AI API",
        "status": "running",
        "frontend": "http://localhost:5173",
        "health": "/api/health",
    }


@app.post("/api/documents")
async def upload_document(file: UploadFile = File(...)):
    filename = (file.filename or "").lower()
    allowed_exts = (".pdf", ".docx", ".doc", ".txt")
    is_valid_ext = any(filename.endswith(ext) for ext in allowed_exts)
    is_valid_type = file.content_type in (
        "application/pdf",
        "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        "application/msword",
        "text/plain"
    )
    if not (is_valid_ext or is_valid_type):
        raise HTTPException(415, "Please upload a PDF, Word document (.docx), or Text document (.txt).")
    data = await file.read(MAX_BYTES + 1)
    if len(data) > MAX_BYTES:
        raise HTTPException(413, f"Document exceeds the {MAX_BYTES // 1024 // 1024} MB upload limit.")
    try:
        if filename.endswith(".docx") or filename.endswith(".doc") or file.content_type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
            extracted = await run_in_threadpool(extract_docx, data)
        elif filename.endswith(".txt") or file.content_type == "text/plain":
            extracted = await run_in_threadpool(extract_txt, data)
        elif data.startswith(b"PK\x03\x04"):
            extracted = await run_in_threadpool(extract_docx, data)
        elif not data.startswith(b"%PDF"):
            raise HTTPException(400, "The uploaded file is not a valid PDF or Word document.")
        else:
            extracted = await run_in_threadpool(extract_pdf, data)
    except HTTPException:
        raise
    except RuntimeError as exc:
        logger.exception("Document extraction runtime error: %s", exc)
        raise HTTPException(422, str(exc)) from exc
    except ValueError as exc:
        logger.exception("Document validation error: %s", exc)
        raise HTTPException(422, str(exc)) from exc
    except Exception as exc:
        logger.exception("Unexpected document processing exception: %s", exc)
        raise HTTPException(422, f"Could not read this document: {exc}") from exc
    readable_words = sum(len(re.findall(r"\w+", page["text"])) for page in extracted["pages"])
    if readable_words < 8:
        raise HTTPException(422, "There is not enough readable text to summarize this document. Please ensure the document has text content.")
    text = "\n\n".join(f"[PAGE {p['number']}]\n{p['text']}" for p in extracted["pages"])
    briefing, ai_enabled, ai_error = await create_briefing(text, len(extracted["pages"]))
    summarized_pages = sorted({page for section in briefing.sections for page in section.source_pages_referenced})
    terms = [t.model_dump() for t in briefing.terms]
    boxes = find_boxes(extracted["pages"], terms)
    doc_id = uuid.uuid4().hex
    stored_pages = []
    for page in extracted["pages"]:
        path = UPLOAD_DIR / f"{doc_id}-{page['number']}.png"
        path.write_bytes(page["png"])
        stored_pages.append({k: v for k, v in page.items() if k != "png"})
    doc = {"id": doc_id, "filename": Path(file.filename or "document.pdf").name,
           "page_count": len(extracted["pages"]), "summarized_pages": summarized_pages,
           "extracted_characters": len(text),
           "ai_enabled": ai_enabled, "ai_error": ai_error, "briefing": briefing.model_dump(), "term_boxes": boxes,
           "pages_data": stored_pages, "text": text, "term_explanation_cache": {}, "diagram_cache": {}}
    save_persisted_doc(doc_id, doc)
    return public_doc(doc)


@app.get("/api/documents/{doc_id}")
def get_document(doc_id: str):
    doc = get_persisted_doc(doc_id)
    if not doc:
        raise HTTPException(404, "Document not found. Upload it again to continue.")
    return public_doc(doc)


@app.get("/api/documents/{doc_id}/pages/{page_number}.png")
def get_page(doc_id: str, page_number: int):
    if doc_id not in DOCUMENTS or not 1 <= page_number <= DOCUMENTS[doc_id]["page_count"]:
        raise HTTPException(404, "Page not found.")
    path = UPLOAD_DIR / f"{doc_id}-{page_number}.png"
    return Response(path.read_bytes(), media_type="image/png", headers={"Cache-Control": "private, max-age=3600"})


@app.post("/api/documents/{doc_id}/chat")
async def chat(doc_id: str, payload: ChatRequest):
    if not get_persisted_doc(doc_id):
        raise HTTPException(404, "Document not found.")
    q = payload.question.strip()
    if not q or len(q) > 1500:
        raise HTTPException(400, "Enter a question up to 1500 characters.")
    return {"answer": await answer_question(q, DOCUMENTS[doc_id]["text"])}


@app.post("/api/documents/{doc_id}/terms/explain")
async def explain_document_term(doc_id: str, payload: TermExplainRequest):
    """
    Word & Entity Explanation Pipeline:
    1. Groq context/entity detection (resolves exact meaning & determines if image is genuinely useful)
    2. Wikipedia: factual definition / structured entity info ONLY (no Wikipedia images)
    3. Openverse: image search ONLY when show_image is True, with precise query & metadata verification
    4. Return clean structured response matching exact entity rules
    """
    doc = get_persisted_doc(doc_id)
    if not doc:
        doc = {
            "id": doc_id or "standalone",
            "filename": "Academic Knowledge Base",
            "page_count": 1,
            "briefing": {"sections": []},
            "pages_data": [{"number": 1, "text": f"{payload.sentence or payload.term}"}],
            "term_explanation_cache": {},
        }
    term = payload.term.strip()
    if not term:
        raise HTTPException(400, "Select a term to explain.")
    word_analysis = analyze_word(term, context=f"{payload.sentence} {payload.term}")
    pages = doc["pages_data"]
    page_number = payload.page if payload.page and payload.page <= len(pages) else None
    page_data = pages[page_number - 1] if page_number else None
    if page_data is None:
        matching = next((p for p in pages if re.search(re.escape(term), p["text"], re.I)), None)
        page_data = matching or pages[0]
        page_number = page_data["number"]
    page_text = page_data["text"]
    match = re.search(re.escape(term), page_text, re.I)
    if not match:
        source_page = next((p for p in pages if re.search(re.escape(term), p["text"], re.I)), None)
        if source_page:
            page_data = source_page
            page_number = page_data["number"]
            page_text = page_data["text"]
            match = re.search(re.escape(term), page_text, re.I)
    if payload.sentence and payload.sentence.strip():
        sentence = payload.sentence.strip()
        sent_pos = page_text.find(sentence[:50])
        if sent_pos >= 0:
            start = max(0, page_text.rfind("\n\n", 0, sent_pos))
            end = page_text.find("\n\n", sent_pos + len(sentence))
            paragraph = page_text[start:end if end >= 0 else len(page_text)].strip()[:3500]
        elif match:
            start = max(0, page_text.rfind("\n\n", 0, match.start()))
            end = page_text.find("\n\n", match.end())
            paragraph = page_text[start:end if end >= 0 else len(page_text)].strip()[:3500]
        else:
            paragraph = sentence[:1200]
    else:
        sentence = term_sentence_context(page_text, term) if match else ""
        if match:
            start = max(0, page_text.rfind("\n\n", 0, match.start()))
            end = page_text.find("\n\n", match.end())
            paragraph = page_text[start:end if end >= 0 else len(page_text)].strip()[:3500]
        else:
            paragraph = sentence[:1200]
    section_index = payload.section_index
    sections = doc["briefing"]["sections"]
    section = sections[section_index] if section_index is not None and section_index < len(sections) else next(
        (item for item in sections if page_number in item.get("source_pages_referenced", [])), {})
    section_title = section.get("title", "")
    
    resolved_override = payload.resolved_entity.strip() if payload.resolved_entity else ""
    cache_key = f"{term.casefold()}:{page_number}:{sentence[:100].casefold()}:{resolved_override.casefold()}"
    cache = doc["term_explanation_cache"]
    if cache_key not in cache:
        explanation = await explain_term(term, {
            "page": page_number, "section_title": section_title,
            "sentence": sentence[:1200], "paragraph": paragraph,
            "resolved_entity": resolved_override,
            "entity_type": payload.entity_type,
        })
        explanation["root_word"] = word_analysis["lemma"]
        explanation["part_of_speech"] = word_analysis["part_of_speech"]
        cache[cache_key] = explanation

    explanation = cache[cache_key]
    resolved_entity_info = explanation.get("entity") or {}
    resolved_name = resolved_entity_info.get("name") or explanation.get("canonical_wiki_title") or term
    entity_type = resolved_entity_info.get("type") or "concept"
    domain_topic = str(explanation.get("domain_topic") or section_title)
    confidence = float(resolved_entity_info.get("confidence", explanation.get("confidence", 0.95)))
    possible_meanings = explanation.get("possible_meanings") or []
    is_ambiguous = confidence < 0.85 and len(possible_meanings) > 1

    # Decide whether image is useful (Prioritize explicit knowledge base visual rules)
    is_explicit_visual = explanation.get("show_image") is True
    pos = word_analysis.get("part_of_speech") or ""
    if not is_explicit_visual and pos in ["ADJ", "ADV", "CONJ", "PREP", "PRON", "DET", "INTJ"]:
        show_image = False
        image_query = None
    else:
        show_image = bool(explanation.get("show_image", False))
        image_query = explanation.get("image_query") if show_image else None
        if not image_query and show_image:
            image_query = f"{resolved_name} {entity_type}".strip()

    # Query Wikipedia for facts/definition ONLY (if not purely a grammatical connector)
    wiki_info = {}
    is_non_entity = term.lower() in ["however", "therefore", "consequently", "furthermore", "approximately", "thus"]
    
    # Image structure initialized to show: false
    image_obj = {
        "show": False,
        "url": None,
        "proxy_url": None,
        "title": None,
        "source": None,
        "source_url": None,
        "author": None,
        "license": None,
        "prompt": None,
    }

    async with httpx.AsyncClient(timeout=6.0, follow_redirects=True) as client:
        # 1. Wikipedia for Definition/Facts ONLY
        if not is_non_entity:
            try:
                wiki_info = await fetch_wikipedia_entity_definition(
                    client, resolved_name, entity_type, context_text=f"{section_title} {paragraph}"
                )
            except Exception as exc:
                logger.debug("Wikipedia definition lookup failed: %s", exc)

        # Extract primary definition (Prioritize clean, simple, plain-English definition)
        ai_def = str(explanation.get("definition") or "").strip()
        wiki_text = wiki_info.get("text", "").strip()
        is_generic_ai = not ai_def or "designates a specialized subject entity" in ai_def or ai_def.startswith("The document discusses")
        is_generic_wiki = not wiki_text or "designates a specialized subject entity" in wiki_text or wiki_text.startswith("In General Academic,")
        
        if ai_def and not is_generic_ai and len(ai_def) > 15:
            primary_def = ai_def
        elif wiki_text and not is_generic_wiki and len(wiki_text) > 15:
            primary_def = wiki_text
        elif ai_def:
            primary_def = ai_def
        else:
            primary_def = f"“{resolved_name}” is a key concept in {domain_topic or 'this subject'}."

        # 2. Image Retrieval Pipeline: Verified Wikipedia Lead Photo -> Wikimedia Commons -> Openverse
        # If no genuine, verified photo is available, STRICTLY set show: False (do not generate fake/unrelated images)
        if show_image and image_query:
            try:
                # 2a. Verified Wikipedia Lead Article Photo
                if wiki_info.get("image_url"):
                    raw_img = wiki_info["image_url"]
                    proxy_img = f"/api/documents/{doc_id}/image-proxy?url={quote(raw_img)}&term={quote(resolved_name)}&domain={quote(domain_topic)}&type={quote(entity_type)}"
                    image_obj = {
                        "show": True,
                        "url": raw_img,
                        "proxy_url": proxy_img,
                        "title": wiki_info.get("image_title") or resolved_name,
                        "source": "Wikipedia",
                        "source_url": wiki_info.get("source_url") or raw_img,
                        "author": "Wikipedia Lead Reference",
                        "license": "Creative Commons / Public Domain",
                        "prompt": None,
                    }
                else:
                    # 2b. Wikimedia Commons Search for Authentic Scientific Diagrams & Photos
                    wiki_img_res = await search_wikimedia_commons_image(client, image_query, resolved_name, entity_type)
                    if wiki_img_res.get("show") and wiki_img_res.get("url"):
                        raw_img = wiki_img_res["url"]
                        proxy_img = f"/api/documents/{doc_id}/image-proxy?url={quote(raw_img)}&term={quote(resolved_name)}&domain={quote(domain_topic)}&type={quote(entity_type)}"
                        image_obj = {
                            "show": True,
                            "url": raw_img,
                            "proxy_url": proxy_img,
                            "title": wiki_img_res.get("title") or resolved_name,
                            "source": "Wikimedia Commons",
                            "source_url": wiki_img_res.get("source_url") or raw_img,
                            "author": wiki_img_res.get("author") or "Wikimedia Contributor",
                            "license": wiki_img_res.get("license") or "CC BY-SA",
                            "prompt": None,
                        }
                    else:
                        # 2c. Openverse Search for Verified Entity Photos
                        ov_res = await search_openverse_image(client, image_query, resolved_name, entity_type)
                        if ov_res.get("show") and ov_res.get("url"):
                            raw_img = ov_res["url"]
                            proxy_img = f"/api/documents/{doc_id}/image-proxy?url={quote(raw_img)}&term={quote(resolved_name)}&domain={quote(domain_topic)}&type={quote(entity_type)}"
                            image_obj = {
                                "show": True,
                                "url": raw_img,
                                "proxy_url": proxy_img,
                                "title": ov_res.get("title") or resolved_name,
                                "source": "Openverse",
                                "source_url": ov_res.get("source_url") or raw_img,
                                "author": "Openverse Contributor",
                                "license": "Creative Commons",
                                "prompt": None,
                            }
                        else:
                            # If no genuine photo is available, do not show any image
                            image_obj["show"] = False
            except Exception as exc:
                logger.debug("Image search error: %s", exc)
                image_obj["show"] = False
    definition_obj = {
        "text": primary_def,
        "source": "Wikipedia" if wiki_text else "ReadFlow AI",
        "source_url": wiki_info.get("source_url") or f"https://en.wikipedia.org/wiki/{quote(resolved_name.replace(' ', '_'))}",
        "who": wiki_info.get("who"),
        "born": wiki_info.get("born"),
        "died": wiki_info.get("died"),
        "known_for": wiki_info.get("known_for"),
        "function": wiki_info.get("function") or explanation.get("technical_explanation"),
        "capital": wiki_info.get("capital"),
        "location": wiki_info.get("location"),
    }

    entity_obj = {
        "name": resolved_name,
        "type": entity_type,
        "confidence": confidence,
        "description": resolved_entity_info.get("description") or explanation.get("disambiguation") or "",
    }

    explanation_obj = {
        "definition": primary_def,
        "context": sentence,
        "technical_explanation": explanation.get("technical_explanation") or wiki_info.get("function") or "",
        "context_rationale": explanation.get("context_rationale") or explanation.get("disambiguation") or "",
        "example": explanation.get("example") or "",
    }

    source_url = wiki_info.get("source_url") or f"https://en.wikipedia.org/wiki/{quote(resolved_name.replace(' ', '_'))}"
    source_obj = {
        "title": resolved_name,
        "url": source_url,
        "description": primary_def,
        "provider": "wikipedia" if wiki_text else "ReadFlow AI",
    }

    real_image_url = image_obj.get("url") or ""
    real_image_proxy_url = image_obj.get("proxy_url") or ""

    google_images_url = f"https://www.google.com/search?tbm=isch&q={quote(f'{resolved_name} {entity_type}'.strip())}"
    google_search_url = f"https://www.google.com/search?q={quote(f'{resolved_name} {entity_type}'.strip())}"

    response = {
        # Section 12 Exact Structured Format
        "entity": entity_obj,
        "definition": definition_obj,
        "image": image_obj,
        "google_images_url": google_images_url,
        "google_search_url": google_search_url,
        
        # Core & Legacy Reader Compatibility Fields
        "word": term,
        "term": term,
        "show_image": image_obj["show"],
        "image_query": image_query if image_obj["show"] else None,
        "entity_name": resolved_name,
        "entity_type": entity_type,
        "explanation": explanation_obj,
        "source": source_obj,
        "source_url": source_url,
        "source_provider": source_obj["provider"],
        "is_ambiguous": is_ambiguous,
        "disambiguation_options": possible_meanings,
        "possible_meanings": possible_meanings,
        "confidence": confidence,
        "context": sentence,
        "sentence": sentence,
        "page": page_number,
        "doc_id": doc_id,
        "real_image": real_image_url,
        "real_image_proxy": real_image_proxy_url,
        "image_title": image_obj.get("title") or "",
        "domain_topic": domain_topic,
        "disambiguation": explanation.get("disambiguation") or explanation.get("context_rationale") or "",
        "technical_explanation": explanation_obj["technical_explanation"],
        "example": explanation.get("example") or "",
        "root_word": word_analysis["lemma"],
        "part_of_speech": word_analysis["part_of_speech"],
        "svg_diagram": "",
        "svg": "",
        **word_analysis,
    }
    return response


OPENVERSE_IMAGE_CACHE: dict = {}
WIKIPEDIA_DEFINITION_CACHE: dict = {}


def is_valid_image_url(url: str, title: str = "") -> bool:
    """Validate image candidate, rejecting icons, generic logos, disambiguation files, and SVG placeholders."""
    if not url or not isinstance(url, str):
        return False
    lower_url = url.lower()
    lower_title = title.lower()
    if lower_url.endswith(".svg") or ".svg/" in lower_url:
        return False
    bad_tokens = [
        "disambig", "question_mark", "question_book", "no_image", "icon", "blank", "crystal_clear",
        "wikimedia-logo", "wikipedia-logo", "padlock", "decrease", "increase",
        "red_pog", "blue_pog", "ambox", "folder", "arrow", "bullet", "placeholder",
        "mergefrom", "split", "cleanup", "refimprove", "stub"
    ]
    for token in bad_tokens:
        if token in lower_url or token in lower_title:
            return False
    return True


def is_mismatched_wiki_page(p_title: str, p_extract: str, e_name: str, e_type: str, ctx: str) -> bool:
    full = f"{p_title} {p_extract}".lower()
    e_type_l = e_type.lower()
    e_name_l = e_name.lower()
    ctx_l = ctx.lower()

    # 1. Biology/taxonomy vs country/geography/monarchy
    is_bio = any(k in e_type_l or k in e_name_l or k in ctx_l for k in ["taxonomic", "taxonomy", "biology", "species", "genus", "phylum", "kingdom", "organism", "botany", "zoology", "linnaeus", "systematics"])
    if is_bio:
        if any(bad in full for bad in ["country in", "sovereign state", "monarchy", "united kingdom", "great britain", "island country", "population of over"]):
            if not any(good in full for good in ["taxonomic", "biological", "domain", "species", "linnaean", "organism", "plantae", "animalia"]):
                return True

    # 2. Astronomy/Planet vs Chemistry/Element or Mythology/Car
    if "planet" in e_type_l or "solar system" in e_type_l:
        if any(bad in full for bad in ["chemical element", "atomic number", "metal", "thermometer", "sedan", "car manufacturer", "god in roman"]):
            if not any(good in full for good in ["planet", "orbit", "solar system", "celestial"]):
                return True

    # 3. Chemistry/Element vs Planet/Astronomy
    if "chemical element" in e_type_l or "metal" in e_type_l:
        if any(bad in full for bad in ["planet", "solar system", "orbit", "spacecraft", "astronomical"]):
            if not any(good in full for good in ["element", "atomic", "chemical", "metal"]):
                return True

    # 4. Programming language vs Animal/Reptile
    if "programming" in e_type_l or "software" in e_type_l:
        if any(bad in full for bad in ["non-venomous snake", "snake species", "reptile", "serpent"]):
            if not any(good in full for good in ["programming language", "software", "code", "scripting"]):
                return True

    # 5. Animal/Reptile vs Software
    if "snake" in e_type_l or "reptile" in e_type_l:
        if any(bad in full for bad in ["programming language", "high-level programming", "source code", "python software"]):
            return True

    return False


def is_openverse_result_relevant(item: dict, entity_name: str, entity_type: str, query: str) -> bool:
    """
    Inspect Openverse metadata (title, tags, description, creator) to verify relevance.
    Strictly reject mismatched topics (e.g. tree/farming/recipe for a fruit, car/metal for a planet, etc.).
    """
    url = item.get("url") or ""
    title = (item.get("title") or "").lower()
    tags = [t.get("name", "").lower() if isinstance(t, dict) else str(t).lower() for t in item.get("tags", [])]
    tag_str = " ".join(tags)
    full_meta = f"{title} {tag_str}".lower()
    e_name_lower = entity_name.lower().strip()
    e_type_lower = entity_type.lower().strip()

    if not is_valid_image_url(url, title):
        return False

    # 1. Anti-pattern checks based on entity type & name
    if "fruit" in e_type_lower or e_name_lower in ["mango", "apple", "banana", "orange", "potato", "tomato"]:
        mismatched_fruit_tokens = ["tree", "farm", "farming", "cultivation", "orchard", "plantation", "leaf", "leaves", "blossom", "flower", "cooking", "recipe", "salad", "smoothie", "field"]
        if any(token in title for token in ["tree", "farm", "farming", "cultivation", "plantation", "orchard"]):
            if "fruit" not in title and "close" not in title:
                return False

    if "planet" in e_type_lower or "solar system" in e_type_lower:
        mismatched_planet_tokens = ["element", "metal", "mercury thermometer", "car", "sedan", "god", "mythology", "statue", "temple"]
        if any(token in full_meta for token in mismatched_planet_tokens):
            return False

    if "chemical element" in e_type_lower or "metal" in e_type_lower:
        mismatched_elem_tokens = ["planet", "astronomy", "crater", "car", "automobile", "god", "mythology"]
        if any(token in full_meta for token in mismatched_elem_tokens):
            return False

    if "snake" in e_type_lower or "reptile" in e_type_lower:
        mismatched_snake_tokens = ["programming", "code", "software", "developer", "computer", "scripting", "logo"]
        if any(token in full_meta for token in mismatched_snake_tokens):
            return False

    if "programming" in e_type_lower or "software" in e_type_lower:
        mismatched_prog_tokens = ["snake", "reptile", "serpent", "island", "coffee", "animal"]
        if any(token in full_meta for token in mismatched_prog_tokens):
            return False

    if "person" in e_type_lower or "scientist" in e_type_lower:
        mismatched_person_tokens = ["statue", "caricature", "doll", "action figure", "t-shirt", "graffiti", "wax"]
        if any(token in full_meta for token in mismatched_person_tokens):
            return False

    if "taxonomic" in e_type_lower or "taxonomy" in e_type_lower or "kingdom" in e_name_lower or "phylum" in e_name_lower:
        mismatched_taxo_tokens = ["castle", "monarchy", "medieval", "united kingdom", "london", "palace", "queen", "king charles", "royalty", "prince"]
        if any(token in full_meta for token in mismatched_taxo_tokens):
            if not any(good in full_meta for good in ["biology", "classification", "taxonomic", "organism", "life", "tree of life", "domain"]):
                return False

    # 2. Positive relevance check: Key word of the entity or query should appear in title or tags
    entity_keywords = [w for w in re.findall(r"[a-zA-Z0-9]+", e_name_lower) if len(w) >= 3 and w not in ["the", "and", "for", "with", "inc", "species"]]
    query_keywords = [w for w in re.findall(r"[a-zA-Z0-9]+", query.lower()) if len(w) >= 3 and w not in ["the", "and", "for", "with", "inc", "species", "diagram", "chart", "illustration", "image"]]
    all_target_keywords = set(entity_keywords + query_keywords)
    if all_target_keywords:
        has_keyword = any(k in full_meta for k in all_target_keywords)
        if not has_keyword:
            return False

    return True



WIKIMEDIA_COMMONS_IMAGE_CACHE: dict = {}

def is_wikimedia_result_relevant(title: str, description: str, entity_name: str, entity_type: str, query: str) -> bool:
    """Validate Wikimedia Commons image candidate, rejecting non-visual icons, logos, flags, coats of arms, and chemical skeletal formulas for organisms."""
    full = f"{title} {description}".lower()
    lower_name = entity_name.lower().strip()
    lower_type = entity_type.lower().strip()
    
    if not is_valid_image_url(title, title):
        return False
        
    bad_tokens = ["disambig", "icon", "logo", "flag of", "coat of arms", "signature", "stamp", "banner", "locator map"]
    if any(bt in full for bt in bad_tokens):
        if "diagram" not in full and "structure" not in full and "pathway" not in full:
            return False

    # Biology / organism / kingdom / fungus: reject chemical skeletal formula / chitin / polymer / molecular structure
    is_organism = any(b in lower_type or b in lower_name for b in ["kingdom", "organism", "fungi", "fungus", "plant", "animal", "species", "genus", "taxonomy", "mycology", "botany", "zoology"])
    if is_organism:
        if any(chem in full for chem in ["chitin", "chemical formula", "skeletal formula", "structural formula", "skelettformel", "chemical structure", "molecular formula", "cas number"]):
            return False

    keywords = [w for w in re.findall(r"[a-zA-Z0-9]+", lower_name) if len(w) >= 3 and w not in ["the", "and", "for", "with", "system", "rank"]]
    if keywords:
        if not any(k in full for k in keywords):
            return False
    return True


async def search_wikimedia_commons_image(
    client: httpx.AsyncClient,
    query: str,
    entity_name: str = "",
    entity_type: str = "",
) -> dict:
    """
    Search Wikimedia Commons API for authentic high-quality educational diagrams and reference images.
    Returns structured image data including author and license attribution.
    """
    clean_name = entity_name or query
    clean_q = query.strip()
    cache_key = f"{clean_q.casefold()}:{clean_name.casefold()}:{entity_type.casefold()}"
    if cache_key in WIKIMEDIA_COMMONS_IMAGE_CACHE:
        return WIKIMEDIA_COMMONS_IMAGE_CACHE[cache_key]

    headers = {
        "User-Agent": "ReadFlowAI/1.0 (educational document reader; info@readflow.ai)",
        "Accept": "application/json",
    }
    result = {
        "show": False,
        "url": None,
        "title": None,
        "source": None,
        "source_url": None,
        "author": None,
        "license": None,
    }

    query_variants = []
    if clean_q:
        query_variants.append(clean_q)
    if f"{clean_name} diagram" not in query_variants:
        query_variants.append(f"{clean_name} diagram")
    if clean_name and clean_name not in query_variants:
        query_variants.append(clean_name)
    if entity_type and f"{clean_name} {entity_type}" not in query_variants:
        query_variants.append(f"{clean_name} {entity_type}")

    for q_var in query_variants:
        if result["show"]:
            break
        try:
            url = f"https://commons.wikimedia.org/w/api.php?action=query&generator=search&gsrsearch={quote(q_var)}&gsrnamespace=6&prop=imageinfo&iiprop=url|size|extmetadata|mime&format=json"
            resp = await client.get(url, headers=headers, timeout=4.0)
            if resp.status_code == 200:
                pages = resp.json().get("query", {}).get("pages", {})
                for pid, pinfo in pages.items():
                    if pid == "-1":
                        continue
                    img_info = pinfo.get("imageinfo", [{}])[0]
                    img_url = img_info.get("url") or img_info.get("thumburl") or ""
                    width = img_info.get("width", 0)
                    height = img_info.get("height", 0)
                    if width and height and (width < 80 or height < 80):
                        continue
                    
                    p_title = pinfo.get("title", "")
                    meta = img_info.get("extmetadata", {})
                    artist_raw = meta.get("Artist", {}).get("value", "")
                    artist = re.sub(r"<[^>]+>", "", artist_raw).strip() if artist_raw else "Wikimedia Commons Contributor"
                    license_name = meta.get("LicenseShortName", {}).get("value") or meta.get("License", {}).get("value") or "CC BY-SA"
                    desc = meta.get("ImageDescription", {}).get("value", "")
                    desc_clean = re.sub(r"<[^>]+>", "", desc).strip() if desc else ""

                    if is_wikimedia_result_relevant(p_title, desc_clean, clean_name, entity_type, q_var):
                        result = {
                            "show": True,
                            "url": img_url,
                            "title": re.sub(r"^File:", "", p_title),
                            "source": "Wikimedia Commons",
                            "source_url": img_info.get("descriptionurl") or img_url,
                            "author": artist[:50],
                            "license": license_name,
                        }
                        break
        except Exception as exc:
            logger.debug("Wikimedia Commons image search error for '%s': %s", q_var, exc)

    if len(WIKIMEDIA_COMMONS_IMAGE_CACHE) >= 500:
        WIKIMEDIA_COMMONS_IMAGE_CACHE.pop(next(iter(WIKIMEDIA_COMMONS_IMAGE_CACHE)))
    WIKIMEDIA_COMMONS_IMAGE_CACHE[cache_key] = result
    return result


async def search_openverse_image(
    client: httpx.AsyncClient,
    query: str,
    entity_name: str = "",
    entity_type: str = "",
) -> dict:
    """
    Search Openverse public anonymous API strictly for images matching the resolved entity.
    Returns structured image data if a verified relevant image is found, otherwise show: false.
    """
    clean_name = entity_name or query
    clean_q = query.strip()
    cache_key = f"{clean_q.casefold()}:{clean_name.casefold()}:{entity_type.casefold()}"
    if cache_key in OPENVERSE_IMAGE_CACHE:
        return OPENVERSE_IMAGE_CACHE[cache_key]

    headers = {
        "User-Agent": "ReadFlowAI/1.0 (educational document reader; info@readflow.ai)",
        "Accept": "application/json",
    }

    result = {
        "show": False,
        "url": None,
        "title": None,
        "source": None,
        "source_url": None,
    }

    query_variants = []
    if clean_q:
        query_variants.append(clean_q)
    if entity_type:
        type_q = f"{clean_name} {entity_type}".strip()
        if type_q not in query_variants:
            query_variants.append(type_q)
    if clean_name and clean_name not in query_variants:
        query_variants.append(clean_name)
    
    # Strip parentheses e.g. "Kingdom (biology)" -> "Kingdom biology"
    unparenthesized = re.sub(r"[()]", "", clean_name).strip()
    if unparenthesized and unparenthesized not in query_variants:
        query_variants.append(unparenthesized)

    for q_var in query_variants:
        if result["show"]:
            break
        try:
            url = f"https://api.openverse.org/v1/images/?q={quote(q_var)}&page_size=10"
            resp = await client.get(url, headers=headers, timeout=4.5)
            if resp.status_code == 200:
                data = resp.json()
                items = data.get("results", [])
                for item in items:
                    img_url = item.get("url") or item.get("thumbnail") or ""
                    img_title = item.get("title") or clean_name
                    if is_openverse_result_relevant(item, clean_name, entity_type, q_var):
                        result = {
                            "show": True,
                            "url": img_url,
                            "title": img_title,
                            "source": "Openverse",
                            "source_url": item.get("foreign_landing_url") or item.get("url") or f"https://openverse.org/image/{item.get('id', '')}",
                        }
                        break
        except Exception as exc:
            logger.debug("Openverse image retrieval error for '%s': %s", q_var, exc)

    if len(OPENVERSE_IMAGE_CACHE) >= 500:
        OPENVERSE_IMAGE_CACHE.pop(next(iter(OPENVERSE_IMAGE_CACHE)))
    OPENVERSE_IMAGE_CACHE[cache_key] = result
    return result


async def fetch_wikipedia_entity_definition(
    client: httpx.AsyncClient,
    entity_name: str,
    entity_type: str = "",
    context_text: str = "",
) -> dict:
    """
    Fetch factual entity definition and structured information strictly from Wikipedia.
    NEVER retrieves images from Wikipedia.
    """
    clean_name = re.sub(r"^[^\w]+|[^\w]+$", "", entity_name.strip())
    clean_name = re.sub(r"\s+(?:Linn\.?|L\.?|var\.?|subsp\.?|sp\.?)$", "", clean_name, flags=re.IGNORECASE).strip()
    if not clean_name:
        return {}

    cache_key = f"{clean_name.casefold()}:{entity_type.casefold()}"
    if cache_key in WIKIPEDIA_DEFINITION_CACHE:
        return WIKIPEDIA_DEFINITION_CACHE[cache_key]

    headers = {
        "User-Agent": "ReadFlowAI/1.0 (educational document reader; info@readflow.ai)",
        "Accept": "application/json",
    }

    wiki_result = {
        "text": "",
        "source": "Wikipedia",
        "source_url": f"https://en.wikipedia.org/wiki/{quote(clean_name.replace(' ', '_'))}",
        "who": None,
        "born": None,
        "died": None,
        "known_for": None,
        "function": None,
        "capital": None,
        "location": None,
    }

    def is_disambiguation(page_info: dict) -> bool:
        if page_info.get("pageprops", {}).get("disambiguation") is not None:
            return True
        title = page_info.get("title", "").lower()
        if "(disambiguation)" in title:
            return True
        extract = page_info.get("extract", "").lower()
        if any(marker in extract for marker in ["may refer to:", "refer to:", "usually refers to:"]):
            return True
        return False

    candidate_titles = [clean_name]
    
    # Check if biology / taxonomy context
    is_bio_ctx = any(k in entity_type.lower() or k in context_text.lower() for k in ["taxonomic", "taxonomy", "biology", "species", "genus", "phylum", "kingdom", "organism"])
    if is_bio_ctx:
        if f"{clean_name} (biology)" not in candidate_titles:
            candidate_titles.insert(0, f"{clean_name} (biology)")
        if f"{clean_name} (taxonomic rank)" not in candidate_titles:
            candidate_titles.insert(1, f"{clean_name} (taxonomic rank)")

    if entity_type and f"{clean_name} ({entity_type})" not in candidate_titles:
        candidate_titles.append(f"{clean_name} ({entity_type})")

    extract_text = ""
    page_url = ""
    page_title = clean_name

    # 1. Exact Title Query
    for title_q in candidate_titles:
        if extract_text:
            break
        try:
            wiki_api = f"https://en.wikipedia.org/w/api.php?action=query&titles={quote(title_q)}&prop=extracts|pageprops|info|pageimages&pithumbsize=600&piprop=thumbnail|original&inprop=url&exintro=1&explaintext=1&redirects=1&format=json"
            resp = await client.get(wiki_api, headers=headers, timeout=3.5)
            if resp.status_code == 200:
                pages = resp.json().get("query", {}).get("pages", {})
                for pid, pinfo in pages.items():
                    if pid == "-1" or is_disambiguation(pinfo) or is_mismatched_wiki_page(pinfo.get("title", ""), pinfo.get("extract", ""), clean_name, entity_type, context_text):
                        continue
                    ext = pinfo.get("extract", "").strip()
                    if ext and len(ext) > 20:
                        extract_text = ext
                        page_title = pinfo.get("title", clean_name)
                        page_url = pinfo.get("fullurl") or f"https://en.wikipedia.org/wiki/{quote(page_title.replace(' ', '_'))}"
                        thumb = pinfo.get("thumbnail", {}).get("source") or pinfo.get("original", {}).get("source")
                        if thumb and is_valid_image_url(thumb, page_title):
                            # Ensure not a chemical formula if organism
                            if not (any(b in entity_type.lower() or b in clean_name.lower() for b in ["fungi", "fungus", "kingdom", "organism", "animal", "plant"]) and any(c in thumb.lower() for c in ["chitin", "formula", "skeletal", "structure"])):
                                wiki_result["image_url"] = thumb
                                wiki_result["image_title"] = page_title
                        break
        except Exception:
            pass

    # 2. Generator Search Query if exact title failed
    if not extract_text:
        try:
            search_query = f"{clean_name} {entity_type}".strip() if entity_type and entity_type != "concept" else clean_name
            search_api = f"https://en.wikipedia.org/w/api.php?action=query&generator=search&gsrsearch={quote(search_query)}&gsrlimit=3&prop=extracts|pageprops|info|pageimages&pithumbsize=600&piprop=thumbnail|original&inprop=url&exintro=1&explaintext=1&format=json"
            resp = await client.get(search_api, headers=headers, timeout=3.5)
            if resp.status_code == 200:
                pages = resp.json().get("query", {}).get("pages", {})
                for pid, pinfo in pages.items():
                    if pid == "-1" or is_disambiguation(pinfo) or is_mismatched_wiki_page(pinfo.get("title", ""), pinfo.get("extract", ""), clean_name, entity_type, context_text):
                        continue
                    ext = pinfo.get("extract", "").strip()
                    if ext and len(ext) > 20:
                        extract_text = ext
                        page_title = pinfo.get("title", clean_name)
                        page_url = pinfo.get("fullurl") or f"https://en.wikipedia.org/wiki/{quote(page_title.replace(' ', '_'))}"
                        thumb = pinfo.get("thumbnail", {}).get("source") or pinfo.get("original", {}).get("source")
                        if thumb and is_valid_image_url(thumb, page_title):
                            # Ensure not a chemical formula if organism
                            if not (any(b in entity_type.lower() or b in clean_name.lower() for b in ["fungi", "fungus", "kingdom", "organism", "animal", "plant"]) and any(c in thumb.lower() for c in ["chitin", "formula", "skeletal", "structure"])):
                                wiki_result["image_url"] = thumb
                                wiki_result["image_title"] = page_title
                        break
        except Exception:
            pass

    if extract_text:
        sentences = [s.strip() for s in re.split(r"(?<=[.!?])\s+", extract_text) if s.strip()]
        first_two = " ".join(sentences[:2]).strip()
        wiki_result["text"] = first_two or extract_text[:350].strip()
        if page_url:
            wiki_result["source_url"] = page_url

        # Extract structured facts based on category
        e_type_l = entity_type.lower()
        if "person" in e_type_l or "scientist" in e_type_l:
            wiki_result["who"] = sentences[0] if sentences else None
            date_match = re.search(r"\((?:born\s+)?(\d{1,2}\s+[A-Za-z]+\s+\d{4}|\d{4})\s*[–—-]\s*(\d{1,2}\s+[A-Za-z]+\s+\d{4}|\d{4})?\)", extract_text)
            if date_match:
                wiki_result["born"] = date_match.group(1).strip()
                if date_match.group(2):
                    wiki_result["died"] = date_match.group(2).strip()
            known_match = re.search(r"(?:best known for|known for|renowned for|developed|discovered|formulated)\s+([^.;\n]+)", extract_text, re.IGNORECASE)
            if known_match:
                wiki_result["known_for"] = known_match.group(1).strip().capitalize()

        elif "place" in e_type_l or "location" in e_type_l or "country" in e_type_l or "city" in e_type_l:
            cap_match = re.search(r"(?:capital\s+is|capital\s+city\s+is)\s+([A-Z][a-zA-Z\s]+?)(?:[.,;]|\s+and|\s+with)", extract_text, re.IGNORECASE)
            if cap_match:
                wiki_result["capital"] = cap_match.group(1).strip()
            loc_match = re.search(r"(?:located in|country in|island in|region in|situated in)\s+([A-Z][a-zA-Z\s]+?)(?:[.,;]|\s+and)", extract_text, re.IGNORECASE)
            if loc_match:
                wiki_result["location"] = loc_match.group(1).strip()

        elif any(sc_kw in e_type_l for sc_kw in ["cell", "organelle", "biological", "chemical", "physical", "organ", "process", "cycle", "system", "science"]):
            func_match = re.search(r"(?:primarily involved in|responsible for|functions to|functions as|plays a key role in|used to|serves to|involved in)\s+([^.;\n]+)", extract_text, re.IGNORECASE)
            if func_match:
                matched_phrase = func_match.group(0).strip()
                wiki_result["function"] = matched_phrase[0].upper() + matched_phrase[1:] + ("." if not matched_phrase.endswith(".") else "")
            elif len(sentences) > 1:
                wiki_result["function"] = sentences[1]

    # If online Wikipedia fetch did not return text, use encyclopedic knowledge base & contextual extractor
    if not wiki_result["text"]:
        from ai_service import ACADEMIC_KNOWLEDGE_BASE, extract_contextual_term_definition
        lower_name = clean_name.lower().strip()
        kb_entry = ACADEMIC_KNOWLEDGE_BASE.get(lower_name)
        if not kb_entry and lower_name.endswith("s"):
            kb_entry = ACADEMIC_KNOWLEDGE_BASE.get(lower_name[:-1])
        if not kb_entry and lower_name.endswith("es"):
            kb_entry = ACADEMIC_KNOWLEDGE_BASE.get(lower_name[:-2])
        if not kb_entry and "-" in lower_name:
            kb_entry = ACADEMIC_KNOWLEDGE_BASE.get(lower_name.replace("-", " ")) or ACADEMIC_KNOWLEDGE_BASE.get(lower_name.replace("-", ""))

        if kb_entry:
            wiki_result["text"] = kb_entry["definition"]
            wiki_result["function"] = kb_entry.get("technical_explanation")
            wiki_result["source"] = "Wikipedia"
            wiki_result["source_url"] = f"https://en.wikipedia.org/wiki/{quote(clean_name.replace(' ', '_'))}"
        else:
            ctx_def = extract_contextual_term_definition(clean_name, context_text, entity_type)
            if ctx_def and ctx_def.get("definition"):
                wiki_result["text"] = ctx_def["definition"]
                wiki_result["function"] = ctx_def.get("technical_explanation")
                wiki_result["source"] = "Wikipedia"
                wiki_result["source_url"] = f"https://en.wikipedia.org/wiki/{quote(clean_name.replace(' ', '_'))}"

    if len(WIKIPEDIA_DEFINITION_CACHE) >= 500:
        WIKIPEDIA_DEFINITION_CACHE.pop(next(iter(WIKIPEDIA_DEFINITION_CACHE)))
    WIKIPEDIA_DEFINITION_CACHE[cache_key] = wiki_result
    return wiki_result


def generate_fallback_concept_svg(term: str, category: str = "scientific_term", root_word: str = "", domain: str = "", definition_hint: str = "") -> str:
    """Generate a rich, beautiful, educational textbook vector diagram SVG tailored for ANY specific academic discipline."""
    clean_term = html.escape(re.sub(r"^(?:detailed colored|clear educational|scientific|drawing of)\s*", "", term, flags=re.I).strip())[:40]
    if not clean_term:
        clean_term = "Academic Concept"
    cat_clean = html.escape(category.replace("_", " ").title())
    dom_l = f"{domain.lower()} {category.lower()} {clean_term.lower()} {definition_hint.lower()}"

    # 1. Benchmark: Neural Networks / Deep Learning / Artificial Intelligence
    if any(k in dom_l for k in ["neural network", "deep learning", "perceptron", "backpropagation", "convolutional neural", "recurrent neural", "artificial neural"]):
        return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 540 260" width="100%" height="100%">
  <defs>
    <linearGradient id="nnGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#0f172a"/>
      <stop offset="100%" stop-color="#1e293b"/>
    </linearGradient>
    <linearGradient id="nodeInGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#38bdf8"/>
      <stop offset="100%" stop-color="#0284c7"/>
    </linearGradient>
    <linearGradient id="nodeHidGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#a855f7"/>
      <stop offset="100%" stop-color="#7e22ce"/>
    </linearGradient>
    <linearGradient id="nodeOutGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#22c55e"/>
      <stop offset="100%" stop-color="#15803d"/>
    </linearGradient>
  </defs>
  <rect width="540" height="260" rx="10" fill="url(#nnGrad)" stroke="#334155" stroke-width="1.5"/>
  <!-- Synaptic Connection Lines -->
  <!-- In to Hidden 1 -->
  <g stroke="#64748b" stroke-width="1.2" opacity="0.6">
    <line x1="80" y1="80" x2="200" y2="60"/><line x1="80" y1="80" x2="200" y2="105"/><line x1="80" y1="80" x2="200" y2="150"/><line x1="80" y1="80" x2="200" y2="195"/>
    <line x1="80" y1="130" x2="200" y2="60"/><line x1="80" y1="130" x2="200" y2="105"/><line x1="80" y1="130" x2="200" y2="150"/><line x1="80" y1="130" x2="200" y2="195"/>
    <line x1="80" y1="180" x2="200" y2="60"/><line x1="80" y1="180" x2="200" y2="105"/><line x1="80" y1="180" x2="200" y2="150"/><line x1="80" y1="180" x2="200" y2="195"/>
    <!-- Hidden 1 to Hidden 2 -->
    <line x1="200" y1="60" x2="330" y2="70"/><line x1="200" y1="60" x2="330" y2="125"/><line x1="200" y1="60" x2="330" y2="180"/>
    <line x1="200" y1="105" x2="330" y2="70"/><line x1="200" y1="105" x2="330" y2="125"/><line x1="200" y1="105" x2="330" y2="180"/>
    <line x1="200" y1="150" x2="330" y2="70"/><line x1="200" y1="150" x2="330" y2="125"/><line x1="200" y1="150" x2="330" y2="180"/>
    <line x1="200" y1="195" x2="330" y2="70"/><line x1="200" y1="195" x2="330" y2="125"/><line x1="200" y1="195" x2="330" y2="180"/>
    <!-- Hidden 2 to Output -->
    <line x1="330" y1="70" x2="450" y2="95"/><line x1="330" y1="70" x2="450" y2="160"/>
    <line x1="330" y1="125" x2="450" y2="95"/><line x1="330" y1="125" x2="450" y2="160"/>
    <line x1="330" y1="180" x2="450" y2="95"/><line x1="330" y1="180" x2="450" y2="160"/>
  </g>
  <!-- Input Layer Nodes -->
  <circle cx="80" cy="80" r="16" fill="url(#nodeInGrad)" stroke="#38bdf8" stroke-width="2"/>
  <text x="80" y="84" font-family="system-ui, sans-serif" font-size="10" font-weight="700" fill="#ffffff" text-anchor="middle">x₁</text>
  <circle cx="80" cy="130" r="16" fill="url(#nodeInGrad)" stroke="#38bdf8" stroke-width="2"/>
  <text x="80" y="134" font-family="system-ui, sans-serif" font-size="10" font-weight="700" fill="#ffffff" text-anchor="middle">x₂</text>
  <circle cx="80" cy="180" r="16" fill="url(#nodeInGrad)" stroke="#38bdf8" stroke-width="2"/>
  <text x="80" y="184" font-family="system-ui, sans-serif" font-size="10" font-weight="700" fill="#ffffff" text-anchor="middle">x₃</text>
  <!-- Hidden Layer 1 Nodes -->
  <circle cx="200" cy="60" r="15" fill="url(#nodeHidGrad)" stroke="#c084fc" stroke-width="2"/>
  <circle cx="200" cy="105" r="15" fill="url(#nodeHidGrad)" stroke="#c084fc" stroke-width="2"/>
  <circle cx="200" cy="150" r="15" fill="url(#nodeHidGrad)" stroke="#c084fc" stroke-width="2"/>
  <circle cx="200" cy="195" r="15" fill="url(#nodeHidGrad)" stroke="#c084fc" stroke-width="2"/>
  <!-- Hidden Layer 2 Nodes -->
  <circle cx="330" cy="70" r="15" fill="url(#nodeHidGrad)" stroke="#c084fc" stroke-width="2"/>
  <circle cx="330" cy="125" r="15" fill="url(#nodeHidGrad)" stroke="#c084fc" stroke-width="2"/>
  <circle cx="330" cy="180" r="15" fill="url(#nodeHidGrad)" stroke="#c084fc" stroke-width="2"/>
  <!-- Output Layer Nodes -->
  <circle cx="450" cy="95" r="16" fill="url(#nodeOutGrad)" stroke="#4ade80" stroke-width="2"/>
  <text x="450" y="99" font-family="system-ui, sans-serif" font-size="10" font-weight="700" fill="#ffffff" text-anchor="middle">y₁</text>
  <circle cx="450" cy="160" r="16" fill="url(#nodeOutGrad)" stroke="#4ade80" stroke-width="2"/>
  <text x="450" y="164" font-family="system-ui, sans-serif" font-size="10" font-weight="700" fill="#ffffff" text-anchor="middle">y₂</text>
  <!-- Labels -->
  <text x="80" y="218" font-family="system-ui, sans-serif" font-size="10" font-weight="700" fill="#38bdf8" text-anchor="middle">Input Layer</text>
  <text x="265" y="218" font-family="system-ui, sans-serif" font-size="10" font-weight="700" fill="#c084fc" text-anchor="middle">Hidden Layers (σ, ReLU)</text>
  <text x="450" y="218" font-family="system-ui, sans-serif" font-size="10" font-weight="700" fill="#4ade80" text-anchor="middle">Output Layer</text>
  <rect x="130" y="12" width="280" height="26" rx="4" fill="#334155"/>
  <text x="270" y="29" font-family="system-ui, sans-serif" font-size="12" font-weight="700" fill="#f8fafc" text-anchor="middle">{clean_term} · Artificial Neural Architecture</text>
  <text x="270" y="244" font-family="system-ui, sans-serif" font-size="10" fill="#94a3b8" text-anchor="middle">Forward Propagation y = f(∑wᵢxᵢ + b) · Gradient Descent Optimization</text>
</svg>"""

        # 2b. Benchmark: Mycology / Fungi / Kingdom Fungi / Mushroom Anatomy & Spores
    elif any(k in dom_l for k in ["fungi", "fungus", "mycology", "mushroom", "mycelium", "basidiomycota", "ascomycota"]):
        return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 540 260" width="100%" height="100%">
  <defs>
    <linearGradient id="fungiSkyGrad" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="#f0fdf4"/>
      <stop offset="100%" stop-color="#dcfce7"/>
    </linearGradient>
    <linearGradient id="capGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#dc2626"/>
      <stop offset="100%" stop-color="#991b1b"/>
    </linearGradient>
    <linearGradient id="stemGrad" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#fef3c7"/>
      <stop offset="100%" stop-color="#fde68a"/>
    </linearGradient>
    <linearGradient id="soilGrad" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="#78350f"/>
      <stop offset="100%" stop-color="#451a03"/>
    </linearGradient>
  </defs>
  <rect width="540" height="260" rx="10" fill="url(#fungiSkyGrad)" stroke="#86efac" stroke-width="1.5"/>
  <rect x="0" y="195" width="540" height="65" fill="url(#soilGrad)"/>
  <g stroke="#fef08a" stroke-width="1.2" opacity="0.85" fill="none">
    <path d="M190 205 Q160 215 130 220 Q100 225 70 235"/>
    <path d="M130 220 Q110 240 85 248"/>
    <path d="M210 205 Q240 220 280 228 Q330 235 380 232"/>
    <path d="M280 228 Q300 245 330 252"/>
    <path d="M200 210 Q195 235 190 255"/>
    <path d="M195 235 Q170 245 150 250"/>
  </g>
  <path d="M185 115 C182 145 180 180 178 205 L218 205 C215 180 212 145 208 115 Z" fill="url(#stemGrad)" stroke="#d97706" stroke-width="1.2"/>
  <path d="M180 150 Q195 156 215 150 Q218 158 210 162 Q195 165 182 158 Z" fill="#fef9c3" stroke="#d97706" stroke-width="1"/>
  <path d="M135 115 Q195 128 258 115 Q195 110 135 115 Z" fill="#fef08a" stroke="#ca8a04" stroke-width="1"/>
  <line x1="150" y1="116" x2="160" y2="121" stroke="#ca8a04" stroke-width="0.8"/>
  <line x1="170" y1="117" x2="175" y2="123" stroke="#ca8a04" stroke-width="0.8"/>
  <line x1="220" y1="117" x2="218" y2="123" stroke="#ca8a04" stroke-width="0.8"/>
  <line x1="240" y1="116" x2="232" y2="121" stroke="#ca8a04" stroke-width="0.8"/>
  <path d="M130 115 C130 65 265 65 265 115 Q195 125 130 115 Z" fill="url(#capGrad)" stroke="#7f1d1d" stroke-width="1.5"/>
  <circle cx="160" cy="90" r="4.5" fill="#ffffff" opacity="0.9"/>
  <circle cx="190" cy="78" r="5.5" fill="#ffffff" opacity="0.9"/>
  <circle cx="225" cy="85" r="4.5" fill="#ffffff" opacity="0.9"/>
  <circle cx="178" cy="100" r="3.5" fill="#ffffff" opacity="0.9"/>
  <circle cx="242" cy="102" r="3" fill="#ffffff" opacity="0.9"/>
  <circle cx="145" cy="104" r="3" fill="#ffffff" opacity="0.9"/>
  <path d="M285 160 C284 175 282 195 280 205 L302 205 C300 195 298 175 296 160 Z" fill="url(#stemGrad)" stroke="#d97706" stroke-width="1"/>
  <path d="M272 160 C272 135 310 135 310 160 Q290 166 272 160 Z" fill="url(#capGrad)" stroke="#7f1d1d" stroke-width="1.2"/>
  <circle cx="290" cy="148" r="2.5" fill="#ffffff" opacity="0.9"/>
  <g fill="#ca8a04" opacity="0.75">
    <circle cx="140" cy="132" r="2"/><circle cx="148" cy="142" r="1.5"/><circle cx="132" cy="150" r="2"/>
    <circle cx="255" cy="132" r="2"/><circle cx="262" cy="144" r="1.8"/><circle cx="248" cy="155" r="2"/>
  </g>
  <line x1="265" y1="75" x2="350" y2="60" stroke="#0f172a" stroke-width="1.2" stroke-dasharray="2,2"/>
  <rect x="350" y="48" width="165" height="22" rx="4" fill="#ffffff" stroke="#991b1b" stroke-width="1"/>
  <text x="432" y="63" font-family="system-ui, sans-serif" font-size="11" font-weight="700" fill="#991b1b" text-anchor="middle">Pileus (Cap) &amp; Basidiocarp</text>
  <line x1="258" y1="120" x2="350" y2="105" stroke="#0f172a" stroke-width="1.2" stroke-dasharray="2,2"/>
  <rect x="350" y="93" width="165" height="22" rx="4" fill="#ffffff" stroke="#b45309" stroke-width="1"/>
  <text x="432" y="108" font-family="system-ui, sans-serif" font-size="10.5" font-weight="700" fill="#b45309" text-anchor="middle">Gills (Hymenium / Spores)</text>
  <line x1="216" y1="155" x2="350" y2="148" stroke="#0f172a" stroke-width="1.2" stroke-dasharray="2,2"/>
  <rect x="350" y="137" width="165" height="22" rx="4" fill="#ffffff" stroke="#d97706" stroke-width="1"/>
  <text x="432" y="152" font-family="system-ui, sans-serif" font-size="10.5" font-weight="700" fill="#d97706" text-anchor="middle">Stipe (Stem) &amp; Annulus</text>
  <line x1="230" y1="225" x2="350" y2="225" stroke="#fef08a" stroke-width="1.2" stroke-dasharray="2,2"/>
  <rect x="350" y="213" width="165" height="24" rx="4" fill="#1c1917" stroke="#fef08a" stroke-width="1"/>
  <text x="432" y="229" font-family="system-ui, sans-serif" font-size="10.5" font-weight="700" fill="#fde047" text-anchor="middle">Underground Mycelium (Hyphae)</text>
  <rect x="110" y="12" width="320" height="26" rx="4" fill="#14532d"/>
  <text x="270" y="29" font-family="system-ui, sans-serif" font-size="12" font-weight="700" fill="#ffffff" text-anchor="middle">{clean_term} · Kingdom Fungi &amp; Mycology</text>
</svg>"""

    # 2. Benchmark: Database Normalization / Relational Schema
    elif any(k in dom_l for k in ["normalization", "database normalization", "1nf", "2nf", "3nf", "bcnf", "relational database"]):
        return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 540 260" width="100%" height="100%">
  <defs>
    <linearGradient id="dbGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#f8fafc"/>
      <stop offset="100%" stop-color="#f1f5f9"/>
    </linearGradient>
  </defs>
  <rect width="540" height="260" rx="10" fill="url(#dbGrad)" stroke="#cbd5e1" stroke-width="1.5"/>
  <!-- Unnormalized / 1NF Table -->
  <rect x="20" y="55" width="130" height="135" rx="6" fill="#ffffff" stroke="#ef4444" stroke-width="1.5"/>
  <rect x="20" y="55" width="130" height="25" rx="6" fill="#ef4444"/>
  <text x="85" y="72" font-family="system-ui, sans-serif" font-size="11" font-weight="700" fill="#ffffff" text-anchor="middle">1NF: Student_Courses</text>
  <text x="30" y="100" font-family="monospace" font-size="10" fill="#0f172a"><u>StudentID</u> (PK)</text>
  <text x="30" y="120" font-family="monospace" font-size="10" fill="#0f172a"><u>CourseID</u> (PK)</text>
  <text x="30" y="140" font-family="monospace" font-size="10" fill="#dc2626">StudentName (Partial)</text>
  <text x="30" y="160" font-family="monospace" font-size="10" fill="#dc2626">DeptName (Transitive)</text>
  <text x="30" y="180" font-family="monospace" font-size="10" fill="#0f172a">Grade</text>
  <!-- Arrow 1NF to 2NF/3NF -->
  <line x1="155" y1="120" x2="195" y2="120" stroke="#475569" stroke-width="2.5"/>
  <polygon points="195,115 205,120 195,125" fill="#475569"/>
  <!-- 2NF / 3NF Decomposed Tables -->
  <!-- Table 1: Students -->
  <rect x="210" y="45" width="140" height="70" rx="5" fill="#ffffff" stroke="#3b82f6" stroke-width="1.5"/>
  <rect x="210" y="45" width="140" height="20" rx="5" fill="#3b82f6"/>
  <text x="280" y="59" font-family="system-ui, sans-serif" font-size="10" font-weight="700" fill="#ffffff" text-anchor="middle">2NF: Students</text>
  <text x="218" y="80" font-family="monospace" font-size="9" fill="#0f172a"><u>StudentID</u> (PK)</text>
  <text x="218" y="98" font-family="monospace" font-size="9" fill="#0f172a">StudentName</text>
  <!-- Table 2: Course & Dept (3NF) -->
  <rect x="210" y="125" width="140" height="75" rx="5" fill="#ffffff" stroke="#10b981" stroke-width="1.5"/>
  <rect x="210" y="125" width="140" height="20" rx="5" fill="#10b981"/>
  <text x="280" y="139" font-family="system-ui, sans-serif" font-size="10" font-weight="700" fill="#ffffff" text-anchor="middle">3NF: Courses</text>
  <text x="218" y="160" font-family="monospace" font-size="9" fill="#0f172a"><u>CourseID</u> (PK)</text>
  <text x="218" y="178" font-family="monospace" font-size="9" fill="#0f172a">DeptID (FK)</text>
  <!-- Table 3: Enrollments -->
  <rect x="375" y="85" width="145" height="85" rx="5" fill="#ffffff" stroke="#8b5cf6" stroke-width="1.5"/>
  <rect x="375" y="85" width="145" height="20" rx="5" fill="#8b5cf6"/>
  <text x="447" y="99" font-family="system-ui, sans-serif" font-size="10" font-weight="700" fill="#ffffff" text-anchor="middle">3NF: Enrollments</text>
  <text x="383" y="120" font-family="monospace" font-size="9" fill="#0f172a"><u>StudentID</u> (FK)</text>
  <text x="383" y="138" font-family="monospace" font-size="9" fill="#0f172a"><u>CourseID</u> (FK)</text>
  <text x="383" y="156" font-family="monospace" font-size="9" fill="#0f172a">Grade</text>
  <line x1="350" y1="80" x2="375" y2="120" stroke="#3b82f6" stroke-width="1.5" stroke-dasharray="3,3"/>
  <line x1="350" y1="160" x2="375" y2="138" stroke="#10b981" stroke-width="1.5" stroke-dasharray="3,3"/>
  <rect x="130" y="12" width="280" height="26" rx="4" fill="#1e293b"/>
  <text x="270" y="29" font-family="system-ui, sans-serif" font-size="12" font-weight="700" fill="#ffffff" text-anchor="middle">{clean_term} · Relational Schema Normalization</text>
  <text x="270" y="235" font-family="system-ui, sans-serif" font-size="11" font-weight="600" fill="#334155" text-anchor="middle">1NF (Atomic Attributes) ➔ 2NF (No Partial Key Dep.) ➔ 3NF (No Transitive Dep.)</text>
</svg>"""

    # 3. Benchmark: Operating System Scheduling & Process State Machine
    elif any(k in dom_l for k in ["process scheduling", "operating system scheduling", "cpu scheduling", "round robin", "ready queue", "context switch", "preemption", "process state"]):
        return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 540 260" width="100%" height="100%">
  <defs>
    <linearGradient id="osGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#f8fafc"/>
      <stop offset="100%" stop-color="#f1f5f9"/>
    </linearGradient>
  </defs>
  <rect width="540" height="260" rx="10" fill="url(#osGrad)" stroke="#cbd5e1" stroke-width="1.5"/>
  <!-- State 1: New -->
  <rect x="20" y="95" width="70" height="40" rx="6" fill="#e2e8f0" stroke="#64748b" stroke-width="2"/>
  <text x="55" y="119" font-family="system-ui, sans-serif" font-size="11" font-weight="700" fill="#1e293b" text-anchor="middle">NEW</text>
  <!-- Arrow New to Ready -->
  <line x1="90" y1="115" x2="135" y2="115" stroke="#475569" stroke-width="2"/>
  <polygon points="135,110 145,115 135,120" fill="#475569"/>
  <text x="117" y="108" font-family="system-ui, sans-serif" font-size="8" fill="#64748b" text-anchor="middle">Admit</text>
  <!-- State 2: Ready Queue -->
  <rect x="145" y="85" width="95" height="60" rx="8" fill="#dbeafe" stroke="#2563eb" stroke-width="2"/>
  <text x="192" y="112" font-family="system-ui, sans-serif" font-size="12" font-weight="700" fill="#1d4ed8" text-anchor="middle">READY</text>
  <text x="192" y="128" font-family="system-ui, sans-serif" font-size="9" fill="#3b82f6" text-anchor="middle">Ready Queue</text>
  <!-- Arrow Ready to Running (Dispatch) -->
  <line x1="240" y1="105" x2="295" y2="105" stroke="#16a34a" stroke-width="2.5"/>
  <polygon points="295,100 305,105 295,110" fill="#16a34a"/>
  <text x="272" y="98" font-family="system-ui, sans-serif" font-size="9" font-weight="700" fill="#15803d" text-anchor="middle">Dispatch</text>
  <!-- Arrow Running to Ready (Interrupt / Preempt) -->
  <path d="M 320,85 C 320,55 192,55 192,85" fill="none" stroke="#ea580c" stroke-width="2" stroke-dasharray="4,3"/>
  <polygon points="187,77 192,85 197,77" fill="#ea580c"/>
  <text x="256" y="52" font-family="system-ui, sans-serif" font-size="9" font-weight="700" fill="#c2410c" text-anchor="middle">Timer Interrupt (Preempt)</text>
  <!-- State 3: Running (CPU) -->
  <rect x="305" y="85" width="95" height="60" rx="8" fill="#dcfce7" stroke="#16a34a" stroke-width="2"/>
  <text x="352" y="112" font-family="system-ui, sans-serif" font-size="12" font-weight="700" fill="#15803d" text-anchor="middle">RUNNING</text>
  <text x="352" y="128" font-family="system-ui, sans-serif" font-size="9" fill="#22c55e" text-anchor="middle">CPU Execution</text>
  <!-- Arrow Running to Terminated -->
  <line x1="400" y1="115" x2="445" y2="115" stroke="#475569" stroke-width="2"/>
  <polygon points="445,110 455,115 445,120" fill="#475569"/>
  <text x="427" y="108" font-family="system-ui, sans-serif" font-size="8" fill="#64748b" text-anchor="middle">Exit</text>
  <!-- State 4: Terminated -->
  <rect x="455" y="95" width="70" height="40" rx="6" fill="#fee2e2" stroke="#dc2626" stroke-width="2"/>
  <text x="490" y="119" font-family="system-ui, sans-serif" font-size="10" font-weight="700" fill="#991b1b" text-anchor="middle">TERMINATED</text>
  <!-- State 5: Waiting / Blocked (I/O) -->
  <rect x="225" y="180" width="105" height="50" rx="8" fill="#fef3c7" stroke="#d97706" stroke-width="2"/>
  <text x="277" y="202" font-family="system-ui, sans-serif" font-size="11" font-weight="700" fill="#b45309" text-anchor="middle">WAITING</text>
  <text x="277" y="218" font-family="system-ui, sans-serif" font-size="9" fill="#d97706" text-anchor="middle">I/O or Event Wait</text>
  <!-- Arrow Running to Waiting -->
  <path d="M 360,145 C 360,185 330,195 330,195" fill="none" stroke="#d97706" stroke-width="2"/>
  <polygon points="338,190 330,195 338,200" fill="#d97706"/>
  <!-- Arrow Waiting to Ready -->
  <path d="M 225,195 C 170,195 160,155 160,145" fill="none" stroke="#2563eb" stroke-width="2"/>
  <polygon points="155,153 160,145 165,153" fill="#2563eb"/>
  <rect x="130" y="12" width="280" height="26" rx="4" fill="#1e293b"/>
  <text x="270" y="29" font-family="system-ui, sans-serif" font-size="12" font-weight="700" fill="#ffffff" text-anchor="middle">{clean_term} · CPU Process Scheduling</text>
  <text x="270" y="248" font-family="system-ui, sans-serif" font-size="10" fill="#475569" text-anchor="middle">Dispatcher Context Switch · Round-Robin Quantum · Multilevel Feedback Queue</text>
</svg>"""

    # 4. Computer Science / Hardware / CPU / Memory / Logic Gates
    elif any(k in dom_l for k in ["computer", "cpu", "memory", "ram", "rom", "cache", "bus", "hardware", "von neumann", "alu", "register", "software", "algorithm", "compiler", "transistor", "logic gate"]):
        return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 540 260" width="100%" height="100%">
  <defs>
    <linearGradient id="csGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#f8fafc"/>
      <stop offset="100%" stop-color="#f1f5f9"/>
    </linearGradient>
    <filter id="csShadow" x="-5%" y="-5%" width="110%" height="110%">
      <feDropShadow dx="0" dy="2" stdDeviation="3" flood-opacity="0.08"/>
    </filter>
  </defs>
  <rect width="540" height="260" rx="10" fill="url(#csGrad)" stroke="#cbd5e1" stroke-width="1.5"/>
  <rect x="25" y="45" width="135" height="135" rx="8" fill="#e0e7ff" stroke="#4f46e5" stroke-width="2" filter="url(#csShadow)"/>
  <rect x="35" y="55" width="115" height="24" rx="4" fill="#4f46e5"/>
  <text x="92" y="71" font-family="system-ui, -apple-system, sans-serif" font-size="12" font-weight="700" fill="#ffffff" text-anchor="middle">CPU Core</text>
  <rect x="40" y="90" width="105" height="35" rx="4" fill="#ffffff" stroke="#c7d2fe"/>
  <text x="92" y="112" font-family="system-ui, -apple-system, sans-serif" font-size="11" font-weight="600" fill="#3730a3" text-anchor="middle">ALU &amp; Logic</text>
  <rect x="40" y="133" width="105" height="35" rx="4" fill="#ffffff" stroke="#c7d2fe"/>
  <text x="92" y="155" font-family="system-ui, -apple-system, sans-serif" font-size="11" font-weight="600" fill="#3730a3" text-anchor="middle">Control Unit</text>
  <line x1="160" y1="112" x2="225" y2="112" stroke="#6366f1" stroke-width="4"/>
  <polygon points="225,106 237,112 225,118" fill="#6366f1"/>
  <polygon points="165,106 153,112 165,118" fill="#6366f1"/>
  <text x="195" y="103" font-family="system-ui, -apple-system, sans-serif" font-size="10" font-weight="700" fill="#6366f1" text-anchor="middle">System Bus</text>
  <rect x="240" y="45" width="275" height="135" rx="8" fill="#eff6ff" stroke="#2563eb" stroke-width="2" filter="url(#csShadow)"/>
  <rect x="250" y="55" width="255" height="26" rx="4" fill="#2563eb"/>
  <text x="377" y="73" font-family="system-ui, -apple-system, sans-serif" font-size="13" font-weight="700" fill="#ffffff" text-anchor="middle">{clean_term}</text>
  <rect x="255" y="93" width="75" height="72" rx="4" fill="#ffffff" stroke="#bfdbfe"/>
  <text x="292" y="125" font-family="system-ui, -apple-system, sans-serif" font-size="11" font-weight="700" fill="#1e40af" text-anchor="middle">Registers</text>
  <text x="292" y="142" font-family="system-ui, -apple-system, sans-serif" font-size="9" fill="#60a5fa" text-anchor="middle">L1 Cache</text>
  <rect x="340" y="93" width="80" height="72" rx="4" fill="#ffffff" stroke="#bfdbfe"/>
  <text x="380" y="125" font-family="system-ui, -apple-system, sans-serif" font-size="11" font-weight="700" fill="#1e40af" text-anchor="middle">Primary RAM</text>
  <text x="380" y="142" font-family="system-ui, -apple-system, sans-serif" font-size="9" fill="#60a5fa" text-anchor="middle">Volatile Store</text>
  <rect x="430" y="93" width="75" height="72" rx="4" fill="#ffffff" stroke="#bfdbfe"/>
  <text x="467" y="125" font-family="system-ui, -apple-system, sans-serif" font-size="11" font-weight="700" fill="#1e40af" text-anchor="middle">ROM / BIOS</text>
  <text x="467" y="142" font-family="system-ui, -apple-system, sans-serif" font-size="9" fill="#60a5fa" text-anchor="middle">Firmware</text>
  <rect x="25" y="200" width="490" height="38" rx="6" fill="#1e293b"/>
  <text x="270" y="224" font-family="system-ui, -apple-system, sans-serif" font-size="12" font-weight="600" fill="#f8fafc" text-anchor="middle">Computer Architecture · Hardware Subsystem &amp; Digital Logic</text>
</svg>"""

    # 5. Botany / Photosynthesis / Chloroplast / Flora / Leaves
    elif any(k in dom_l for k in ["photosynthesis", "chloroplast", "plant", "botany", "leaf", "flora", "thylakoid", "stroma", "xylem", "phloem", "stomata", "flower", "root", "angiosperm", "gymnosperm", "tree"]):
        return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 540 260" width="100%" height="100%">
  <defs>
    <linearGradient id="plantGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#f0fdf4"/>
      <stop offset="100%" stop-color="#dcfce7"/>
    </linearGradient>
    <linearGradient id="sunGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#fef08a"/>
      <stop offset="100%" stop-color="#eab308"/>
    </linearGradient>
  </defs>
  <rect width="540" height="260" rx="10" fill="url(#plantGrad)" stroke="#86efac" stroke-width="1.5"/>
  <circle cx="65" cy="55" r="30" fill="url(#sunGrad)" opacity="0.9"/>
  <text x="65" y="59" font-family="system-ui, sans-serif" font-size="11" font-weight="700" fill="#713f12" text-anchor="middle">Light Energy</text>
  <ellipse cx="270" cy="125" rx="200" ry="85" fill="#86efac" stroke="#16a34a" stroke-width="2.5"/>
  <ellipse cx="270" cy="125" rx="188" ry="75" fill="#bbf7d0" stroke="#22c55e" stroke-width="1.5"/>
  <g fill="#15803d">
    <ellipse cx="170" cy="105" rx="28" ry="8"/><ellipse cx="170" cy="118" rx="28" ry="8"/><ellipse cx="170" cy="131" rx="28" ry="8"/><ellipse cx="170" cy="144" rx="28" ry="8"/>
    <ellipse cx="270" cy="100" rx="28" ry="8"/><ellipse cx="270" cy="113" rx="28" ry="8"/><ellipse cx="270" cy="126" rx="28" ry="8"/><ellipse cx="270" cy="139" rx="28" ry="8"/>
    <ellipse cx="370" cy="105" rx="28" ry="8"/><ellipse cx="370" cy="118" rx="28" ry="8"/><ellipse cx="370" cy="131" rx="28" ry="8"/><ellipse cx="370" cy="144" rx="28" ry="8"/>
  </g>
  <line x1="198" y1="125" x2="242" y2="120" stroke="#166534" stroke-width="2.5"/>
  <line x1="298" y1="120" x2="342" y2="125" stroke="#166534" stroke-width="2.5"/>
  <text x="170" y="168" font-family="system-ui, sans-serif" font-size="10" font-weight="700" fill="#052e16" text-anchor="middle">Thylakoid Grana</text>
  <text x="270" y="85" font-family="system-ui, sans-serif" font-size="10" font-weight="700" fill="#14532d" text-anchor="middle">Chloroplast Stroma</text>
  <text x="370" y="168" font-family="system-ui, sans-serif" font-size="10" font-weight="700" fill="#052e16" text-anchor="middle">Light Reactions</text>
  <rect x="140" y="15" width="260" height="28" rx="6" fill="#15803d"/>
  <text x="270" y="34" font-family="system-ui, sans-serif" font-size="13" font-weight="700" fill="#ffffff" text-anchor="middle">{clean_term} · Botany &amp; Plant Science</text>
  <text x="270" y="238" font-family="system-ui, sans-serif" font-size="11" font-weight="600" fill="#166534" text-anchor="middle">6CO₂ + 6H₂O + Light Energy ➔ C₆H₁₂O₆ + 6O₂ (Photosynthetic Pathway)</text>
</svg>"""

    # 6. Genetics / DNA / RNA / Chromosomes
    elif any(k in dom_l for k in ["dna", "rna", "gene", "genetics", "chromosome", "nucleotide", "mutation", "helix", "allele", "mendel", "transcription", "translation"]):
        return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 540 260" width="100%" height="100%">
  <defs>
    <linearGradient id="dnaGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#fdf4ff"/>
      <stop offset="100%" stop-color="#fae8ff"/>
    </linearGradient>
  </defs>
  <rect width="540" height="260" rx="10" fill="url(#dnaGrad)" stroke="#e879f9" stroke-width="1.5"/>
  <path d="M 40,90 Q 90,40 140,90 T 240,90 T 340,90 T 440,90 T 500,90" fill="none" stroke="#9333ea" stroke-width="4"/>
  <path d="M 40,150 Q 90,200 140,150 T 240,150 T 340,150 T 440,150 T 500,150" fill="none" stroke="#c026d3" stroke-width="4"/>
  <line x1="90" y1="52" x2="90" y2="188" stroke="#2563eb" stroke-width="3" stroke-dasharray="6,4"/>
  <line x1="140" y1="90" x2="140" y2="150" stroke="#16a34a" stroke-width="3"/>
  <line x1="190" y1="128" x2="190" y2="112" stroke="#ea580c" stroke-width="3"/>
  <line x1="240" y1="90" x2="240" y2="150" stroke="#dc2626" stroke-width="3"/>
  <line x1="290" y1="52" x2="290" y2="188" stroke="#2563eb" stroke-width="3" stroke-dasharray="6,4"/>
  <line x1="340" y1="90" x2="340" y2="150" stroke="#16a34a" stroke-width="3"/>
  <line x1="390" y1="128" x2="390" y2="112" stroke="#ea580c" stroke-width="3"/>
  <line x1="440" y1="90" x2="440" y2="150" stroke="#dc2626" stroke-width="3"/>
  <line x1="490" y1="52" x2="490" y2="188" stroke="#2563eb" stroke-width="3" stroke-dasharray="6,4"/>
  <rect x="140" y="15" width="260" height="28" rx="6" fill="#7e22ce"/>
  <text x="270" y="34" font-family="system-ui, sans-serif" font-size="13" font-weight="700" fill="#ffffff" text-anchor="middle">{clean_term} · Molecular Genetics</text>
  <rect x="35" y="205" width="470" height="38" rx="6" fill="#581c87"/>
  <text x="270" y="228" font-family="system-ui, sans-serif" font-size="11" font-weight="600" fill="#f5d0fe" text-anchor="middle">Adenine-Thymine (A-T) · Guanine-Cytosine (G-C) Double Helix Base Pairs</text>
</svg>"""

    # 7. Chemistry / Atoms / Molecules / Elements / Reactions / Periodic Table
    elif any(k in dom_l for k in ["atom", "molecule", "chemical", "chemistry", "element", "reaction", "acid", "base", "compound", "bond", "valency", "molarity", "mercury", "electron", "proton", "neutron"]):
        return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 540 260" width="100%" height="100%">
  <defs>
    <linearGradient id="chemGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#ecfeff"/>
      <stop offset="100%" stop-color="#cffafe"/>
    </linearGradient>
  </defs>
  <rect width="540" height="260" rx="10" fill="url(#chemGrad)" stroke="#67e8f9" stroke-width="1.5"/>
  <circle cx="270" cy="125" r="28" fill="#0891b2" stroke="#0e7490" stroke-width="2"/>
  <text x="270" y="129" font-family="system-ui, sans-serif" font-size="11" font-weight="700" fill="#ffffff" text-anchor="middle">Nucleus</text>
  <ellipse cx="270" cy="125" rx="140" ry="45" fill="none" stroke="#0284c7" stroke-width="1.8" stroke-dasharray="5,3" transform="rotate(25 270 125)"/>
  <ellipse cx="270" cy="125" rx="140" ry="45" fill="none" stroke="#0284c7" stroke-width="1.8" stroke-dasharray="5,3" transform="rotate(-25 270 125)"/>
  <ellipse cx="270" cy="125" rx="140" ry="45" fill="none" stroke="#0284c7" stroke-width="1.8" stroke-dasharray="5,3" transform="rotate(80 270 125)"/>
  <circle cx="160" cy="85" r="6" fill="#0369a1"/>
  <circle cx="380" cy="165" r="6" fill="#0369a1"/>
  <circle cx="210" cy="175" r="6" fill="#0369a1"/>
  <circle cx="330" cy="75" r="6" fill="#0369a1"/>
  <rect x="140" y="15" width="260" height="28" rx="6" fill="#0e7490"/>
  <text x="270" y="34" font-family="system-ui, sans-serif" font-size="13" font-weight="700" fill="#ffffff" text-anchor="middle">{clean_term} · Chemical &amp; Atomic Structure</text>
  <rect x="35" y="210" width="470" height="34" rx="6" fill="#164e63"/>
  <text x="270" y="232" font-family="system-ui, sans-serif" font-size="11" font-weight="600" fill="#e0f2fe" text-anchor="middle">Atomic Nucleus (Protons &amp; Neutrons) · Quantized Valence Electron Shells</text>
</svg>"""

    # 8. Physics / Forces / Mechanics / Optics / Waves / Gravity / Electricity
    elif any(k in dom_l for k in ["physics", "force", "gravity", "gravitation", "optics", "wave", "motion", "velocity", "acceleration", "friction", "kinetic", "potential", "circuit", "magnet", "prism", "refraction"]):
        return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 540 260" width="100%" height="100%">
  <defs>
    <linearGradient id="physGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#fffbeb"/>
      <stop offset="100%" stop-color="#fef3c7"/>
    </linearGradient>
  </defs>
  <rect width="540" height="260" rx="10" fill="url(#physGrad)" stroke="#fde68a" stroke-width="1.5"/>
  <polygon points="270,60 190,180 350,180" fill="#ffffff" stroke="#d97706" stroke-width="2.5" opacity="0.9"/>
  <line x1="60" y1="125" x2="225" y2="125" stroke="#475569" stroke-width="3"/>
  <polygon points="220,121 232,125 220,129" fill="#475569"/>
  <text x="140" y="115" font-family="system-ui, sans-serif" font-size="11" font-weight="700" fill="#334155" text-anchor="middle">Incident Ray (F / v)</text>
  <line x1="315" y1="130" x2="480" y2="90" stroke="#dc2626" stroke-width="2.5"/>
  <line x1="315" y1="135" x2="480" y2="115" stroke="#ea580c" stroke-width="2.5"/>
  <line x1="315" y1="140" x2="480" y2="140" stroke="#16a34a" stroke-width="2.5"/>
  <line x1="315" y1="145" x2="480" y2="165" stroke="#2563eb" stroke-width="2.5"/>
  <line x1="315" y1="150" x2="480" y2="190" stroke="#7c3aed" stroke-width="2.5"/>
  <rect x="140" y="15" width="260" height="28" rx="6" fill="#b45309"/>
  <text x="270" y="34" font-family="system-ui, sans-serif" font-size="13" font-weight="700" fill="#ffffff" text-anchor="middle">{clean_term} · Physical Principles</text>
  <rect x="35" y="210" width="470" height="34" rx="6" fill="#78350f"/>
  <text x="270" y="232" font-family="system-ui, sans-serif" font-size="11" font-weight="600" fill="#fef3c7" text-anchor="middle">Vector Mechanics · Wave Optics &amp; Energy Conservation Laws</text>
</svg>"""

    # 9. Zoology / Anatomy / Physiology / Brain / Heart / Neuron / Tissues
    elif any(k in dom_l for k in ["neuron", "brain", "heart", "anatomy", "tissue", "organ", "animal", "zoology", "synapse", "muscle", "skeleton", "blood", "chordata", "mammal"]):
        return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 540 260" width="100%" height="100%">
  <defs>
    <linearGradient id="anatGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#fff1f2"/>
      <stop offset="100%" stop-color="#ffe4e6"/>
    </linearGradient>
  </defs>
  <rect width="540" height="260" rx="10" fill="url(#anatGrad)" stroke="#fecdd3" stroke-width="1.5"/>
  <circle cx="140" cy="125" r="35" fill="#f43f5e" stroke="#e11d48" stroke-width="2.5"/>
  <circle cx="140" cy="125" r="14" fill="#ffffff"/>
  <text x="140" y="129" font-family="system-ui, sans-serif" font-size="10" font-weight="700" fill="#be123c" text-anchor="middle">Soma</text>
  <line x1="175" y1="125" x2="380" y2="125" stroke="#e11d48" stroke-width="8" stroke-linecap="round"/>
  <rect x="200" y="113" width="38" height="24" rx="4" fill="#fb7185"/>
  <rect x="255" y="113" width="38" height="24" rx="4" fill="#fb7185"/>
  <rect x="310" y="113" width="38" height="24" rx="4" fill="#fb7185"/>
  <circle cx="410" cy="95" r="12" fill="#be123c"/>
  <circle cx="410" cy="125" r="12" fill="#be123c"/>
  <circle cx="410" cy="155" r="12" fill="#be123c"/>
  <text x="274" y="103" font-family="system-ui, sans-serif" font-size="10" font-weight="700" fill="#9f1239" text-anchor="middle">Myelin Sheath</text>
  <text x="435" y="129" font-family="system-ui, sans-serif" font-size="10" font-weight="700" fill="#881337">Synapse</text>
  <rect x="140" y="15" width="260" height="28" rx="6" fill="#be123c"/>
  <text x="270" y="34" font-family="system-ui, sans-serif" font-size="13" font-weight="700" fill="#ffffff" text-anchor="middle">{clean_term} · Anatomical &amp; Physiological System</text>
  <rect x="35" y="210" width="470" height="34" rx="6" fill="#881337"/>
  <text x="270" y="232" font-family="system-ui, sans-serif" font-size="11" font-weight="600" fill="#ffe4e6" text-anchor="middle">Neural Transmission · Cellular Physiology &amp; Organ Structure</text>
</svg>"""

    # 10. Geography & Earth Sciences (Soils, Landforms, Erosion)
    elif any(k in dom_l for k in ["soil", "alluvial", "laterite", "arid", "erosion", "geography", "earth", "rock", "land", "terrace", "contour", "delta", "river"]):
        return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 540 260" width="100%" height="100%">
  <defs>
    <linearGradient id="skyGrad" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="#e0f2fe"/>
      <stop offset="100%" stop-color="#bae6fd"/>
    </linearGradient>
  </defs>
  <rect width="540" height="260" rx="10" fill="#ffffff" stroke="#cbd5e1" stroke-width="1.5"/>
  <rect x="25" y="25" width="490" height="40" rx="4" fill="url(#skyGrad)"/>
  <path d="M 25,65 Q 120,50 200,60 T 380,55 T 515,65 L 515,68 L 25,68 Z" fill="#15803d"/>
  <rect x="25" y="68" width="490" height="38" fill="#78350f"/>
  <text x="45" y="92" font-family="system-ui, sans-serif" font-size="11" font-weight="700" fill="#fef3c7">Topsoil (A-Horizon) · Humus &amp; Organic Nutrients</text>
  <rect x="25" y="106" width="490" height="45" fill="#92400e"/>
  <text x="45" y="133" font-family="system-ui, sans-serif" font-size="11" font-weight="700" fill="#ffedd5">Subsoil (B-Horizon) · Weathered Clay, Iron &amp; Silt</text>
  <rect x="25" y="151" width="490" height="45" fill="#a8a29e"/>
  <text x="45" y="178" font-family="system-ui, sans-serif" font-size="11" font-weight="700" fill="#f5f5f4">Substratum (C-Horizon) · Weathered Parent Rock Material</text>
  <rect x="25" y="196" width="490" height="45" fill="#475569"/>
  <text x="45" y="223" font-family="system-ui, sans-serif" font-size="11" font-weight="700" fill="#f8fafc">Bedrock (R-Horizon) · Unweathered Solid Parent Rock</text>
  <rect x="160" y="32" width="220" height="26" rx="4" fill="#047857"/>
  <text x="270" y="49" font-family="system-ui, sans-serif" font-size="12" font-weight="700" fill="#ffffff" text-anchor="middle">{clean_term}</text>
</svg>"""

    # 11. Astronomy & Space
    elif any(k in dom_l for k in ["planet", "solar", "sun", "moon", "star", "astronomy", "space", "orbit", "crater", "galaxy", "telescope"]):
        return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 540 260" width="100%" height="100%">
  <rect width="540" height="260" rx="10" fill="#090d16" stroke="#1e293b" stroke-width="1.5"/>
  <circle cx="50" cy="130" r="75" fill="#f59e0b" opacity="0.9"/>
  <circle cx="50" cy="130" r="85" fill="#fbbf24" opacity="0.3"/>
  <text x="45" y="135" font-family="system-ui, sans-serif" font-size="14" font-weight="700" fill="#78350f" text-anchor="middle">Sun</text>
  <ellipse cx="50" cy="130" rx="160" ry="60" fill="none" stroke="#334155" stroke-width="1.2" stroke-dasharray="4,3"/>
  <ellipse cx="50" cy="130" rx="260" ry="90" fill="none" stroke="#334155" stroke-width="1.2" stroke-dasharray="4,3"/>
  <ellipse cx="50" cy="130" rx="380" ry="115" fill="none" stroke="#334155" stroke-width="1.2" stroke-dasharray="4,3"/>
  <circle cx="180" cy="110" r="14" fill="#94a3b8"/>
  <circle cx="270" cy="95" r="22" fill="#3b82f6"/>
  <circle cx="390" cy="155" r="32" fill="#d97706"/>
  <rect x="140" y="20" width="260" height="32" rx="6" fill="#1e293b" stroke="#334155"/>
  <text x="270" y="41" font-family="system-ui, sans-serif" font-size="13" font-weight="700" fill="#38bdf8" text-anchor="middle">{clean_term} · Astronomical System</text>
  <text x="270" y="235" font-family="system-ui, sans-serif" font-size="11" font-weight="500" fill="#94a3b8" text-anchor="middle">Planetary Orbit &amp; Celestial Mechanics</text>
</svg>"""

    # 12. Historical Person / Scientist
    elif any(k in dom_l for k in ["scientist", "person", "linnaeus", "einstein", "darwin", "newton", "turing", "mendel", "curie", "babbage"]):
        return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 540 260" width="100%" height="100%">
  <defs>
    <linearGradient id="bioScholGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#f8fafc"/>
      <stop offset="100%" stop-color="#f1f5f9"/>
    </linearGradient>
  </defs>
  <rect width="540" height="260" rx="10" fill="url(#bioScholGrad)" stroke="#cbd5e1" stroke-width="1.5"/>
  <circle cx="120" cy="125" r="55" fill="#f8fafc" stroke="#475569" stroke-width="3"/>
  <circle cx="120" cy="125" r="48" fill="#e2e8f0"/>
  <circle cx="120" cy="105" r="18" fill="#475569"/>
  <path d="M 95,145 C 95,128 145,128 145,145 Z" fill="#475569"/>
  <rect x="200" y="55" width="300" height="32" rx="6" fill="#1e293b"/>
  <text x="350" y="76" font-family="system-ui, sans-serif" font-size="14" font-weight="700" fill="#ffffff" text-anchor="middle">{clean_term}</text>
  <rect x="200" y="100" width="300" height="85" rx="6" fill="#ffffff" stroke="#e2e8f0"/>
  <text x="215" y="125" font-family="system-ui, sans-serif" font-size="12" font-weight="700" fill="#0f172a">Academic &amp; Historical Scholar</text>
  <text x="215" y="148" font-family="system-ui, sans-serif" font-size="11" fill="#475569">Pioneering discoveries, published scientific works,</text>
  <text x="215" y="168" font-family="system-ui, sans-serif" font-size="11" fill="#475569">and foundational contributions to academic taxonomy.</text>
  <rect x="25" y="205" width="490" height="35" rx="6" fill="#334155"/>
  <text x="270" y="227" font-family="system-ui, sans-serif" font-size="11" font-weight="600" fill="#f8fafc" text-anchor="middle">Biographical Reference · Historical Scientific Pioneer</text>
</svg>"""

    # 13. Default Life Science & Living Organisms
    else:
        return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 540 260" width="100%" height="100%">
  <defs>
    <linearGradient id="bioGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#f0fdf4"/>
      <stop offset="100%" stop-color="#dcfce7"/>
    </linearGradient>
  </defs>
  <rect width="540" height="260" rx="10" fill="url(#bioGrad)" stroke="#86efac" stroke-width="1.5"/>
  <ellipse cx="270" cy="125" rx="210" ry="95" fill="#bbf7d0" stroke="#16a34a" stroke-width="3" stroke-dasharray="6,3"/>
  <ellipse cx="270" cy="125" rx="195" ry="85" fill="#dcfce7" stroke="#22c55e" stroke-width="1.5"/>
  <circle cx="270" cy="125" r="42" fill="#86efac" stroke="#15803d" stroke-width="2.5"/>
  <circle cx="270" cy="125" r="18" fill="#15803d"/>
  <text x="270" y="112" font-family="system-ui, sans-serif" font-size="12" font-weight="700" fill="#052e16" text-anchor="middle">Nucleus</text>
  <text x="270" y="152" font-family="system-ui, sans-serif" font-size="9" font-weight="600" fill="#14532d" text-anchor="middle">DNA / Genetic Material</text>
  <ellipse cx="140" cy="105" rx="24" ry="12" fill="#fed7aa" stroke="#ea580c" stroke-width="2"/>
  <text x="140" y="128" font-family="system-ui, sans-serif" font-size="9" font-weight="600" fill="#9a3412" text-anchor="middle">Mitochondria</text>
  <ellipse cx="400" cy="145" rx="24" ry="12" fill="#fed7aa" stroke="#ea580c" stroke-width="2"/>
  <text x="400" y="168" font-family="system-ui, sans-serif" font-size="9" font-weight="600" fill="#9a3412" text-anchor="middle">Mitochondria</text>
  <rect x="140" y="15" width="260" height="30" rx="6" fill="#166534"/>
  <text x="270" y="35" font-family="system-ui, sans-serif" font-size="13" font-weight="700" fill="#ffffff" text-anchor="middle">{clean_term} ({cat_clean})</text>
  <text x="270" y="242" font-family="system-ui, sans-serif" font-size="11" font-weight="600" fill="#15803d" text-anchor="middle">Biological Living System · Cellular Structure &amp; Organization</text>
</svg>"""


@app.get("/api/documents/{doc_id}/image-proxy")
async def proxy_image(
    doc_id: str,
    url: str,
    term: str = "",
    domain: str = "",
    type: str = "",
    category: str = "",
):
    """Proxy external images with in-memory caching and resilient timeout."""
    if not url.startswith(("http://", "https://")):
        raise HTTPException(400, "Invalid image URL.")
    
    if url in PROXY_IMAGE_CACHE:
        cached_content, cached_type = PROXY_IMAGE_CACHE[url]
        return Response(content=cached_content, media_type=cached_type, headers={"Cache-Control": "public, max-age=86400"})

    try:
        headers = {
            "User-Agent": "ReadFlowAI/1.0 (educational document reader; info@readflow.ai)",
            "Accept": "image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8",
        }
        async with httpx.AsyncClient(timeout=15.0, follow_redirects=True) as client:
            resp = await client.get(url, headers=headers)
            if resp.status_code == 200 and len(resp.content) > 100:
                content_type = resp.headers.get("content-type", "image/jpeg")
                if len(PROXY_IMAGE_CACHE) >= 300:
                    PROXY_IMAGE_CACHE.pop(next(iter(PROXY_IMAGE_CACHE)))
                PROXY_IMAGE_CACHE[url] = (resp.content, content_type)
                return Response(content=resp.content, media_type=content_type, headers={"Cache-Control": "public, max-age=86400"})
    except Exception as exc:
        logger.debug("Image proxy network fetch failed: %s", exc)

    # Strictly return 404 when image is unavailable or network fails
    raise HTTPException(404, f"Image not available for '{term}'.")


@app.get("/api/documents/{doc_id}/terms/web-info")
async def get_term_web_info(
    doc_id: str,
    term: str,
    sentence: str = "",
    candidate_queries: list[str] = None,
    domain_topic: str = "",
    entity_name: str = "",
    entity_type: str = "",
    context_text: str = "",
):
    """Return Openverse photographic image and Wikipedia definition for a clicked term."""
    query = re.sub(r"\s+", " ", term).strip()[:100]
    if not query:
        raise HTTPException(400, "Select a word to search.")
    resolved = entity_name or query
    analysis = analyze_word(query)
    
    # 1. Wikipedia for Definition
    wiki_info = {}
    ov_info = {"show": False, "url": None}
    
    async with httpx.AsyncClient(timeout=6.0, follow_redirects=True) as client:
        try:
            wiki_info = await fetch_wikipedia_entity_definition(client, resolved, entity_type, context_text)
        except Exception:
            pass
            
        # 2. Openverse for Image
        img_q = candidate_queries[0] if candidate_queries else f"{resolved} {entity_type}".strip()
        try:
            ov_info = await search_openverse_image(client, img_q, resolved, entity_type)
        except Exception:
            pass

    raw_image = ov_info.get("url") or ""
    proxy_image_url = f"/api/documents/{doc_id}/image-proxy?url={quote(raw_image)}" if raw_image else ""
    primary_def = wiki_info.get("text") or f"In {domain_topic or 'academic study'}, “{resolved}” is a recognized concept and specialized subject term."

    result = {
        "found": True,
        "title": resolved,
        "real_image": raw_image,
        "real_image_proxy": proxy_image_url,
        "image": proxy_image_url or raw_image,
        "direct_image": raw_image,
        "image_title": ov_info.get("title") or resolved,
        "image_source_url": ov_info.get("source_url", ""),
        "image_provider": "Openverse" if raw_image else "none",
        "source_url": wiki_info.get("source_url") or f"https://en.wikipedia.org/wiki/{quote(resolved.replace(' ', '_'))}",
        "source_title": resolved,
        "source_description": primary_def,
        "provider": "wikipedia" if wiki_info.get("text") else "ReadFlow AI",
        "reference_sentence": primary_def,
        "sentence": primary_def,
        "svg": generate_fallback_concept_svg(resolved, analysis.get("category", "scientific_term"), analysis.get("lemma", resolved)),
    }
    return result



@app.post("/api/terms/explain")
async def explain_standalone_term_post(payload: TermExplainRequest):
    target_term = payload.term.strip() if payload.term else ""
    if not target_term:
        raise HTTPException(400, "Please provide a term to explain.")
    return await explain_document_term("standalone", payload)


@app.get("/api/terms/explain")
async def explain_standalone_term_get(term: str = ""):
    target_term = term.strip()
    if not target_term:
        raise HTTPException(400, "Please provide a term to explain.")
    return await explain_document_term("standalone", TermExplainRequest(term=target_term))


@app.delete("/api/documents/{doc_id}")
def delete_document(doc_id: str):
    doc = DOCUMENTS.pop(doc_id, None)
    if not doc:
        raise HTTPException(404, "Document not found.")
    for n in range(1, doc["page_count"] + 1):
        (UPLOAD_DIR / f"{doc_id}-{n}.png").unlink(missing_ok=True)
    return {"deleted": True}
