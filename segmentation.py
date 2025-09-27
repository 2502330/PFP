import json
import os
import re
import wordninja
from itertools import product


class ReviewSegmenter:
    def __init__(self):
        self.data = self._load_reviews()
        self.result_data = self._load_result_data()
        self.dictionary = self._load_dictionary()  # For multiple segmentations
        
    def _load_dictionary(self):
        """Load dictionary for multiple segmentation options"""
        try:
            with open('data/words.txt', 'r', encoding='utf-8') as f:
                word_set = set(line.strip().lower() for line in f if line.strip())
            print(f"Loaded dictionary with {len(word_set)} words")
            return word_set
        except FileNotFoundError:
            print("Using wordninja's default dictionary")
            # Fallback to common English words
            return set(wordninja.split("hello world this is a test"))  # Sample to get common words

    def _load_reviews(self):
        """Load reviews from JSON file"""
        try:
            with open('data/imdb.json', 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            print("Warning: data/imdb.json not found.")
            return {}

    def _load_result_data(self):
        """Load existing results.json data"""
        try:
            with open('results/results.json', 'r', encoding='utf-8') as f:
                existing_data = json.load(f)
                print("Loaded existing results.json")
                return existing_data
        except FileNotFoundError:
            print("Starting with empty results structure.")
            return {}

    def simple_segmentation(self, text):
        """Single best segmentation using wordninja"""
        words = wordninja.split(text)
        return ' '.join(words)

    def all_possible_segmentations(self, text):
        """Return all possible valid segmentations"""
        text = text.lower().strip()
        n = len(text)
        results = []
        
        # DP table: dp[i] contains all possible segmentations ending at position i
        dp = [[] for _ in range(n + 1)]
        dp[0] = [[]]  # Empty segmentation at start
        
        for i in range(n + 1):
            if dp[i]:
                for j in range(i + 1, n + 1):
                    word = text[i:j]
                    # Check if word is valid (in dictionary or valid via wordninja)
                    if (word in self.dictionary or 
                        len(wordninja.split(word)) == 1 or 
                        len(word) == 1):  # Allow single letters
                        for segmentation in dp[i]:
                            dp[j].append(segmentation + [word])
        
        # Convert to space-separated strings
        return [' '.join(segmentation) for segmentation in dp[n]]

    def _auto_segment_review(self, review_text, return_all=False):
        """Automatically segment review text with option for all combinations"""
        # Clean the text
        clean_review = re.sub(r'[^\w\s\.!?]', '', review_text.lower())
        clean_review = re.sub(r'\s+', ' ', clean_review).strip()
        
        if return_all:
            # Get all possible segmentations for the clean text (without spaces)
            text_without_spaces = re.sub(r'[^\w]', '', clean_review)
            segmentations = self.all_possible_segmentations(text_without_spaces)
            # Capitalize each segmentation
            return [self._capitalize_sentences(seg) for seg in segmentations]
        else:
            # Use simple segmentation
            text_without_spaces = re.sub(r'[^\w]', '', clean_review)
            segmented_review = self.simple_segmentation(text_without_spaces)
            return self._capitalize_sentences(segmented_review)

    def _capitalize_sentences(self, text):
        """Capitalize the first letter of each sentence after a dot"""
        if not text:
            return text
        
        parts = text.split('.')
        capitalized_parts = []
        
        for i, part in enumerate(parts):
            part = part.strip()
            if part:
                capitalized_part = part[0].upper() + part[1:] if part else ""
                capitalized_parts.append(capitalized_part)
        
        result = '. '.join(capitalized_parts)
        
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
            has_result = "Yes" if movie_id in self.result_data else "No"
            print(f"{i}: {movie_id} - {movie_title} [In results.json: {has_result}]")

    def add_new_review(self, movie_id, review_text, show_all_options=False):
        """Add a new review with optional multiple segmentation display"""
        if movie_id not in self.data:
            print("Movie ID not found!")
            return False
        
        if show_all_options:
            # Show all possible segmentations
            all_segmentations = self._auto_segment_review(review_text, return_all=True)
            
            print(f"\nAll possible segmentations for: '{review_text}'")
            for i, segmentation in enumerate(all_segmentations[:10], 1):  # Limit to first 10
                print(f"{i}. {segmentation}")
            
            if len(all_segmentations) > 10:
                print(f"... and {len(all_segmentations) - 10} more options")
            
            # Let user choose or use the first one
            try:
                choice = input("\nChoose segmentation number (or Enter for first option): ").strip()
                if choice and choice.isdigit():
                    chosen_index = int(choice) - 1
                    if 0 <= chosen_index < len(all_segmentations):
                        segmented_review = all_segmentations[chosen_index]
                    else:
                        segmented_review = all_segmentations[0]
                else:
                    segmented_review = all_segmentations[0]
            except:
                segmented_review = all_segmentations[0]
        else:
            # Use simple segmentation
            segmented_review = self._auto_segment_review(review_text, return_all=False)
        
        self._add_review_to_results(movie_id, segmented_review)
        
        print(f"\nNew review added:")
        print(f"Original: {review_text}")
        print(f"Segmented: {segmented_review}")
        
        self.save_reviews_data()
        return True

    def _add_review_to_results(self, movie_id, segmented_review):
        """Add segmented review to results structure"""
        if movie_id not in self.result_data:
            movie_info = self.data.get(movie_id, {})
            self.result_data[movie_id] = {
                "name": movie_info.get("title", "Unknown Title"),
                "poster": movie_info.get("poster", ""),
                "description": movie_info.get("description", ""),
                "rating": movie_info.get("rating", 0),
                "genres": movie_info.get("genres", []),
                "date_published": movie_info.get("date_published", ""),
                "keywords": movie_info.get("keywords", []),
                "reviews": []
            }
        
        if "reviews" not in self.result_data[movie_id]:
            self.result_data[movie_id]["reviews"] = []
        
        self.result_data[movie_id]["reviews"].append(segmented_review)
        print(f"Added review to results.json")

    def save_reviews_data(self):
        """Save results.json"""
        try:
            with open('results/results.json', 'w', encoding='utf-8') as f:
                json.dump(self.result_data, f, ensure_ascii=False, indent=2)
            print("results.json updated successfully!")
            return True
        except Exception as e:
            print(f"Error saving results.json: {e}")
            return False
        
    def run(self):
        """Main application loop"""
        while True:
            print(f"\n{'='*50}")
            print("ENHANCED REVIEW SEGMENTATION TOOL")
            print("Solves: Single segmentation + All possible combinations")
            print(f"{'='*50}")
            print("1. List all movies")
            print("2. Add new review (single segmentation)")
            print("3. Add new review (choose from all segmentations)")
            print("4. Exit")

            choice = input("\nEnter your choice (1-4): ").strip()

            if choice == "1":
                self.display_movies()
            
            elif choice == "2":
                self.display_movies()
                try:
                    movie_index = int(input("\nEnter movie index: "))
                    movie_id = list(self.data.keys())[movie_index]
                    review_text = input("Enter your new review: ").strip()
                    if review_text:
                        self.add_new_review(movie_id, review_text, show_all_options=False)
                    else:
                        print("No review text provided!")
                except (ValueError, IndexError):
                    print("Invalid input!")
            
            elif choice == "3":
                self.display_movies()
                try:
                    movie_index = int(input("\nEnter movie index: "))
                    movie_id = list(self.data.keys())[movie_index]
                    review_text = input("Enter your new review: ").strip()
                    if review_text:
                        self.add_new_review(movie_id, review_text, show_all_options=True)
                    else:
                        print("No review text provided!")
                except (ValueError, IndexError):
                    print("Invalid input!")
                    
            elif choice == "4":
                print("Exiting.")
                break
            
            else:
                print("Invalid choice! Please enter 1-4.")


def main():
    os.makedirs('data', exist_ok=True)
    os.makedirs('results', exist_ok=True)
    
    segmenter = ReviewSegmenter()
    
    if segmenter.result_data:
        movie_count = len(segmenter.result_data)
        total_reviews = sum(len(movie.get("reviews", [])) for movie in segmenter.result_data.values())
        print(f"Loaded results.json with {movie_count} movies and {total_reviews} reviews")
    
    segmenter.run()


if __name__ == "__main__":
    main()