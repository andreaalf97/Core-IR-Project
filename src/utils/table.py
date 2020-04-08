from src.data_processing.data_loader import DataLoader

class Table:
    '''This class is used to represent a table object and its parameters'''

    def __init__(self, tableName, pageTitle, sectionTitle, tableCaption, tableHeadings, tableBody):
        '''To initialize this class manually'''
        self.tableName = tableName
        self.pageTitle = pageTitle
        self.sectionTitle = sectionTitle
        self.tableCaption = tableCaption
        self.tableHeadings = tableHeadings
        self.tableBody = tableBody

    # Still working on this
    def __init__(self, tableName, jsonData):
        '''To initialize this class from a JSON file'''
        self.tableName = tableName
        self.pageTitle = jsonData["pgTitle"]
        self.sectionTitle = jsonData["secondTitle"]
        self.tableCaption = jsonData["caption"]
        self.tableHeadings = jsonData["title"]

        self.tableBody = jsonData["data"]  # Please note that each element in this array is a ROW

    def getTableAsString(self):
        result = ""
        result += self.pageTitle + " "
        result += self.sectionTitle + " "
        result += self.tableCaption + " "

        for w in self.tableHeadings:
            result += w + " "

        for i in range(len(self.tableBody)):
            for j in range(len(self.tableBody[i])):
                result += self.tableBody[i][j] + " "

        return result


if __name__ == '__main__':
    dl = DataLoader()  # Instantiate the data loader class
    data = dl.load_preprocessed_data()  # Loads the clean data
    for v in data:
        table = Table(v, data[v])  # Creates a Table object from the JSON file
        break

    #print(table.tableBody)  # Testing if the values are in place