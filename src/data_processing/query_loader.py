class query_loader:
    fileLocation = "../data/query_data/queries.txt"
    # Data will have the following format: an array containing an array with 2 elements.
    # The first element will contain the query number. The second element will contain the individual words for the query
    data = []

    def __init__(self):
        # Read from txt file
        f = open(self.fileLocation, "r")
        # Split into elements by \n
        unparsedData = str.splitlines(f.read())
        for i in range(0, len(unparsedData)):
            # Split by spaces
            splitStrings = unparsedData[i].split(' ')
            row = [splitStrings[0], splitStrings[1:]]
            self.data.append(row)
