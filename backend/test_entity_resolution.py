import unittest
from unittest.mock import AsyncMock, patch, MagicMock
from ai_service import resolve_disambiguated_term_queries, should_concept_show_image
from main import is_valid_image_url, is_openverse_result_relevant, search_openverse_image, fetch_wikipedia_entity_definition


class TestEntityResolutionAndVisualDecision(unittest.TestCase):
    # 1. Mango
    def test_mango_entity_and_visual(self):
        context = "Mango is a tropical fruit widely cultivated across India and Asia."
        res = resolve_disambiguated_term_queries("Mango", context, "Botany and Agriculture")
        self.assertEqual(res["entity"], "Mango")
        self.assertIn("fruit", res["entity_type"].lower())
        self.assertTrue(res["show_image"])
        self.assertIn("mango", res["image_query"].lower())
        self.assertIn("fruit", res["image_query"].lower())

    # 2. Mercury in astronomy context
    def test_mercury_astronomy_context(self):
        context = "Mercury is the smallest planet in the Solar System and the closest to the Sun with cratered surface and thin atmosphere."
        res = resolve_disambiguated_term_queries("Mercury", context, "Astronomy and Planetary Science")
        self.assertEqual(res["entity"], "Mercury (planet)")
        self.assertEqual(res["entity_type"], "planet")
        self.assertTrue(res["show_image"])
        self.assertIn("planet", res["image_query"].lower())

    # 3. Mercury in chemistry context
    def test_mercury_chemistry_context(self):
        context = "Mercury is a dense chemical element with atomic number 80 that remains liquid at standard temperature and pressure."
        res = resolve_disambiguated_term_queries("Mercury", context, "Chemistry and Physics")
        self.assertEqual(res["entity"], "Mercury (element)")
        self.assertEqual(res["entity_type"], "chemical element")
        self.assertTrue(res["show_image"])
        self.assertTrue("element" in res["image_query"].lower() or "chemical" in res["image_query"].lower() or "metal" in res["image_query"].lower())

    # 4. Albert Einstein
    def test_albert_einstein_person(self):
        context = "Albert Einstein formulated the theory of relativity and made foundational contributions to quantum mechanics."
        res = resolve_disambiguated_term_queries("Albert Einstein", context, "Physics")
        self.assertIn("Einstein", res["entity"])
        self.assertTrue(res["show_image"])
        self.assertIn("einstein", res["image_query"].lower())

    # 5. Photosynthesis
    def test_photosynthesis_scientific_process(self):
        context = "During photosynthesis, light-dependent reactions convert photons and water into chemical energy."
        res = resolve_disambiguated_term_queries("Photosynthesis", context, "Plant Biology")
        self.assertEqual(res["entity"], "Photosynthesis")
        self.assertTrue(res["show_image"])
        self.assertIn("photosynthesis", res["image_query"].lower())

    # 6. However (connector word - No image)
    def test_however_connector_no_image(self):
        show_img, q = should_concept_show_image("however", "However", "connective", "Linguistics")
        self.assertFalse(show_img)
        self.assertIsNone(q)

    # 7. Implementation (abstract term - No image)
    def test_implementation_general_term_no_image(self):
        show_img, q = should_concept_show_image("implementation", "Implementation", "concept", "Software Engineering")
        self.assertFalse(show_img)
        self.assertIsNone(q)

    # 8. Python programming language context
    def test_python_programming_context(self):
        context = "Python is a high-level interpreted programming language widely used in backend development, data science, and scripting."
        res = resolve_disambiguated_term_queries("Python", context, "Software Engineering")
        self.assertEqual(res["entity"], "Python (programming language)")
        self.assertEqual(res["entity_type"], "programming language")

    # 9. Python snake context
    def test_python_snake_context(self):
        context = "The Burmese python coiled silently in the rainforest undergrowth."
        res = resolve_disambiguated_term_queries("Python", context, "Zoology and Herpetology")
        self.assertEqual(res["entity"], "Pythonidae")
        self.assertEqual(res["entity_type"], "snake species")
        self.assertTrue(res["show_image"])
        self.assertIn("snake", res["image_query"].lower())

    # 10. Sound (adjective in context - strictly NO image)
    def test_sound_adjective_no_image(self):
        show_img, q = should_concept_show_image("sound", "Sound", "adjective")
        self.assertFalse(show_img)
        self.assertIsNone(q)

        show_img_2, q_2 = should_concept_show_image("sound", "Sound", "taxonomic placement")
        self.assertFalse(show_img_2)
        self.assertIsNone(q_2)

    # 11. Scientific (adjective in context - strictly NO image)
    def test_scientific_adjective_no_image(self):
        show_img, q = should_concept_show_image("scientific", "Scientific", "adjective")
        self.assertFalse(show_img)
        self.assertIsNone(q)

    # 12. Placement (abstract action/noun - strictly NO image)
    def test_placement_abstract_no_image(self):
        show_img, q = should_concept_show_image("placement", "Placement", "concept")
        self.assertFalse(show_img)
        self.assertIsNone(q)


