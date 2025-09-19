import time
import json
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
from sas import *

def load_sentiments(file):
    sentiments = {}
    with open(file, 'r', encoding='utf-8') as f:
        for line in f:
            parts = line.strip().split('\t')
            if len(parts) == 2:
                word, score = parts
                sentiments[word] = int(score)
    return sentiments

def sort_by_prefix(path):
    return int(path.stem.split('_')[0])

def load_review(file):
    print(f'loading {file}')
    return file.read_text('utf-8')

def build_reviews_json():
    print('building reviews.json')
    # Load original review files in parallel
    with ThreadPoolExecutor() as executor:
        # sort_by_prefix ensures that files are loaded in the correct order
        neg_files = sorted(Path('data/neg').glob('*.txt'), key=sort_by_prefix)
        pos_files = sorted(Path('data/pos').glob('*.txt'), key=sort_by_prefix)

        neg_reviews = list(executor.map(load_review, neg_files))
        pos_reviews = list(executor.map(load_review, pos_files))

        reviews = neg_reviews + pos_reviews

    # Load ids from urls
    neg_urls = Path('data/urls_neg.txt').read_text().splitlines()
    pos_urls = Path('data/urls_pos.txt').read_text().splitlines()
    urls = neg_urls + pos_urls
    ids = [re.search(r'tt\d+', url).group() for url in urls if re.search(r'tt\d+', url)]

    # Create a reviews dictionary with ids as keys and reviews as values
    reviews_dict = {}
    for id, review in zip(ids, reviews):
        if id in reviews_dict:
            reviews_dict[id].append(review)
        else:
            reviews_dict[id] = [review]

    # Write to reviews.json
    with open('data/reviews.json', 'w', encoding='utf-8') as f:
        serialized = json.dumps(reviews_dict)
        f.write(serialized)

# Start timer to measure execution time
t1 = time.perf_counter()

# Load sentiment dictionary
sentiments = load_sentiments('data/AFINN-en-165.txt')

# Build reviews.json if not built
if not Path('data/reviews.json').is_file():
    build_reviews_json()

# Load reviews from reviews.json
with open('data/reviews.json', 'r', encoding='utf-8') as f:
    reviews = json.load(f)
    reviews_count = sum(len(reviews) for reviews in reviews.values())

print(f'loaded {len(sentiments)} sentiments')
print(f'loaded {len(reviews)} movies')
print(f'loaded {reviews_count} reviews')

# Sentiment analysis
results = {}
for id in reviews.keys():
    analysis = [analyze(review, sentiments) for review in reviews[id]]
    results[id] = analysis

# Write to results.json
Path('results').mkdir(exist_ok=True)
with open('results/results.json', 'w', encoding='utf-8') as f:
    json.dump(results, f)

# End timer to measure execution time
t2 = time.perf_counter()
print(f'time elapsed: {t2 - t1}s')