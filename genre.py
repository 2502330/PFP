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
    rating = info.get('rating', 0)
    name = info.get('name', '')  # Add movie name
    description = info.get('description', '')  # Add description
    movie_list.append({
        "id": movie_id,
        "name": name,
        "description": description,
        "genres": genres,
        "keywords": keywords,
        "rating": rating
    })

# Group movies by (genre, keyword) pairs
grouped = defaultdict(list)
for movie in movie_list:
    genres = set(movie['genres'])
    keywords = set(movie['keywords'])
    # For every genre-keyword combination in this movie, add to group
    for genre in genres:
        for keyword in keywords:
            grouped[(genre, keyword)].append(movie)

# Remove groups with only one movie (no match)
grouped = {k: v for k, v in grouped.items() if len(v) > 1}

# Sort each group by rating descending
for group in grouped.values():
    group.sort(key=lambda x: x.get('rating', 0), reverse=True)

# Write to genre.json
with open('data/genre.json', 'w', encoding='utf-8') as f:
    # Convert tuple keys to strings for JSON compatibility
    json.dump({f"{k[0]}|{k[1]}": v for k, v in grouped.items()}, f, ensure_ascii=False, indent=2)