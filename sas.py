import re

def split_into_sentences(text):
    sentences = re.split(r'[.!?]+', text.lower())
    return [s.strip() for s in sentences if s.strip()]

def sliding_window(sentence, sentiments, window_size = 3):
    results = []
    words = sentence.split()
    for i in range(len(words) - window_size + 1):
        window = words[i:i+window_size]
        score = sum(sentiments.get(word, 0) for word in window)
        results.append({
            'window': window,
            'score': score,
            'start': i,
            'end': i + window_size - 1
        })
    return results

def analyze(review, sentiments):
    sentences = split_into_sentences(review)
    sentence_scores = {}

    # Sentence scoring
    for sentence in sentences:
        sentence_score = 0
        phrases = sliding_window(sentence, sentiments, 3)

        for word in phrases:
            word_score = word['score']
            sentence_score += word_score

        # print(f'{sentence} -> {sentence_score}')
        sentence_scores[sentence] = sentence_score

    total_score = sum(sentence_scores.values())

    # Find most positive and negative sentences
    most_pos_sentence = max(sentence_scores, key = sentence_scores.get)
    most_pos_sentence_score = sentence_scores[most_pos_sentence]

    most_neg_sentence = min(sentence_scores, key = sentence_scores.get)
    most_neg_sentence_score = sentence_scores[most_neg_sentence]

    # Paragraph scoring
    paragraphs = []
    paragraph_size = min(3, len(sentences))

    # Paragraph scoring with arbitrary length
    most_pos_paragraph = []
    most_neg_paragraph = []
    most_pos_paragraph_score = float('-inf')
    most_neg_paragraph_score = float('inf')

    # Original fixed-size paragraph scoring
    for i in range(len(sentences) - paragraph_size + 1):
        paragraph = sentences[i:i+paragraph_size]
        paragraph_score = sum([sentence_scores[sentence] for sentence in paragraph])
        paragraphs.append([paragraph, paragraph_score])

    # Paragraph scoring with variable length
    for start in range(len(sentences)):
        current_score = 0
        for end in range(start, len(sentences)):
            current_score += sentence_scores[sentences[end]]
            if current_score > most_pos_paragraph_score:
                most_pos_paragraph_score = current_score
                most_pos_paragraph = sentences[start:end + 1]
            if current_score < most_neg_paragraph_score:
                most_neg_paragraph_score = current_score
                most_neg_paragraph = sentences[start:end + 1]

    # Find most positive and negative paragraphs
    most_pos_paragraph, most_pos_paragraph_score = max(paragraphs, key=lambda x: x[1])
    most_neg_paragraph, most_neg_paragraph_score = min(paragraphs, key=lambda x: x[1])

    # print(f'sentence scores: {sentence_scores}\ntotal score: {total_score}\nmost pos sentence ({most_pos_sentence_score}): {most_pos_sentence}\nmost neg sentence ({most_neg_sentence_score}): {most_neg_sentence}\nmost pos paragraph ({most_pos_paragraph_score}): {most_pos_paragraph}\nmost neg paragraph ({most_neg_paragraph_score}): {most_neg_paragraph}\n')

    return {
        # 'review': review,
        'total_score': total_score,
        'most_pos_sentence': most_pos_sentence,
        'most_neg_sentence': most_neg_sentence,
        'most_pos_paragraph': most_pos_paragraph,
        'most_neg_paragraph': most_neg_paragraph,
    }