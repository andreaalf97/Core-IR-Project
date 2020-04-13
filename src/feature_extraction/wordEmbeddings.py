from src.utils.similarity import fusion
from src.utils.globalLoaders import getQueryList, getTableList
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import spacy
import pandas as pd
from gensim.models import KeyedVectors

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


def word_embedding_single_word(words: list, nlp):
    '''This functions receives a list of words and returns their vector
    representations (Token type) based on a pre-loaded model'''
    return [nlp[word] for word in words if word in nlp.vocab]


def getQueryByNumber(id: int, queries: list) -> str:
    '''This function returns the query from its id'''
    for query in queries:
        # print("#" + query[0] + "||" + str(id) + "#", query[0] == id)
        if query[0] == str(id):
            return " ".join(query[1])

    raise Exception("The list of queries does not contain the given id:", id, query[0])


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
    nlp = KeyedVectors.load_word2vec_format("../resources/datasets/GoogleNews-vectors-negative300.bin", binary=True)
    print("Finished loading")

    tables = getTableList()  # The list of all tables
    queries: list = getQueryList()  # The list of all queries

    with open("../resources/extracted_features/features.csv", "r") as file:
        df = pd.read_csv(file)

    if "google_early" in df:
        print("The features are already in the CSV file")
        exit(-1)

    lastQueryNumber = -1  # We keep track of the last loaded query so we don't have to extract embeddings at every cycle

    # This is used to keep track of the tables that have already been
    # vectorized to reload them if necessary
    table_vectors_dict: dict = {}

    # These are the lists of similarities to be added to the csv file
    earlyFusionResults = []
    lateMaxResults = []
    lateSumResults = []
    lateAvgResults = []

    # For each row in the CSV file, I have the table-query pairs
    for index, row in df.iterrows():

        # I save the last vectorization of the query to just reload it if necessary
        # This is because the same query compares in multiple adjacent rows in the file
        if row["queryNumber"] != lastQueryNumber:
            lastQueryNumber = row["queryNumber"]
            query: str = getQueryByNumber(row["queryNumber"], queries)  # Retrieve the query from the id as a string
            query_vectors: list = word_embedding_single_word(  # Extract the word embeddings from the normalized sentence
                normalize_string(query, lemmatizer),
                nlp
            )

        # If the table has already been processed, I just load the vectors from memory
        if row["tableId"] in table_vectors_dict:
            table_vectors: list = table_vectors_dict[row["tableId"]]
        else:
            table: str = getTableById(row["tableId"], tables)  # I retrieve the table as a long string of words
            table_vectors: list = word_embedding_single_word(  # Extract the word embeddings from the normalized sentence
                normalize_string(table, lemmatizer),
                nlp
            )
            table_vectors_dict[row["tableId"]] = table_vectors

        print("QUERY:", query_vectors)
        print("TABLE no duplicates:", table_vectors)

        # This function compare the vectors in the table and in the query with
        # different similarity measure, returned in this dictionary
        fusion_dict: dict = fusion(table_vectors, query_vectors)

        print("Early fusion: %.4f" % fusion_dict["early"])
        earlyFusionResults.append("%.4f" % fusion_dict["early"])

        print("Late-max fusion: %.4f" % fusion_dict["late-max"])
        lateMaxResults.append("%.4f" % fusion_dict["late-max"])

        print("Late-sum fusion: %.4f" % fusion_dict["late-sum"])
        lateSumResults.append("%.4f" % fusion_dict["late-sum"])

        print("Late-avg fusion: %.4f" % fusion_dict["late-avg"])
        lateAvgResults.append("%.4f" % fusion_dict["late-avg"])

        print("=====================")

    # Finally, we add the results to the csv file and save it
    df["google_early"] = earlyFusionResults
    df["google_late_max"] = lateMaxResults
    df["google_late_avg"] = lateAvgResults
    df["google_late_sum"] = lateSumResults

    with open("../resources/extracted_features/features.csv", "w") as file:
        df.to_csv(file)

    exit(0)