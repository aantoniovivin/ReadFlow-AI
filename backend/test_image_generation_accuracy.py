import asyncio
from fastapi.testclient import TestClient

from main import (
    app,
    build_educational_drawing_prompt,
    generate_fallback_concept_svg,
)

client = TestClient(app)

BENCHMARK_CONCEPTS = [
    {
        "term": "neural networks",
        "entity_type": "Computer Science & Artificial Intelligence",
        "expected_prompt_keywords": ["input layer", "hidden", "output", "weighted", "white background"],
        "expected_svg_keywords": ["Neural", "Input Layer", "Hidden Layers"],
    },
    {
        "term": "photosynthesis",
        "entity_type": "Plant Biology",
        "expected_prompt_keywords": ["chloroplast", "thylakoid", "calvin cycle", "white background"],
        "expected_svg_keywords": ["Chloroplast", "Thylakoid Grana", "Stroma"],
    },
    {
        "term": "database normalization",
        "entity_type": "Database Architecture",
        "expected_prompt_keywords": ["1nf", "2nf", "3nf", "decomposition", "white background"],
        "expected_svg_keywords": ["1NF", "2NF", "3NF", "Normalization"],
    },
    {
        "term": "operating system scheduling",
        "entity_type": "Computer Systems",
        "expected_prompt_keywords": ["ready queue", "running", "dispatcher", "context switch", "white background"],
        "expected_svg_keywords": ["READY", "RUNNING", "WAITING", "TERMINATED"],
    },
]


def test_build_educational_drawing_prompt_benchmarks():
    print("\n--- 1. Testing Component-Level Educational Prompt Generation ---")
    for item in BENCHMARK_CONCEPTS:
        prompt = build_educational_drawing_prompt(
            term=item["term"],
            entity_type=item["entity_type"],
            domain=item["entity_type"],
            sentence=f"The study of {item['term']} is essential.",
            technical_explanation=f"Technical architectural principles of {item['term']}.",
        )
        assert len(prompt) > 40, f"Prompt too short for {item['term']}: {prompt}"
        prompt_lower = prompt.lower()
        for kw in item["expected_prompt_keywords"]:
            assert kw.lower() in prompt_lower, f"Missing '{kw}' in prompt for {item['term']}: {prompt}"
        print(f"PASS Prompt for '{item['term']}':\n  {prompt[:120]}...")


def test_generate_fallback_concept_svg():
    print("\n--- 2. Testing Multi-Discipline SVG Diagram Generator ---")
    for item in BENCHMARK_CONCEPTS:
        svg = generate_fallback_concept_svg(item["term"], domain=item["entity_type"])
        assert svg.startswith("<svg") and svg.endswith("</svg>"), f"Invalid SVG format for {item['term']}"
        assert 'viewBox="0 0 540 260"' in svg
        for kw in item["expected_svg_keywords"]:
            assert kw in svg, f"Missing '{kw}' in generated SVG for {item['term']}"
        print(f"PASS SVG for '{item['term']}' ({len(svg)} bytes) with elements: {item['expected_svg_keywords']}")


def test_api_terms_explain_endpoint():
    print("\n--- 3. Testing POST /api/terms/explain Benchmark Responses ---")
    for item in BENCHMARK_CONCEPTS:
        resp = client.post("/api/terms/explain", json={"term": item["term"], "sentence": f"Overview of {item['term']}."})
        assert resp.status_code == 200, f"Failed for {item['term']}: {resp.text}"
        data = resp.json()

        # Check top-level structured contracts
        assert "entity" in data
        assert "definition" in data
        assert "image" in data
        assert "explanation" in data

        # Check definition
        definition_text = data["definition"].get("text", "")
        assert len(definition_text) > 10, f"Definition empty for {item['term']}"

        # Check image structure & attribution
        image_obj = data["image"]
        assert "show" in image_obj
        assert "url" in image_obj
        assert "source" in image_obj
        assert "author" in image_obj
        assert "license" in image_obj

        if image_obj["show"]:
            assert image_obj["source"] in ["Wikimedia Commons", "Openverse", "Pollinations AI"]
            assert image_obj["url"].startswith("http")

        # Test image proxy rendering
        if image_obj.get("proxy_url"):
            proxy_resp = client.get(image_obj["proxy_url"])
            assert proxy_resp.status_code == 200
            assert len(proxy_resp.content) > 100

        print(f"PASS API for '{item['term']}' -> Def: '{definition_text[:50]}...' | Source: {image_obj['source']} ({image_obj.get('license', '')})")


def test_api_terms_explain_get_method():
    print("\n--- 4. Testing GET /api/terms/explain Endpoint ---")
    resp = client.get("/api/terms/explain?term=photosynthesis")
    assert resp.status_code == 200
    data = resp.json()
    assert "photosynthesis" in data["entity_name"].lower()
    assert data["definition"]["text"]
    print("PASS GET /api/terms/explain?term=photosynthesis")


if __name__ == "__main__":
    test_build_educational_drawing_prompt_benchmarks()
    test_generate_fallback_concept_svg()
    test_api_terms_explain_endpoint()
    test_api_terms_explain_get_method()
    print("\n ALL 4 IMAGE GENERATION ACCURACY BENCHMARK SUITES PASSED (100%)!")
