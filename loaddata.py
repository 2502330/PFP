def load_reviews(pos_path='data/pos/0_10.txt', neg_path='data/0_2.txt'):
    
    reviews = []
    with open(pos_path, 'r', encoding='utf-8') as f_pos:
        reviews += [line.strip() for line in f_pos if line.strip()]
    with open(neg_path, 'r', encoding='utf-8') as f_neg:
        reviews += [line.strip() for line in f_neg if line.strip()]
    return reviews

def load_afinn_dict(path='data/AFINN-en-165.txt'):
   
    afinn_dict = {}
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            word, score = line.strip().split('\t')
            afinn_dict[word] = int(score)
    return afinn_dict

if __name__ == '__main__':
    reviews = load_reviews()
    afinn_dict = load_afinn_dict()
    print("Data loaded successfully.")
    print(f"Loaded {len(reviews)} reviews")
    print(f"Loaded {len(afinn_dict)} sentiment words")
