import os
from nltk.tokenize import word_tokenize
dirname = os.path.dirname(__file__)

class QueryLoader:
    fileLocation = "../resources/query_data/queries.txt"
    # Data will have the following format: an array containing an array with 2 elements.
    # The first element will contain the query number. The second element will contain
    # the individual words for the query.
    # Element 0 corresponds to query 1
    data = []

    def __init__(self):
        # Read from txt file
        f = open(os.path.join(dirname, self.fileLocation), "r")
        # Split into elements by \n
        unparsed_data = str.splitlines(f.read())
        for line in unparsed_data:
            query_number = line[0]  # The first char is always the query number
            words  = word_tokenize(line[1:].lower())  # We return the lemmatized version of the query

            row = [query_number, words]
            self.data.append(row)
