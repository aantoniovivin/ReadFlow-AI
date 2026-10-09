import unittest
from fastapi.testclient import TestClient
from main import app

class TestE2EApi(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)

    def test_health_or_root(self):
        response = self.client.get("/api/health")
        # Check health endpoint if exists
        self.assertIn(response.status_code, [200, 404])

    def test_document_upload_and_term_explain_flow(self):
        # Create a mock document directly via API or test term explain
        # 1. Create a dummy text/pdf file for upload
        import io
        file_content = b"""
        The Solar System and Inner Planets
        Mercury is the closest planet to the Sun. It has a cratered surface and thin exosphere.
        In contrast, in a chemistry laboratory, mercury is a heavy silvery element that is liquid at room temperature.
        Apple Inc. develops the iPhone and macOS operating systems, while farmers harvest the apple fruit in autumn.
        """
        files = {"file": ("solar_system.txt", io.BytesIO(file_content), "text/plain")}
        upload_resp = self.client.post("/api/documents", files=files)
        self.assertEqual(upload_resp.status_code, 200)
        doc_data = upload_resp.json()
        self.assertIn("id", doc_data)
        doc_id = doc_data["id"]

        # 2. Test explaining 'Mercury' in astronomy context
        explain_resp_1 = self.client.post(
            f"/api/documents/{doc_id}/terms/explain",
            json={
                "term": "Mercury",
                "sentence": "Mercury is the closest planet to the Sun. It has a cratered surface and thin exosphere.",
                "page": 1,
                "section_index": 0
            }
        )
        self.assertEqual(explain_resp_1.status_code, 200)
        res_1 = explain_resp_1.json()
        self.assertEqual(res_1["word"], "Mercury")
        self.assertIn("planet", res_1["entity_name"].lower() + " " + res_1["entity_type"].lower() + " " + res_1["disambiguation"].lower())
        self.assertIsNotNone(res_1.get("definition"))
        print(f"\n[E2E Test 1 - Mercury Planet] Resolved to: {res_1.get('entity_name')} ({res_1.get('entity_type')}), Image: {res_1.get('real_image') or (res_1.get('image') or {}).get('url')}")

        # 3. Test explaining 'Mercury' in chemistry context
        explain_resp_2 = self.client.post(
            f"/api/documents/{doc_id}/terms/explain",
            json={
                "term": "Mercury",
                "sentence": "In a chemistry laboratory, mercury is a heavy silvery element that is liquid at room temperature.",
                "page": 1,
                "section_index": 0
            }
        )
        self.assertEqual(explain_resp_2.status_code, 200)
        res_2 = explain_resp_2.json()
        self.assertIn("element", res_2["entity_name"].lower() + " " + res_2["entity_type"].lower() + " " + res_2["disambiguation"].lower())
        print(f"[E2E Test 2 - Mercury Element] Resolved to: {res_2.get('entity_name')} ({res_2.get('entity_type')}), Image: {res_2.get('real_image') or (res_2.get('image') or {}).get('url')}")

        # 4. Test explaining 'Apple' in tech context
        explain_resp_3 = self.client.post(
            f"/api/documents/{doc_id}/terms/explain",
            json={
                "term": "Apple",
                "sentence": "Apple Inc. develops the iPhone and macOS operating systems.",
                "page": 1,
                "section_index": 0
            }
        )
        self.assertEqual(explain_resp_3.status_code, 200)
        res_3 = explain_resp_3.json()
        self.assertIn("apple inc", res_3["entity_name"].lower() + " " + res_3["entity_type"].lower() + " " + str(res_3.get("entity", {})))
        print(f"[E2E Test 3 - Apple Inc.] Resolved to: {res_3.get('entity_name')} ({res_3.get('entity_type')}), Image: {res_3.get('real_image') or (res_3.get('image') or {}).get('url')}")

        # 5. Test manual disambiguation selection
        explain_resp_4 = self.client.post(
            f"/api/documents/{doc_id}/terms/explain",
            json={
                "term": "Mercury",
                "sentence": "Look up Mercury.",
                "resolved_entity": "Mercury (planet)",
                "entity_type": "planet",
                "page": 1,
                "section_index": 0
            }
        )
        self.assertEqual(explain_resp_4.status_code, 200)
        res_4 = explain_resp_4.json()
        self.assertEqual(res_4["entity_name"], "Mercury (planet)")
        print(f"[E2E Test 4 - Manual Disambiguation] Resolved to: {res_4.get('entity_name')}, Confidence: {res_4.get('confidence')}")

        # 6. Test abstract non-visual term (show_image = False, image = None)
        explain_resp_5 = self.client.post(
            f"/api/documents/{doc_id}/terms/explain",
            json={
                "term": "implementation",
                "sentence": "The implementation methodology followed standard engineering guidelines.",
                "page": 1,
                "section_index": 0
            }
        )
        self.assertEqual(explain_resp_5.status_code, 200)
        res_5 = explain_resp_5.json()
        self.assertFalse(res_5.get("show_image", True))
        self.assertFalse(res_5.get("image", {}).get("show", True))
        self.assertIsNone(res_5.get("image", {}).get("url"))
        self.assertEqual(res_5.get("real_image"), "")
        print(f"[E2E Test 5 - Implementation] Explanation only, show_image: {res_5.get('show_image')}")

        # 7. Test 'sound' as adjective in taxonomy passage (show_image = False, NO incorrect image generated)
        explain_resp_6 = self.client.post(
            f"/api/documents/{doc_id}/terms/explain",
            json={
                "term": "sound",
                "sentence": "to facilitate more sound and scientific placement of various taxa",
                "page": 1,
                "section_index": 0
            }
        )
        self.assertEqual(explain_resp_6.status_code, 200)
        res_6 = explain_resp_6.json()
        self.assertFalse(res_6.get("show_image", True))
        self.assertFalse(res_6.get("image", {}).get("show", True))
        self.assertIsNone(res_6.get("image", {}).get("url"))
        self.assertEqual(res_6.get("real_image"), "")
        print(f"[E2E Test 6 - Sound (Adjective in Taxonomy)] show_image: {res_6.get('show_image')}, image: {res_6.get('image')}")

        # 8. Test 'scientific' adjective (show_image = False)
        explain_resp_7 = self.client.post(
            f"/api/documents/{doc_id}/terms/explain",
            json={
                "term": "scientific",
                "sentence": "scientific placement of various taxa",
                "page": 1,
                "section_index": 0
            }
        )
        self.assertEqual(explain_resp_7.status_code, 200)
        res_7 = explain_resp_7.json()
        self.assertFalse(res_7.get("show_image", True))
        self.assertFalse(res_7.get("image", {}).get("show", True))
        print(f"[E2E Test 7 - Scientific (Adjective)] show_image: {res_7.get('show_image')}")


if __name__ == "__main__":
    unittest.main()

