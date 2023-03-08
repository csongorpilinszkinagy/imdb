import requests
from bs4 import BeautifulSoup
import pandas as pd

def scraper() -> pd.DataFrame:
    url = 'https://www.imdb.com/chart/top/'
    page = requests.get(url)
    soup = BeautifulSoup(page.text, 'html.parser')

    titles = [elem.text for elem in soup.select('td.titleColumn a')]
    assert len(titles) == 250
    assert all(type(title) == str for title in titles)

    data = titles[:20]
    columns = ['title']
    df = pd.DataFrame(data, columns=columns)
    return df

if __name__ == '__main__':
    df = scraper()
    print(df)