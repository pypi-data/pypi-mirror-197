import nltk
from nltk.corpus import wordnet
import random

# Define a list of sentence structures and their corresponding synonyms
sentence_structures = [
    ("I am {synonym} about {object}.", ["happy", "glad", "pleased"]),
    ("I am {synonym} at {object}.", ["angry", "irate", "furious"]),
    ("I {synonym} every morning.", ["run", "jog", "sprint"]),
    ("The {object} is {synonym}.", ["big", "large", "enormous"]),
    ("The {object} is {synonym}.", ["small", "tiny", "minuscule"]),
    ("It is {synonym} outside.", ["hot", "warm", "toasty"]),
    ("This is a {synonym} idea.", ["good", "great", "excellent"]),
    ("This is a {synonym} idea.", ["bad", "terrible", "awful"]),
    ("The {object} is {synonym}.", ["beautiful", "gorgeous", "stunning"]),
]


# Define a function to find synonyms of a word using NLTK
def get_synonyms(word):
    synonyms = []
    for syn in wordnet.synsets(word):
        for lemma in syn.lemmas():
            synonym = lemma.name().replace('_', ' ').lower()
            if synonym != word:
                synonyms.append(synonym)
    return list(set(synonyms))


# Define a function to rephrase a sentence using synonyms
def rephrase_sentence(sentence, sentence_structures, custom_synonyms):
    # Loop through each sentence structure
    for structure, base_words in sentence_structures:
        # Tokenize the sentence and extract the base words that match the structure
        tokens = nltk.word_tokenize(sentence)
        base_tokens = [token for token in tokens if token in base_words]

        # If no base words are found, move on to the next structure
        if not base_tokens:
            continue

        # Loop through each base word and replace it with a synonym
        for base_token in base_tokens:
            # Use custom synonyms if available, otherwise use NLTK synonyms
            if base_token in custom_synonyms:
                synonyms = custom_synonyms[base_token]
            else:
                synonyms = get_synonyms(base_token)

            # Choose a random synonym and replace the base word
            if synonyms:
                synonym = random.choice(synonyms)
                sentence = sentence.replace(base_token, synonym)

    return sentence


# Define custom synonyms for certain words
custom_synonyms = {
    "happy": ["joyful", "elated"],
    "angry": ["upset", "mad"],
    "big": ["huge", "enormous"],
    "small": ["tiny", "minuscule"],
    "hot": ["warm", "toasty", "boiling"],
    "good": ["great", "excellent", "superb"],
    "bad": ["terrible", "awful", "dreadful"],
    "beautiful": ["gorgeous", "stunning", "elegant"]
}

while True:
    # Get input from the user
    input_text = input("Enter a sentence to rephrase: ")

    # Rephrase the input sentence using the selected sentence structures and custom synonyms
    output = rephrase_sentence(input_text, sentence_structures, custom_synonyms)

    # Print the rephrased output
    print("Rephrased: " + output)
