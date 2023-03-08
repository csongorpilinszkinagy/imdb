import unittest
from main import scraper
import pandas as pd
import numpy as np

class Test(unittest.TestCase):

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

if __name__ == '__main__':
    unittest.main()