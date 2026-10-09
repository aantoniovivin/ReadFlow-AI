"""Fast, local token analysis for clicked document words."""

from __future__ import annotations

import re
from functools import lru_cache


@lru_cache(maxsize=1)
def _load_nlp():
    try:
        import spacy

        return spacy.load("en_core_web_sm", disable=["parser", "ner"])
    except (ImportError, OSError):
        return None


COMMON_ADJECTIVES = {
    "sound", "scientific", "valid", "clear", "fast", "direct", "simple", "general",
    "special", "rich", "major", "minor", "broad", "deep", "sharp", "smooth",
    "soft", "strong", "weak", "pure", "raw", "neat", "plain", "dry", "wet",
    "hot", "cold", "true", "false", "fair", "fine", "proper", "novel", "early",
    "late", "great", "small", "large", "high", "low", "modern", "ancient",
    "primary", "secondary", "tertiary", "initial", "final", "constant", "variable",
    "similar", "different", "distinct", "unique", "common", "rare", "frequent",
    "equal", "unequal", "positive", "negative", "neutral", "active", "passive",
    "complex", "basic", "fundamental", "critical", "essential", "primary"
}

COMMON_ADVERBS = {
    "very", "more", "most", "almost", "nearly", "quite", "rather", "extremely",
    "highly", "fairly", "completely", "totally", "absolutely", "partially",
    "always", "never", "often", "seldom", "rarely", "sometimes", "usually",
    "generally", "predominantly", "primarily", "largely", "mainly", "well", "badly"
}


COMMON_AL_NOUNS = {
    "animal", "animals", "manual", "manuals", "journal", "journals", "crystal", "crystals",
    "mineral", "minerals", "cereal", "cereals", "signal", "signals", "metal", "metals",
    "portal", "portals", "canal", "canals", "coral", "corals", "pedal", "pedals",
    "mammal", "mammals", "individual", "individuals", "material", "materials",
    "chemical", "chemicals", "capital", "capitals", "hospital", "hospitals"
}

COMMON_CONNECTORS = {
    "however", "therefore", "furthermore", "moreover", "consequently", "nevertheless",
    "nonetheless", "accordingly", "otherwise", "hence", "thus", "meanwhile", "instead",
    "besides", "incidentally", "namely", "afterwards", "indeed", "additionally"
}


def _fallback_analysis(word: str, context: str = "") -> tuple[str, str]:
    value = word.casefold().strip()
    lemma = value
    pos = "NOUN"

    if value in COMMON_CONNECTORS:
        return lemma, "CONJ"
    if value in COMMON_ADVERBS:
        return lemma, "ADV"
    if value in COMMON_ADJECTIVES:
        # If context is provided, check if it's used as an adjective
        if context:
            ctx_lower = context.lower()
            # E.g. "more sound and scientific", "sound placement", "sound method"
            if re.search(rf"\b(?:more|very|most|highly|strictly|and|or)\s+{re.escape(value)}\b", ctx_lower) or \
               re.search(rf"\b{re.escape(value)}\s+[a-z]+(?:tion|ment|ing|ty|cy|ness|s|ance|ence|gy|my|y)\b", ctx_lower):
                return lemma, "ADJ"
        return lemma, "ADJ"

    if len(value) > 5 and value.endswith("ies"):
        lemma = value[:-3] + "y"
        pos = "NOUN"
    elif len(value) > 5 and value.endswith("ing"):
        lemma = value[:-3]
        if len(lemma) > 2 and lemma[-1] == lemma[-2]:
            lemma = lemma[:-1]
        pos = "VERB"
    elif len(value) > 4 and value.endswith("ed"):
        lemma = value[:-2]
        if lemma.endswith("i"):
            lemma = lemma[:-1] + "y"
        pos = "VERB"
    elif len(value) > 3 and value.endswith("s") and not value.endswith(("ss", "us", "is")):
        lemma = value[:-1]
    elif value in COMMON_AL_NOUNS:
        pos = "NOUN"
    elif re.search(r"(?:ous|ful|less|ive|able|ible|al|ic|ish|ary|ory|lar)$", value):
        pos = "ADJ"
    elif re.search(r"(?:ly)$", value):
        pos = "ADV"
    return lemma, pos


def analyze_word(word: str, context: str = "") -> dict[str, str]:
    """Return the word's lemma and part of speech using spaCy when installed, with contextual fallback."""
    nlp = _load_nlp()
    if nlp is not None:
        text_to_parse = f"{context}" if context and len(context) < 300 else word
        tokens = [token for token in nlp(text_to_parse) if not token.is_space and not token.is_punct]
        if tokens:
            target_token = next((t for t in tokens if t.text.lower() == word.lower()), tokens[0])
            lemma = target_token.lemma_ if target_token.lemma_ and target_token.lemma_ != "-PRON-" else target_token.text
            return {"lemma": lemma, "part_of_speech": target_token.pos_ or "X", "nlp_engine": "spacy"}
    lemma, pos = _fallback_analysis(word, context=context)
    return {"lemma": lemma, "part_of_speech": pos, "nlp_engine": "local_fallback"}
