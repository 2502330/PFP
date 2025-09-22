## Running the program

1. `data` folder should contain `neg`, `pos`,`AFINN-en-165.txt`, `imdb.json`, `urls_neg.txt`, `urls_pos.txt`
2. Run `main.py`
3. Check `results/results.json` for output

## Building `imdb.json`

1. Run `pip install -r requirements.txt`
2. Run `imdb_builder.py`
3. Check `data/imdb.json` for output
4. Run `imdb_validator.py`
    > Repeat until there are no more broken ids.
    This is due to API rate limits by PyMovieDb.