import json
from concurrent.futures import ThreadPoolExecutor

from imdb_builder import fetch_details

# Load imdb dictionary
with open('data/imdb.json', 'r', encoding='utf-8') as f:
    imdb_dict = json.load(f)
    broken_ids = [id for id in imdb_dict if imdb_dict[id]['name'] is None]

# Fetch details of broken ids from api
with ThreadPoolExecutor(10) as executor:
    res = dict(executor.map(fetch_details, broken_ids))

# Update imdb dictionary
for id in broken_ids:
    imdb_dict[id]['name'] = res[id].get('name')
    imdb_dict[id]['poster'] = res[id].get('poster')
    imdb_dict[id]['description'] = res[id].get('description')
    imdb_dict[id]['rating'] = res[id].get('rating', {}).get('ratingValue')
    imdb_dict[id]['genres'] = res[id].get('genre')
    imdb_dict[id]['date_published'] = res[id].get('datePublished')
    imdb_dict[id]['keywords'] = [kw for kw in (res[id].get('keywords') or '').split(',') if kw]

# Write to imdb.json
with open('data/imdb.json', 'w', encoding='utf-8') as f:
    json.dump(imdb_dict, f, ensure_ascii=False, indent=4)

# Print validation results
unfixed_ids = [id for id in imdb_dict if imdb_dict[id]['name'] is None]
fixed_ids = len(broken_ids) - len(unfixed_ids)
print(f'fixed {fixed_ids}/{len(broken_ids)} broken ids')