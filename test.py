import unittest
from main import scraper, review_penalizer, oscar_calculator
import pandas as pd
import numpy as np
from hypothesis import given, settings, strategies as st

MAX_RATING = 10
MAX_NUM_RATING = 1E7
MAX_NUM_OSCAR = 100
MAX_PENALTY = 100
MAX_BOOST = 1.5

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

class TestOscarCalculator(unittest.TestCase):
    @given(st.lists(st.integers(min_value=0, max_value=MAX_NUM_OSCAR)))
    def test_length(self, num_oscars):
        boosts = oscar_calculator(num_oscars)
        self.assertEqual(len(num_oscars), len(boosts))

    @given(st.lists(st.integers(min_value=0, max_value=MAX_NUM_OSCAR)))
    def test_values(self, num_oscars):
        boosts = oscar_calculator(num_oscars)
        self.assertTrue(all(0 <= boost <= MAX_BOOST for boost in boosts))

if __name__ == '__main__':
    unittest.main()