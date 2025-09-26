import json
from collections import defaultdict

# Load your JSON file
with open('data/imdb.json', encoding="utf8") as f:
    movies = json.load(f)

# Prepare a list of movie dicts with id, name, genres, keywords, rating
movie_list = []
for movie_id, info in movies.items():
    if not isinstance(info, dict):
        continue
    genres = info.get('genres') or []
    keywords = info.get('keywords') or []
    rating = info.get('rating', 0)
    name = info.get('name', '')
    movie_list.append({
        "id": movie_id,
        "name": name,
        "genres": genres,
        "keywords": keywords,
        "rating": rating
    })

# Group movies by (genre, keyword) pairs
grouped = defaultdict(list)
for movie in movie_list:
    genres = set(movie['genres'])
    keywords = set(movie['keywords'])
    for genre in genres:
        for keyword in keywords:
            grouped[(genre, keyword)].append(movie)

# Remove groups with only one movie (no match)
grouped = {k: v for k, v in grouped.items() if len(v) > 1}

# Build output with "id|name" as key and list of movie ids sorted by rating
output = {}
for group in grouped.values():
    for movie in group:
        key = f"{movie['id']}"
        # Get all other movies in the group except the current one
        others = [m for m in group if m['id'] != movie['id']]
        # Sort by rating descending
        sorted_others = sorted(others, key=lambda x: x.get('rating', 0), reverse=True)
        # Only keep the id
        output[key] = [m['id'] for m in sorted_others]

# Write to genre.json
with open('data/genre.json', 'w', encoding='utf-8') as f:
    json.dump(output, f, ensure_ascii=False, indent=2)