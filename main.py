import requests
from bs4 import BeautifulSoup
import pandas as pd

def scraper() -> pd.DataFrame:
    url = 'https://www.imdb.com/chart/top/'
    with requests.get(url) as page:
        soup = BeautifulSoup(page.text, 'html.parser')

        titles = [elem.text for elem in soup.select('td.titleColumn a')]
        assert len(titles) == 250
        assert all(type(title) == str for title in titles)

        ratings = [float(elem.get('data-value')) for elem in soup.select('td.posterColumn span[name=ir]')]
        assert len(ratings) == 250
        assert all(type(rating) == float for rating in ratings)

        num_ratings = [int(elem.get('data-value')) for elem in soup.select('td.posterColumn span[name=nv]')]
        assert len(num_ratings) == 250
        assert all(type(num) == int for num in num_ratings)

        df = pd.DataFrame()
        df['title'] = titles[:20]
        df['rating'] = ratings[:20]
        df['num_rating'] = num_ratings[:20]

        return df

if __name__ == '__main__':
    df = scraper()
    print(df)