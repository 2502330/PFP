import json
from datetime import datetime
import os
import re


class ReviewSegmenter:
    def __init__(self):
        self.dictionary = self._load_dictionary()
        self.data = self._load_reviews()
        self.result_data = self._load_result_data()
        self.max_word_len = 20
        
    def _load_dictionary(self):
        """Load dictionary from words.txt file"""
        try:
            with open('data/words.txt', 'r', encoding='utf-8') as f:
                word_set = set(line.strip().lower() for line in f if line.strip())
            print("Loaded dictionary from data/words.txt")
            return word_set
        except FileNotFoundError:
            print("Warning: data/words.txt not found.")
            return set()

    def _load_reviews(self):
        """Load reviews from JSON file"""
        try:
            with open('data/imdb.json', 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            print("Warning: data/imdb.json not found.")
            return {}

    def _load_result_data(self):
        """Load existing results.json data from results/ folder"""
        try:
            with open('results/results.json', 'r', encoding='utf-8') as f:
                existing_data = json.load(f)
                print("Loaded existing results.json file from results/results.json")
                return existing_data
        except FileNotFoundError:
            print("Warning: results/results.json not found. Starting with empty structure.")
            return {}

    def _is_valid_word(self, word):
        """Check if a word exists in our word list"""
        return word in self.dictionary

    def insert_spaces(self, text):
        """Insert spaces into text using dictionary segmentation"""
        n = len(text)
        i = 0
        words = []
        
        while i < n:
            found = False
            
            # Try longest possible word first
            for length in range(min(self.max_word_len, n - i), 0, -1):
                word = text[i:i + length]
                
                if self._is_valid_word(word):
                    words.append(word)
                    i += length
                    found = True
                    break
            
            if not found:
                # If no word found, take one character
                words.append(text[i])
                i += 1
        
        return ' '.join(words)

    def _auto_segment_review(self, review_text):
        """Automatically segment review text and capitalize sentences after dots"""
        # Clean the text - keep spaces, letters, numbers, and basic punctuation
        clean_review = re.sub(r'[^\w\s\.!?]', '', review_text.lower())
        clean_review = re.sub(r'\s+', ' ', clean_review).strip()
        
        # First, segment the text
        segmented_review = self.insert_spaces(clean_review)
        
        # Then capitalize sentences after dots
        segmented_review = self._capitalize_sentences(segmented_review)
        
        return segmented_review

    def _capitalize_sentences(self, text):
        """Capitalize the first letter of each sentence after a dot"""
        if not text:
            return text
        
        # Split into sentences using dot as delimiter, but preserve the dots
        parts = text.split('.')
        capitalized_parts = []
        
        for i, part in enumerate(parts):
            part = part.strip()
            if part:
                # Capitalize first letter of each sentence
                if i == 0:  # First sentence
                    capitalized_part = part[0].upper() + part[1:] if part else ""
                else:  # Subsequent sentences
                    capitalized_part = part[0].upper() + part[1:] if part else ""
                
                capitalized_parts.append(capitalized_part)
        
        # Join with dots and spaces
        result = '. '.join(capitalized_parts)
        
        # Add final dot if the original text ended with a dot
        if text.strip().endswith('.'):
            result += '.'
        
        return result

    def display_movies(self):
        """Display all available movies"""
        if not self.data:
            print("No movies available.")
            return
        
        print("Available movies:")
        for i, movie_id in enumerate(self.data.keys()):
            movie_title = self.data[movie_id].get("title", "Unknown Title")
            # Check if movie exists in results.json
            has_result = "Yes" if movie_id in self.result_data else "No"
            print(f"{i}: {movie_id} - {movie_title} [In results.json: {has_result}]")

    def add_new_review(self, movie_id, review_text):
        """Add a new review to a movie and auto-segment it"""
        if movie_id not in self.data:
            print("Movie ID not found!")
            return False
        
        # Auto-segment the new review
        segmented_review = self._auto_segment_review(review_text)
        
        # Add to results.json using your existing structure
        self._add_review_to_results(movie_id, segmented_review)
        
        print(f"\nNew review added and auto-segmented:")
        print(f"Original: {review_text}")
        print(f"Segmented: {segmented_review}")
        
        # Auto-save after adding
        self.save_reviews_data()
        
        return True

    def _add_review_to_results(self, movie_id, segmented_review):
        """Add segmented review to existing results.json structure"""
        # If movie doesn't exist in results.json, create the structure
        if movie_id not in self.result_data:
            # Get movie info from imdb.json
            movie_info = self.data.get(movie_id, {})
            self.result_data[movie_id] = {
                "name": movie_info.get("title", "Unknown Title"),
                "poster": movie_info.get("poster", ""),
                "description": movie_info.get("description", ""),
                "rating": movie_info.get("rating", 0),
                "genres": movie_info.get("genres", []),
                "date_published": movie_info.get("date_published", ""),
                "keywords": movie_info.get("keywords", []),
                "reviews": []  # Start with empty reviews list
            }
        
        # Add the new segmented review to the reviews array
        if "reviews" not in self.result_data[movie_id]:
            self.result_data[movie_id]["reviews"] = []
        
        self.result_data[movie_id]["reviews"].append(segmented_review)
        print(f"Added review to results.json for movie: {self.result_data[movie_id]['name']}")

    def save_reviews_data(self):
        """Auto-save all data including reviews and results.json"""
        # Save results.json
        try:
            with open('results/results.json', 'w', encoding='utf-8') as f:
                json.dump(self.result_data, f, ensure_ascii=False, indent=2)
            print("results.json updated successfully!")
            return True
        except Exception as e:
            print(f"Error saving results.json: {e}")
            return False

    def run(self):
        """Main application loop - simplified for adding new reviews"""
        while True:
            print("\n=== Review Segmentation Tool ===")
            print("1. List all movies")
            print("2. Add new review to movie (auto-segment & auto-save)")
            print("3. Exit")
            
            choice = input("\nEnter your choice (1-3): ").strip()
            
            if choice == "1":
                self.display_movies()
            
            elif choice == "2":
                self.display_movies()
                try:
                    movie_index = int(input("\nEnter movie index to add review to: "))
                    movie_id = list(self.data.keys())[movie_index]
                    
                    review_text = input("Enter your new review: ").strip()
                    if not review_text:
                        print("No review text provided!")
                        continue
                    
                    if self.add_new_review(movie_id, review_text):
                        print("Review added, auto-segmented, and auto-saved successfully!")
                        
                except (ValueError, IndexError):
                    print("Invalid input!")
            
            elif choice == "3":
                print("Exiting.")
                break
            
            else:
                print("Invalid choice! Please enter 1-3.")


def main():
    # Create both data and results directories if they don't exist
    os.makedirs('data', exist_ok=True)
    os.makedirs('results', exist_ok=True)
    
    segmenter = ReviewSegmenter()
    
    # Display info about existing results.json
    if segmenter.result_data:
        movie_count = len(segmenter.result_data)
        total_reviews = sum(len(movie.get("reviews", [])) for movie in segmenter.result_data.values())
        print(f"Loaded existing results.json with {movie_count} movies and {total_reviews} reviews")
    
    segmenter.run()


if __name__ == "__main__":
    main()