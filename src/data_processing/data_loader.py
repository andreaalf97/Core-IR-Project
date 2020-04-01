import json
from pandas import json_normalize

class data_loader:
    '''
    This class is used to load the data recursively and contains all the necessary parameters.
    Table files are saved as 're_tables-*.json' where * is a 4 digit integer starting from 0001
    '''

    filePrefix = "re_tables-"
    suffix = ".json"
    start = 1
    end = 1653 + 1
    data_location = "../resources/data/"
    currentIndex = start

    def __init__(self, startingIndex=1):
        self.currentIndex = startingIndex

    def load_file_data(self, incrementCurrentIndex=False):
        filename = self.get_data_file_location()  # Retrieves the name of the file we currently have to open
        with open(filename, 'r') as f:
            currentData = json.load(f)
            self.currentIndex += (1 if incrementCurrentIndex else 0)  # Increments the index only if required
        return currentData

    def get_table_ids(self, data) -> []:
        tables = []
        for table in data:
            tables.append(table)
        return tables

    def convert_number_to_string(self, number: int) -> str:
        '''Converts an integer to a string'''
        zeros = 4 - len(str(number))
        prefixString = ""
        for i in range(0, zeros):
            prefixString = prefixString + '0'
        value = prefixString + str(number)
        return value

    def get_data_file_location(self) -> str:
        '''Returns the string of the data path'''
        return self.data_location + self.filePrefix + self.convert_number_to_string(self.currentIndex) + self.suffix

help(data_loader)