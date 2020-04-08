from src.utils.globalLoaders import getQueryList, getTableList
from src.data_processing.relevance_loader import RelevanceLoader
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import spacy


def normalize_string(string, lemmatizer: WordNetLemmatizer, remove_stopwords=True) -> list:
    '''This function removes stopwords and lemmatizes the input string, then returns the '''

    # This is because queries will be already tokenized, but tables are just strings
    if type(string) == str:
        string = word_tokenize(string.lower())  # Tokenize the lowercase version of the input

    # Only keep alphanumeric and remove stopwords
    string = [word for word in string if word.isalpha()]

    if remove_stopwords:  # If necessary, we remove the stopwords
        string = [word for word in string if word not in stopwords.words("english")]

    string = [lemmatizer.lemmatize(word) for word in string]  # Lemmatize all words

    return string


def word_embedding(word: str, nlp):
    '''This functions receives a word and return its vector representation based on a pre-loaded dataset'''
    return nlp(word).vector


if __name__ == '__main__':
    lemmatizer = WordNetLemmatizer()

    print("Loading w2v dataset...")
    nlp = spacy.load('en_vectors_web_lg')
    print("Finished loading")

    tables = getTableList()
    queries = getQueryList()

    words = queries[0][1]
    print(words)

    print("Normalizing...")
    words = normalize_string(words, lemmatizer)
    print(words)

    print("Vector representation:")
    w2v = word_embedding("hello", nlp)
    print(words, "-->", w2v)
    print("Vector of size", len(w2v))

