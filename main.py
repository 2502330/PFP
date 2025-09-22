import json
from pathlib import Path

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

# Load sentiments dictionary
sentiments = load_sentiments('data/AFINN-en-165.txt')

# Load movies dictionary
with open('data/imdb.json', 'r', encoding='utf-8') as f:
    movies = json.load(f)
    total_reviews = sum(len(movie['reviews']) for movie in movies.values())

print(f'loaded {len(sentiments)} sentiments')
print(f'loaded {len(movies)} movies')
print(f'loaded {total_reviews} reviews')

# Sentiment analysis
for id in movies.keys():
    analysis = [analyze(review, sentiments) for review in movies[id]['reviews']]
    
    for review_analysis in analysis:
        # Print or log the most positive and negative paragraphs for debugging
        print(f"Most Positive Paragraph: {review_analysis['most_pos_paragraph']}")
        print(f"Most Negative Paragraph: {review_analysis['most_neg_paragraph']}")    

    movies[id]['analysis'] = analysis

# Write to results.json
Path('results').mkdir(exist_ok=True)
with open('results/results.json', 'w', encoding='utf-8') as f:
    json.dump(movies, f, ensure_ascii=False, indent=4)