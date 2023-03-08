# IMDB top 20 adjusted scores
This coding assigment scrapes the top 20 movies from IMDB and adjusts the ratings based on the number of ratings and Oscars given to the movie.

*Time needed for the assignment: approximately **6 hours**. Did not use ChatGPT for code generation.*

## How to run

### Codespaces environment
Start a Github Codespace from the `main` branch.

### Install dependencies
Codespaces comes with most of the dependencies but we need `progressbar` for tracking of the scraping and `hypothesis` for good testing coverage. Install those dependencies listed in `requirements.txt` with this command:
```
pip install -r requirements.txt
```

### Run tests
First make sure that the code runs as it should, so run the testcases with this command:
```
python test.py
```

### Run scraping
If the tests run OK start scraping with this command:
```
python main.py
```
The program should output the results in the `imdb_top_20.csv` file.
