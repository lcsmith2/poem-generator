import pickle

LEXICON = "NRC-Emotion-Lexicon-Wordlevel-v0.92.txt"
POLARITIES = set(["positive", "negative"])

def save_lexicons(filename):
    emotion_lexicon = {}
    polarity_lexicon = {}
    with open(filename) as file:
        for line in file.readlines():
            word, category, has_association = line.split("\t")
            if has_association.strip() == "1":
                if category in POLARITIES:
                    polarity_lexicon[word] = category
                else:
                    emotion_lexicon[word] = category

    with open("emotion_lexicon.pickle", "wb") as handle:
        pickle.dump(emotion_lexicon, handle, protocol=pickle.HIGHEST_PROTOCOL)
    
    with open("polarity_lexicon.pickle", "wb") as handle:
        pickle.dump(polarity_lexicon, handle, protocol=pickle.HIGHEST_PROTOCOL)

def get_emotion_lexicon():
    with open("emotion_lexicon.pickle", "rb") as handle:
        emotion_lexicon = pickle.load(handle)
    return emotion_lexicon

def get_polarity_lexicon():
    with open("polarity_lexicon.pickle", "rb") as handle:
        polarity_lexicon = pickle.load(handle)
    return polarity_lexicon

def main():
    print()

if __name__ == "__main__":
    main()