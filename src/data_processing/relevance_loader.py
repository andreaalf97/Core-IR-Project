import os
dirname = os.path.dirname(__file__)

# This is a class that reads in data from the qrels txt file and stores it in an array
class RelevanceLoader:
    fileLocation = "../resources/query_data/qrels.txt"
    # The data will have the following format: It is a 2d array. Each array will contain 3 elements.
    # The elements are the query number, the table, and its relevance score in that order.
    data = []

    def __init__(self):
        # Read from txt file
        f = open(os.path.join(dirname, self.fileLocation), "r")
        # Split into elements by \n
        unparsedData = str.splitlines(f.read())
        for i in range(0, len(unparsedData)):
            # Split by \t
            splitData = unparsedData[i].split('\t')
            rowData = [splitData[0], splitData[2], splitData[3]]
            self.data.append(rowData)
