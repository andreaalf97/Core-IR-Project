import os
dirname = os.path.dirname(__file__)

class query_loader:
    fileLocation = "../data/query_data/queries.txt"
    # Data will have the following format: an array containing an array with 2 elements.
    # The first element will contain the query number. The second element will contain the individual words for the query.
    # Element 0 corresponds to query 1
    data = []

    def __init__(self):
        # Read from txt file
        f = open(os.path.join(dirname, self.fileLocation), "r")
        # Split into elements by \n
        unparsedData = str.splitlines(f.read())
        for i in range(0, len(unparsedData)):
            # Split by spaces
            splitStrings = unparsedData[i].split(' ')
            row = [splitStrings[0], splitStrings[1:]]
            self.data.append(row)
