from src.utils.globalLoaders import getQueryList, getTableList
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from src.utils.table import Table
import spacy
import pandas as pd


def normalize_string(string, lemmatizer: WordNetLemmatizer, remove_stopwords=True, remove_duplicates=True) -> list:
    '''This function removes stopwords and lemmatizes the input string, then returns the '''

    # This is because queries will be already tokenized, but tables are just strings
    if type(string) == str:
        string = word_tokenize(string.lower())  # Tokenize the lowercase version of the input

    # Only keep alphanumeric and remove stopwords
    string = [word for word in string if word.isalpha()]

    if remove_stopwords:  # If necessary, we remove the stopwords
        string = [word for word in string if word not in stopwords.words("english")]

    string = [lemmatizer.lemmatize(word) for word in string]  # Lemmatize all words

    if remove_duplicates:
        string = list(dict.fromkeys(string))

    return string


def word_embedding(words: list, nlp):
    '''This functions receives a word and return its vector representation based on a pre-loaded dataset'''
    return [nlp(word) for word in words]


def getQueryByNumber(id: str, queries: list) -> str:
    '''This function returns the query from its id'''

    for query in queries:
        if query[0] == str(id):
            return " ".join(query[1])

    raise Exception("The list of queries does not contain the give id:", id)


def getTableById(id: str, tables: list) -> str:
    '''This function returns a table from its id'''

    for table in tables:
        if table.tableName == id:
            return table.getTableAsString()

    raise Exception("The table with id (", id, ") was not found")


if __name__ == '__main__':
    lemmatizer = WordNetLemmatizer()

    print("Loading w2v dataset...")
    nlp = spacy.load('en_vectors_web_lg')
    print("Finished loading")

    tables = getTableList()
    queries: list = getQueryList()

    with open("../resources/extracted_features/features.csv", "r") as file:
        df = pd.read_csv(file)

    lastQueryNumber = -1
    for index, row in df.iterrows():

        if row["queryNumber"] != lastQueryNumber:
            query: str = getQueryByNumber(row["queryNumber"], queries)  # Retrieve the query from the id as a string
            query_vectors: list = word_embedding(  # Extract the word embeddings from the normalized sentence
                normalize_string(query, lemmatizer),
                nlp
            )

        table: str = getTableById(row["tableId"], tables)

        print("QUERY:", query)
        print("TABLE no duplicates:", len(normalize_string(table, lemmatizer)))



        break

    # words = queries[0][1]
    # print(words)
    #
    # print("Normalizing...")
    # words = normalize_string(words, lemmatizer)
    # print(words)

    # print("Vector representation:")
    # w2v = word_embedding("hello", nlp)
    # print(words, "-->", w2v)
    # print("Vector of size", len(w2v))

