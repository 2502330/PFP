import json
from collections import defaultdict

# Load your JSON file
with open('data/imdb.json', encoding="utf8") as f:
    movies = json.load(f)

# Prepare a list of movie dicts with id, name, description, genres, keywords, rating
movie_list = []
for movie_id, info in movies.items():
    if not isinstance(info, dict):
        continue
    genres = info.get('genres') or []
    keywords = info.get('keywords') or []
    movie_list.append({
        "id": movie_id,
        "genres": genres,
        "keywords": keywords
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

# Sort each group by rating descending
for group in grouped.values():
    group.sort(key=lambda x: x.get('rating', 0), reverse=True)

# Build output with "id" as key and list of movie ids as value
output = {}
for group in grouped.values():
    for movie in group:
        key = f"{movie['id']}"
        if key not in output:
            output[key] = []
        # Add all movie ids in the group except the current movie itself
        output[key].extend([m['id'] for m in group if m['id'] != movie['id']])

# Optionally, remove duplicates in each list
for key in output:
    output[key] = list(dict.fromkeys(output[key]))  # preserves order and removes duplicates

# Write to genre.json
with open('data/genre.json', 'w', encoding='utf-8') as f:
    json.dump(output, f, ensure_ascii=False, indent=2)