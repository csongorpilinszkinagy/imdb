import requests
from bs4 import BeautifulSoup
from progressbar import progressbar
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

        hrefs = [elem.get('href') for elem in soup.select('td.titleColumn a')]
        assert len(hrefs) == 250
        assert all(type(href) == str for href in hrefs)

        award_urls = [f'https://imdb.com{href}awards' for href in hrefs]

        num_oscars = []
        for url in progressbar(award_urls[:20]):
            with requests.get(url) as awards_page:
                soup = BeautifulSoup(awards_page.text, 'html.parser')

                awards = soup.select('td.title_award_outcome')
                oscar_winner = None
                for award in awards:
                    category = award.select_one('span.award_category')
                    outcome = award.select_one('b')
                    if category.text == 'Oscar' and outcome.text == 'Winner':
                        oscar_winner = award.parent.parent

                if oscar_winner:
                    num_oscars.append(len(oscar_winner.select('tr')))
                else:
                    num_oscars.append(0)
        assert len(num_oscars) == 20
        assert all(type(num) == int for num in num_oscars)

        df = pd.DataFrame()
        df['title'] = titles[:20]
        df['rating'] = ratings[:20]
        df['num_rating'] = num_ratings[:20]
        df['num_oscar'] = num_oscars

        return df

if __name__ == '__main__':
    df = scraper()
    print(df)