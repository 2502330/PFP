import re
import os

def load_reviews(pos_dir='data/pos', neg_dir='data/neg'):
    reviews = []
    # Read all positive reviews
    for filename in os.listdir(pos_dir):
        file_path = os.path.join(pos_dir, filename)
        if os.path.isfile(file_path):
            with open(file_path, 'r', encoding='utf-8') as f_pos:
                reviews += [line.strip() for line in f_pos if line.strip()]
    # Read all negative reviews
    for filename in os.listdir(neg_dir):
        file_path = os.path.join(neg_dir, filename)
        if os.path.isfile(file_path):
            with open(file_path, 'r', encoding='utf-8') as f_neg:
                reviews += [line.strip() for line in f_neg if line.strip()]
    return reviews

def load_afinn_dict(afinn_path='data/AFINN-en-165.txt'):
    afinn_dict = {}
    with open(afinn_path, 'r', encoding='utf-8') as f:
        for line in f:
            parts = line.strip().split('\t')
            if len(parts) == 2:
                word, score = parts
                afinn_dict[word] = int(score)
    return afinn_dict




def split_into_sentences(text):
    # Simple sentence splitter using regex
    sentences = re.split(r'[.!?]+', text)
    return [s.strip() for s in sentences if s.strip()]

def sliding_window_sentiment_single_sentence(sentence, afinn_dict, window_size=3):
    results = []
    words = sentence.split()
    for i in range(len(words) - window_size + 1):
        window = words[i:i+window_size]
        score = sum(afinn_dict.get(word.lower(), 0) for word in window)
        results.append({
            'window': window,
            'score': score,
            'start': i,
            'end': i + window_size - 1
        })
    return results
if __name__ == '__main__':
    reviews = load_reviews()
    afinn_dict = load_afinn_dict()
    print("Data loaded successfully.")
    print(f"Loaded {len(reviews)} reviews")
    print(f"Loaded {len(afinn_dict)} sentiment words")
    print("Sample reviews:")
    for review in reviews[:5]:
        print(review)
    print("Sample sentiment words:")
    for word in list(afinn_dict.keys())[:5]:
        print(f"{word}: {afinn_dict[word]}")
    # Sliding window sentiment analysis on all sentences of the first review
    print("\nSliding window sentiment (all sentences of first review):")
    first_review = reviews[0]
    sentences = split_into_sentences(first_review)
    for idx, sentence in enumerate(sentences):
        print(f"\nSentence {idx+1}: \"{sentence}\"")
        # Total sentiment score for the sentence
        sentence_score = sum(afinn_dict.get(word.lower(), 0) for word in sentence.split())
        print(f"  Total sentence sentiment score: {sentence_score}")
        window_results = sliding_window_sentiment_single_sentence(sentence, afinn_dict, window_size=3)
        for res in window_results:
            print(f"  Window {res['start']}-{res['end']}: {res['window']} -> Score: {res['score']}")
