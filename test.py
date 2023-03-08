import unittest
from main import scraper, review_penalizer
import pandas as pd
import numpy as np
from hypothesis import given, settings, strategies as st

class TestScraper(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.df = scraper()

    def test_scraper_type(self):
        self.assertIsInstance(self.df, pd.DataFrame)
    
    def test_scraper_size(self):
        self.assertEqual(len(self.df.index), 20)

    def test_scraper_columns(self):
        self.assertCountEqual(self.df.columns, ['title', 'rating', 'num_rating', 'num_oscar'])

    def test_scraper_ratings(self):
        self.assertTrue(all(0 <= rating <= 10. for rating in self.df['rating']))
    
    def test_scraper_num_ratings(self):
        self.assertTrue(all(0 <= num <= 1E7 for num in self.df['num_rating']))
    
    def test_scraper_num_oscars(self):
        self.assertTrue(all(0 <= num <= 100 for num in self.df['num_oscar']))

class TestReviewPenalizer(unittest.TestCase):
    @given(st.lists(st.integers(min_value=0, max_value=1E7)))
    def test_length(self, num_ratings):
        penalties = review_penalizer(num_ratings)
        self.assertEqual(len(num_ratings), len(penalties))

    @given(st.lists(st.integers(min_value=0, max_value=1E7)))
    def test_values(self, num_ratings):
        penalties = review_penalizer(num_ratings)
        self.assertTrue(all(0 <= penalty <= 100 for penalty in penalties))

    @given(st.lists(st.integers(min_value=0, max_value=1E7)))
    def test_got_zero(self, num_ratings):
        penalties = review_penalizer(num_ratings)
        self.assertTrue(0 in penalties if penalties else True)

if __name__ == '__main__':
    unittest.main()