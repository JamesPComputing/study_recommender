import unittest
from database import init_db, get_db
from recommender import get_recommendations
import os

class TestDatabase(unittest.TestCase):

    def setUp(self):
        """Initialise the database before each test."""
        init_db()

    def test_database_contains_resources(self):
        """Database should contain at least 20 resources after initialisation."""
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute('SELECT COUNT(*) FROM resources')
        count = cursor.fetchone()[0]
        conn.close()
        self.assertGreaterEqual(count, 20)

    def test_resource_has_required_fields(self):
        """Every resource should have non-empty title, description, topic_tags,
        difficulty, format and url fields."""
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM resources')
        resources = cursor.fetchall()
        conn.close()
        for r in resources:
            self.assertTrue(r['title'], f"Resource {r['resource_id']} has empty title")
            self.assertTrue(r['description'], f"Resource {r['resource_id']} has empty description")
            self.assertTrue(r['topic_tags'], f"Resource {r['resource_id']} has empty topic_tags")
            self.assertTrue(r['difficulty'], f"Resource {r['resource_id']} has empty difficulty")
            self.assertTrue(r['format'], f"Resource {r['resource_id']} has empty format")
            self.assertTrue(r['url'], f"Resource {r['resource_id']} has empty url")

    def test_difficulty_values_are_valid(self):
        """All difficulty values should be Beginner, Intermediate or Advanced."""
        valid = {'Beginner', 'Intermediate', 'Advanced'}
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute('SELECT difficulty FROM resources')
        rows = cursor.fetchall()
        conn.close()
        for r in rows:
            self.assertIn(r['difficulty'], valid,
                f"Invalid difficulty value: {r['difficulty']}")

    def test_format_values_are_valid(self):
        """All format values should be one of the defined types."""
        valid = {'Video', 'Article', 'Tutorial', 'Documentation'}
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute('SELECT format FROM resources')
        rows = cursor.fetchall()
        conn.close()
        for r in rows:
            self.assertIn(r['format'], valid,
                f"Invalid format value: {r['format']}")


class TestRecommender(unittest.TestCase):

    def setUp(self):
        """Initialise the database before each test."""
        init_db()

    def test_returns_results_for_valid_query(self):
        """A valid topic query should return at least one result."""
        results = get_recommendations('Python programming')
        self.assertGreater(len(results), 0)

    def test_returns_no_more_than_top_n(self):
        """Results should not exceed the top_n limit."""
        results = get_recommendations('machine learning', top_n=5)
        self.assertLessEqual(len(results), 5)

    def test_results_have_score_field(self):
        """Every result should include a cosine similarity score."""
        results = get_recommendations('Python')
        for r in results:
            self.assertIn('score', r)

    def test_scores_are_between_zero_and_one(self):
        """All cosine similarity scores should be between 0 and 1."""
        results = get_recommendations('Python')
        for r in results:
            self.assertGreaterEqual(r['score'], 0.0)
            self.assertLessEqual(r['score'], 1.0)

    def test_results_sorted_by_score_descending(self):
        """Results should be sorted from highest to lowest similarity score."""
        results = get_recommendations('Python functions')
        scores = [r['score'] for r in results]
        self.assertEqual(scores, sorted(scores, reverse=True))

    def test_difficulty_filter_beginner(self):
        """Filtering by Beginner should return only Beginner resources."""
        results = get_recommendations('Python', difficulty_filter='Beginner')
        for r in results:
            self.assertEqual(r['difficulty'], 'Beginner')

    def test_difficulty_filter_intermediate(self):
        """Filtering by Intermediate should return only Intermediate resources."""
        results = get_recommendations('machine learning',
                                      difficulty_filter='Intermediate')
        for r in results:
            self.assertEqual(r['difficulty'], 'Intermediate')

    def test_all_filter_returns_mixed_difficulties(self):
        """All levels filter should return results across difficulty levels."""
        results = get_recommendations('Python', difficulty_filter='All', top_n=10)
        difficulties = {r['difficulty'] for r in results}
        self.assertGreater(len(difficulties), 1)

    def test_empty_query_returns_empty_list(self):
        """An empty or whitespace-only query should return an empty list."""
        results = get_recommendations('')
        self.assertEqual(results, [])

    def test_unrelated_query_returns_empty_or_low_scores(self):
        """A completely unrelated query should return no results."""
        results = get_recommendations('xyzzy nonsense gibberish')
        self.assertEqual(results, [])


if __name__ == '__main__':
    unittest.main(verbosity=2)