class TestOpenverseFilteringAndValidation(unittest.TestCase):
    def test_image_url_validation(self):
        self.assertTrue(is_valid_image_url("https://live.staticflickr.com/65535/51234567_b.jpg"))
        self.assertTrue(is_valid_image_url("https://images.openverse.org/photo123.png"))
        self.assertFalse(is_valid_image_url("https://example.com/icon.svg"))
        self.assertFalse(is_valid_image_url("https://example.com/disambig.png"))
        self.assertFalse(is_valid_image_url("https://example.com/question_book.jpg"))
        self.assertFalse(is_valid_image_url(""))
        self.assertFalse(is_valid_image_url(None))

    def test_openverse_metadata_rejection_rules(self):
        # Mango fruit should reject mango tree / farming
        bad_mango_farm = {
            "url": "https://example.com/mango1.jpg",
            "title": "Commercial Mango Tree Plantation Farm",
            "tags": [{"name": "farming"}, {"name": "agriculture"}, {"name": "tree"}],
        }
        self.assertFalse(is_openverse_result_relevant(bad_mango_farm, "Mango", "fruit", "Mango fruit"))

        good_mango_fruit = {
            "url": "https://example.com/mango2.jpg",
            "title": "Fresh Ripe Mango Fruit Close-up",
            "tags": [{"name": "mango"}, {"name": "fruit"}, {"name": "sweet"}],
        }
        self.assertTrue(is_openverse_result_relevant(good_mango_fruit, "Mango", "fruit", "Mango fruit"))

        # Mercury planet should reject mercury metal / cars
        bad_planet_car = {
            "url": "https://example.com/car.jpg",
            "title": "1968 Mercury Cougar Automobile Sedan",
            "tags": [{"name": "car"}, {"name": "automobile"}],
        }
        self.assertFalse(is_openverse_result_relevant(bad_planet_car, "Mercury", "planet", "Mercury planet"))

        good_planet = {
            "url": "https://example.com/planet.jpg",
            "title": "Mercury Planet in Solar System",
            "tags": [{"name": "mercury"}, {"name": "planet"}, {"name": "space"}],
        }
        self.assertTrue(is_openverse_result_relevant(good_planet, "Mercury", "planet", "Mercury planet"))


class TestAsyncMockedPipeline(unittest.IsolatedAsyncioTestCase):
    async def test_wikipedia_definition_parsing_for_scientist(self):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "query": {
                "pages": {
                    "123": {
                        "pageid": 123,
                        "title": "Albert Einstein",
                        "fullurl": "https://en.wikipedia.org/wiki/Albert_Einstein",
                        "extract": "Albert Einstein (14 March 1879 – 18 April 1955) was a German-born theoretical physicist widely acknowledged to be one of the greatest physicists of all time. He is best known for developing the theory of relativity."
                    }
                }
            }
        }

        mock_client = AsyncMock()
        mock_client.get.return_value = mock_response

        res = await fetch_wikipedia_entity_definition(mock_client, "Albert Einstein", "scientist")
        self.assertEqual(res["source"], "Wikipedia")
        self.assertIn("Einstein", res["text"])
        self.assertEqual(res["born"], "14 March 1879")
        self.assertEqual(res["died"], "18 April 1955")
        self.assertIn("relativity", res["known_for"].lower())

    async def test_openverse_image_search_success(self):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "results": [
                {
                    "id": "abc-123",
                    "url": "https://images.openverse.org/mango_fruit.jpg",
                    "title": "Ripe Fresh Mango Fruit",
                    "foreign_landing_url": "https://flickr.com/photos/123",
                    "tags": [{"name": "mango"}, {"name": "fruit"}]
                }
            ]
        }

        mock_client = AsyncMock()
        mock_client.get.return_value = mock_response

        res = await search_openverse_image(mock_client, "Mango fruit", "Mango", "fruit")
        self.assertTrue(res["show"])
        self.assertEqual(res["source"], "Openverse")
        self.assertEqual(res["url"], "https://images.openverse.org/mango_fruit.jpg")
        self.assertEqual(res["title"], "Ripe Fresh Mango Fruit")

    async def test_wikipedia_mismatched_uk_page_rejected_for_biology_kingdom(self):
        uk_response = MagicMock()
        uk_response.status_code = 200
        uk_response.json.return_value = {
            "query": {
                "pages": {
                    "999": {
                        "pageid": 999,
                        "title": "United Kingdom",
                        "fullurl": "https://en.wikipedia.org/wiki/United_Kingdom",
                        "extract": "The United Kingdom of Great Britain and Northern Ireland, commonly known as the United Kingdom (UK) or Britain, is a country in Northwestern Europe..."
                    }
                }
            }
        }
        mock_client = AsyncMock()
        mock_client.get.return_value = uk_response

        res = await fetch_wikipedia_entity_definition(mock_client, "kingdom", "taxonomic rank", context_text="Taxonomy and Systematics. species and genera.")
        # Mismatched United Kingdom page MUST NOT be returned as biological kingdom definition
        self.assertNotIn("United Kingdom of Great Britain", res.get("text", ""))


if __name__ == "__main__":
    unittest.main()
