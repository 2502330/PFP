import json
import re
import time
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor

from PyMovieDb import IMDB

imdb = IMDB()

def sort_by_prefix(path):
    return int(path.stem.split('_')[0])

def load_review(file):
    # print(f'loading {file}')
    return file.read_text('utf-8')

def fetch_details(id):
    # Add delay due to api rate limit
    time.sleep(0.1)

    res = json.loads(imdb.get_by_id(id))
    status = res.get('status', 'success')
    emoji = '✅' if status == 'success' else '❌'
    print(f'fetching details of {id} -> {status} {emoji}')
    return id, res

if __name__ == '__main__':

    t1 = time.perf_counter()

    # Load ids from urls
    neg_urls = Path('data/urls_neg.txt').read_text().splitlines()
    pos_urls = Path('data/urls_pos.txt').read_text().splitlines()
    urls = neg_urls + pos_urls
    ids = [re.search(r'tt\d+', url).group() for url in urls if re.search(r'tt\d+', url)]

    unique_ids = list(dict.fromkeys(ids))

    # Fetch details from api
    with ThreadPoolExecutor(10) as executor:
        res = dict(executor.map(fetch_details, unique_ids))

    # Create details dictionary with ids as keys and details as values
    details_dict = {}
    for id in unique_ids:
        details_dict[id] = {
            'name': res[id].get('name'),
            'poster': res[id].get('poster'),
            'description': res[id].get('description'),
            'rating': res[id].get('rating', {}).get('ratingValue'),
            'genres': res[id].get('genre'),
            'date_published': res[id].get('datePublished'),
            'keywords': [kw for kw in (res[id].get('keywords') or '').split(',') if kw],
        }

    # Load original review files in parallel
    with ThreadPoolExecutor() as executor:
        # sort_by_prefix ensures that files are loaded in the correct order
        neg_files = sorted(Path('data/neg').glob('*.txt'), key=sort_by_prefix)
        pos_files = sorted(Path('data/pos').glob('*.txt'), key=sort_by_prefix)

        neg_reviews = list(executor.map(load_review, neg_files))
        pos_reviews = list(executor.map(load_review, pos_files))

        reviews = neg_reviews + pos_reviews

    # Create reviews dictionary with ids as keys and reviews as values
    reviews_dict = {}
    for id, review in zip(ids, reviews):
        if id in reviews_dict:
            reviews_dict[id].append(review)
        else:
            reviews_dict[id] = [review]

    # Create imdb dictionary by merging details dictionary and reviews dictionary
    imdb_dict = {
        id: {
            **details_dict[id],
            'reviews': reviews_dict[id],
        }
        for id in unique_ids
    }

    # Write to imdb.json
    with open('data/imdb.json', 'w', encoding='utf-8') as f:
        json.dump(imdb_dict, f, ensure_ascii=False, indent=4)

    print(f'time elapsed: {time.perf_counter() - t1}')