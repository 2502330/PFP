import json
import enchant
from datetime import datetime


class ReviewSegmenter:
    def __init__(self):
        self.dictionary = self._load_dictionary()
        self.data = self._load_reviews()
        self.max_word_len = 20
    def _load_dictionary(self):
        """Load dictionary from words.txt file with fallbacks"""
        # First try to load from words.txt
        try:
            with open('data/words.txt', 'r', encoding='utf-8') as f:
                word_set = set(line.strip().lower() for line in f if line.strip())
            print("Loaded dictionary from data/words.txt")
            return word_set
        except FileNotFoundError:
            print("Warning: data/words.txt not found. Trying fallback dictionaries...")

    def _load_reviews(self):
        """Load reviews from JSON file"""
        try:
            with open('data/imdb_no_spaces_reviews.json', 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            print("Warning: data/imdb_no_spaces_reviews.json not found.")
            return {}

    def _is_valid_word(self, word):
        """Check if a word exists in the dictionary"""
        if hasattr(self.dictionary, 'check'):  # PyEnchant dictionary
            return self.dictionary.check(word)
        else:  # Set of words
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

    def display_movies(self):
        """Display all available movies"""
        if not self.data:
            print("No movies available.")
            return
        
        print("Available movies:")
        for i, movie_id in enumerate(self.data.keys()):
            movie_title = self.data[movie_id].get("title", "Unknown Title")
            print(f"{i}: {movie_id} - {movie_title}")

    def display_reviews(self, movie_id):
        """Display reviews for a specific movie"""
        if movie_id not in self.data:
            print("Movie ID not found!")
            return False
        
        movie = self.data[movie_id]
        print(f"\nMovie: {movie.get('title', 'Unknown Title')}")
        
        if "reviews" in movie and movie["reviews"]:
            print("Reviews:")
            for i, review in enumerate(movie["reviews"]):
                preview = review[:100] + "..." if len(review) > 100 else review
                print(f"{i}: {preview}")
            return True
        else:
            print("No reviews available for this movie.")
            return False

    def segment_review(self, movie_id, review_index):
        """Segment a specific review and replace it in the data"""
        if movie_id not in self.data:
            print("Movie ID not found!")
            return False
        
        movie = self.data[movie_id]
        if "reviews" not in movie or review_index >= len(movie["reviews"]):
            print("Review index not found!")
            return False
        
        review = movie["reviews"][review_index]
        clean_review = ''.join(filter(str.isalnum, review.lower()))
        segmented_review = self.insert_spaces(clean_review)

        # Replace the original review
        movie["reviews"][review_index] = segmented_review
        
        print(f"\nOriginal review: {review}")
        print(f"Segmented review: {segmented_review}")
        
        return True

    def segment_user_input(self):
        """Segment user-provided text input and optionally save to file"""
        user_text = input("\nEnter the text you want to segment: ").strip()
        
        if not user_text:
            print("No text provided!")
            return
        
        clean_text = ''.join(filter(str.isalnum, user_text.lower()))
        segmented_text = self.insert_spaces(clean_text)
        
        print(f"\nOriginal text: {user_text}")
        print(f"Segmented text: {segmented_text}")
        
        self._save_user_segmentation(user_text, segmented_text)

    def _save_user_segmentation(self, original_text, segmented_text):
        """Save user segmentation to file"""
        save_option = input("\nSave this segmentation? (y/n): ").strip().lower()
        if save_option != 'y':
            return
        
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        user_entry = {
            "timestamp": timestamp,
            "original_text": original_text,
            "segmented_text": segmented_text
        }
        
        try:
            with open('data/user_segmentations.json', 'r', encoding='utf-8') as f:
                user_data = json.load(f)
        except FileNotFoundError:
            user_data = []
        
        user_data.append(user_entry)
        
        with open('data/user_segmentations.json', 'w', encoding='utf-8') as f:
            json.dump(user_data, f, ensure_ascii=False, indent=2)
        
        print("Segmentation saved to data/user_segmentations.json")

    def view_user_segmentations(self):
        """View previously saved user segmentations"""
        try:
            with open('data/user_segmentations.json', 'r', encoding='utf-8') as f:
                user_data = json.load(f)
            
            if not user_data:
                print("No user segmentations found.")
                return
            
            print("\n=== Previously Saved User Segmentations ===")
            for i, entry in enumerate(user_data, 1):
                print(f"\n--- Entry {i} ---")
                print(f"Time: {entry['timestamp']}")
                print(f"Original: {entry['original_text']}")
                print(f"Segmented: {entry['segmented_text']}")
                
        except FileNotFoundError:
            print("No user segmentations file found.")

    def save_data(self):
        """Save the modified data back to the original file"""
        if not self.data:
            print("No data to save.")
            return False
        
        try:
            with open('data/imdb_no_spaces_reviews.json', 'w', encoding='utf-8') as f:
                json.dump(self.data, f, ensure_ascii=False, indent=2)
            print("Changes saved successfully!")
            return True
        except Exception as e:
            print(f"Error saving data: {e}")
            return False

    def run(self):
        """Main application loop"""
        while True:
            print("\n=== Review Segmentation Tool ===")
            print("1. List all movies")
            print("2. Select movie and segment review")
            print("3. Segment user input text")
            print("4. View saved user segmentations")
            print("5. Save changes and exit")
            print("6. Exit without saving")
            
            choice = input("\nEnter your choice (1-6): ").strip()
            
            if choice == "1":
                self.display_movies()
            
            elif choice == "2":
                self.display_movies()
                try:
                    movie_index = int(input("\nEnter movie index: "))
                    movie_id = list(self.data.keys())[movie_index]
                    
                    if self.display_reviews(movie_id):
                        review_index = int(input("\nEnter review index to segment: "))
                        if self.segment_review(movie_id, review_index):
                            print("Review segmented successfully!")
                        else:
                            print("Failed to segment review.")
                    
                except (ValueError, IndexError):
                    print("Invalid input! Please enter valid numbers.")
            
            elif choice == "3":
                self.segment_user_input()
            
            elif choice == "4":
                self.view_user_segmentations()
            
            elif choice == "5":
                if self.save_data():
                    break
            
            elif choice == "6":
                print("Exiting without saving.")
                break
            
            else:
                print("Invalid choice! Please enter 1-6.")


def main():
    segmenter = ReviewSegmenter()
    segmenter.run()


if __name__ == "__main__":
    main()