import unittest
from main import scraper, review_penalizer, oscar_calculator
import pandas as pd
import numpy as np
from hypothesis import given, settings, strategies as st

MAX_RATING = 10
MAX_NUM_RATING = 1E7
MAX_NUM_OSCAR = 100
MAX_PENALTY = MAX_NUM_RATING // 1E5 * 0.1
MAX_BOOST = 1.5

class TestScraper(unittest.TestCase):
    # Runs scraping only once to save time
    @classmethod
    def setUpClass(cls):
        cls.df = scraper()

    # Scraper should return a DataFrame
    def test_scraper_type(self):
        self.assertIsInstance(self.df, pd.DataFrame)
    
    # Scraper should return 20 rows
    def test_scraper_size(self):
        self.assertEqual(len(self.df.index), 20)

    # Scraper should return these four columns
    def test_scraper_columns(self):
        self.assertCountEqual(self.df.columns, ['title', 'rating', 'num_rating', 'num_oscar'])

    # Scraper should return ratings with values between 0 and 10
    def test_scraper_ratings(self):
        self.assertTrue(all(0 <= rating <= MAX_RATING for rating in self.df['rating']))
    
    # Scraper should return number of ratings between 0 and arbitrary big rating number
    def test_scraper_num_ratings(self):
        self.assertTrue(all(0 <= num <= MAX_NUM_RATING for num in self.df['num_rating']))
    
    # Scraper should return number of oscars between 0 and arbitrary big oscar number
    def test_scraper_num_oscars(self):
        self.assertTrue(all(0 <= num <= MAX_NUM_OSCAR for num in self.df['num_oscar']))

# Hypothesis generates lists with integers and tests on those values
class TestReviewPenalizer(unittest.TestCase):
    # The length of the penalties should equal the length of ratings
    @given(st.lists(st.integers(min_value=0, max_value=MAX_NUM_RATING)))
    def test_length(self, num_ratings):
        penalties = review_penalizer(num_ratings)
        self.assertEqual(len(num_ratings), len(penalties))

    # The values of the penalties should be between 0 and MAX_PENALTY which comes from MAX_NUM_RATINGS
    @given(st.lists(st.integers(min_value=0, max_value=MAX_NUM_RATING)))
    def test_values(self, num_ratings):
        penalties = review_penalizer(num_ratings)
        self.assertTrue(all(0 <= penalty <= MAX_PENALTY for penalty in penalties))

    # The penalties list must contain one zero element which comes from the maximum element not needing any penalty
    @given(st.lists(st.integers(min_value=0, max_value=MAX_NUM_RATING)))
    def test_got_zero(self, num_ratings):
        penalties = review_penalizer(num_ratings)
        self.assertTrue(0 in penalties if penalties else True)
    
    def test_explicit_values(self):
        num_ratings = [2432487, 2432486, 1678626, 521344, 0]
        expected_results = [0., 0., 0.7, 1.9, 2.4]
        penalties = review_penalizer(num_ratings)
        np.testing.assert_almost_equal(penalties, expected_results, decimal=4)
        
# Hypothesis generates lists with integers and tests on those values
class TestOscarCalculator(unittest.TestCase):
    # The length of the boosts should equal the length of oscars
    @given(st.lists(st.integers(min_value=0, max_value=MAX_NUM_OSCAR)))
    def test_length(self, num_oscars):
        boosts = oscar_calculator(num_oscars)
        self.assertEqual(len(num_oscars), len(boosts))
        
    # The values of boosts should be between 0 and 1.5 (MAX_BOOST)
    @given(st.lists(st.integers(min_value=0, max_value=MAX_NUM_OSCAR)))
    def test_values(self, num_oscars):
        boosts = oscar_calculator(num_oscars)
        self.assertTrue(all(0 <= boost <= MAX_BOOST for boost in boosts))

    def test_explicit_values(self):
        num_oscars = range(12)
        expected_results = [0., 0.3, 0.3, 0.5, 0.5, 0.5, 1., 1., 1., 1., 1., 1.5]
        boosts = oscar_calculator(num_oscars)
        np.testing.assert_almost_equal(boosts, expected_results, decimal=4)

if __name__ == '__main__':
    unittest.main()
