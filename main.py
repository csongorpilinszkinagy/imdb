import requests
from bs4 import BeautifulSoup
from progressbar import progressbar
import pandas as pd
import numpy as np

def scraper() -> pd.DataFrame:
    '''
    Function for scraping the top 20 movie titles, ratings, number of
    ratings and number of Oscars in a pandas DataFrame
    '''
    # Open the IMDB top 250 page
    url = 'https://www.imdb.com/chart/top/'
    with requests.get(url) as page:
        soup = BeautifulSoup(page.text, 'html.parser')

        # Scrape titles from the titleColumn cells
        titles = [elem.text for elem in soup.select('td.titleColumn a')]
        # Make sure that we get back all the 250 titles as strings
        assert len(titles) == 250
        assert all(type(title) == str for title in titles)

        # Scrape ratings from the posterColumns cell, the data value is called 'ir'
        ratings = [float(elem.get('data-value')) for elem in soup.select('td.posterColumn span[name=ir]')]
        # Make sure that we get back all the 250 ratings as floats
        assert len(ratings) == 250
        assert all(type(rating) == float for rating in ratings)

        # Scrape number of ratings from the posterColumns cell, the data value is called 'nv'
        num_ratings = [int(elem.get('data-value')) for elem in soup.select('td.posterColumn span[name=nv]')]
        # Make sure that we get back all 250 rating numbers as ints
        assert len(num_ratings) == 250
        assert all(type(num) == int for num in num_ratings)

        # For the oscars the movies need to be scraped individually
        # Get the hrefs for the movie pages from the titleColumns cell
        hrefs = [elem.get('href') for elem in soup.select('td.titleColumn a')]
        # Make sure that we get back all 250 links as strings
        assert len(hrefs) == 250
        assert all(type(href) == str for href in hrefs)

        # Complete the hrefs to point to award pages
        award_urls = [f'https://imdb.com{href}awards' for href in hrefs]

        # Iterate over top 20 urls and get the oscar numbers
        num_oscars = []
        for url in progressbar(award_urls[:20]):
            # Open movie awards page
            with requests.get(url) as awards_page:
                soup = BeautifulSoup(awards_page.text, 'html.parser')

                # Select award outcome cells
                awards = soup.select('td.title_award_outcome')
                
                # Find the oscar cell if it exists
                oscar = None
                for award in awards:
                    category = award.select_one('span.award_category')
                    if category.text == 'Oscar':
                        oscar = award.parent.parent

                # Append the number of oscars rows to the list
                if oscar:
                    num_oscars.append(len(oscar.select('tr')))
                else:
                    num_oscars.append(0)

        # Make sure that we get all 20 oscar numbers as ints      
        assert len(num_oscars) == 20
        assert all(type(num) == int for num in num_oscars)

        # Assemble top 20 dataframe from the scraped data
        df = pd.DataFrame()
        df['title'] = titles[:20]
        df['rating'] = ratings[:20]
        df['num_rating'] = num_ratings[:20]
        df['num_oscar'] = num_oscars

        return df
    
def review_penalizer(num_ratings: list) -> list:
    '''
    Calculates a 0.1 point penalty for every 100.000 deviation from the maximum
    number of ratings
    '''
    if len(num_ratings) == 0: return []
    deviation = max(num_ratings) - np.array(num_ratings)
    deviation_steps = deviation // 100000
    penalty = deviation_steps * 0.1
    return list(penalty)

def oscar_calculator(num_oscars: list) -> list:
    '''
    Calculates the score boost for the number of oscars given to the movie
    '''
    score_boosts = []
    for num in num_oscars:
        if num == 0:
            boost = 0.
        elif num < 3:
            boost = 0.3
        elif num < 6:
            boost = 0.5
        elif num < 11:
            boost = 1.
        else:
            boost = 1.5
        score_boosts.append(boost)

    return score_boosts
    
if __name__ == '__main__':
    # Scrape top 20 movie data
    df = scraper()

    # Create adjusted score column in dataframe
    review_penalty = review_penalizer(df['num_rating'])
    oscar_boost = oscar_calculator(df['num_oscar'])
    # Decrese rating by penalty and increase by oscar boost
    df['adjusted_ranking'] = np.array(df['rating']) - np.array(review_penalty) + np.array(oscar_boost)
    # Output results to csv file
    df.to_csv('imdb_top_20.csv', index=False)
    
