import asyncio
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_random_words():
    test_terms = [
        "Photosynthesis",
        "Gravity",
        "Atom",
        "Neuron",
        "CPU",
        "Alluvial soil",
        "Saturn",
        "Carl Linnaeus",
        "DNA",
        "Organism",
        "Primary memory",
        "Compiler",
        "Telescope"
    ]
    print("\n--- Testing Random Words Standalone Explanation & Visual Generation ---")
    for word in test_terms:
        resp = client.post("/api/terms/explain", json={"term": word})
        assert resp.status_code == 200, f"Failed for {word}: {resp.text}"
        data = resp.json()
        
        # Check definition
        assert data.get("definition"), f"Missing definition for {word}"
        def_text = data["definition"].get("text") if isinstance(data["definition"], dict) else data["definition"]
        assert len(def_text) > 10, f"Definition too short for {word}"
        
        # Check image object
        assert "image" in data
        assert data["image"]["show"] is True, f"Image should be shown for {word}"
        assert data["image"]["url"] is not None
        assert data["image"]["proxy_url"] is not None
        
        # Test proxy rendering
        proxy_resp = client.get(data["image"]["proxy_url"])
        assert proxy_resp.status_code == 200
        assert len(proxy_resp.content) > 100
        
        print(f"PASS: '{word}' -> Def: '{def_text[:60]}...' | Image Source: {data['image']['source']} | Proxy HTTP: {proxy_resp.status_code}")

if __name__ == "__main__":
    test_random_words()
