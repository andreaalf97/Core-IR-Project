from src.utils.globalLoaders import getQueryList, getTableList
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import spacy
import pandas as pd


def normalize_string(string, lemmatizer: WordNetLemmatizer, remove_stopwords=True, remove_duplicates=True) -> list:
    '''This function removes stopwords and lemmatizes the input string, then returns the normalized list'''

    # This is because queries will be already tokenized, but tables are just strings
    if type(string) == str:
        string = word_tokenize(string.lower())  # Tokenize the lowercase version of the input

    # Only keep alphanumeric and remove stopwords
    string = [word for word in string if word.isalpha()]

    if remove_stopwords:  # If necessary, we remove the stopwords
        string = [word for word in string if word not in stopwords.words("english")]

    string = [lemmatizer.lemmatize(word) for word in string]  # Lemmatize all words

    if remove_duplicates:  # Removing duplicate words
        string = list(dict.fromkeys(string))

    return string


def word_embedding(words: list, nlp):
    '''This functions receives a list of words and returns their vector representations based on a pre-loaded model'''
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
    lemmatizer = WordNetLemmatizer()  # The model used to lemmatize the words

    print("Loading w2v dataset...")
    # Loads the word embeddings model
    # en_core_web_lg is the largest word embeddings core model from spacy
    nlp = spacy.load('en_core_web_lg')
    print("Finished loading")

    tables = getTableList()  # The list of all tables
    queries: list = getQueryList()  # The list of all queries

    with open("../resources/extracted_features/features.csv", "r") as file:
        df = pd.read_csv(file)

    lastQueryNumber = -1  # We keep track of the last loaded query so we don't have to extract embeddings at every cycle
    for index, row in df.iterrows():

        if row["queryNumber"] != lastQueryNumber:
            lastQueryNumber = row["queryNumber"]
            query: str = getQueryByNumber(row["queryNumber"], queries)  # Retrieve the query from the id as a string
            query_vectors: list = word_embedding(  # Extract the word embeddings from the normalized sentence
                normalize_string(query, lemmatizer),
                nlp
            )

        table: str = getTableById(row["tableId"], tables)
        table_vectors: list = word_embedding(  # Extract the word embeddings from the normalized sentence
            normalize_string(table, lemmatizer),
            nlp
        )

        print("QUERY:", query_vectors)
        print("TABLE no duplicates:", table_vectors)

        break
