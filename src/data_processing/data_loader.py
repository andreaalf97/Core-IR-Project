import json
from pandas import json_normalize

class data_loader:
    filePrefix = "re_tables-"
    suffix = ".json"
    start = 1
    end = 1653 + 1
    data_location = "../data/"
    currentIndex = start
    currentData = None
    prepocessedDataFile = "../data/data.json"

    def __init__(self, startingIndex=1):
        self.currentIndex = startingIndex

    def load_file_data(self, incrementCurrentIndex=False):
        # If the file name exists, write a JSON string into the file.
        filename = self.get_data_file_location()
        if filename:
            # Writing JSON data
            with open(filename, 'r') as f:
                self.currentData = json.load(f)
                if incrementCurrentIndex:
                    self.currentIndex = self.currentIndex + 1
                return self.currentData

    def load_preprocessed_data(self):
        # Reading JSON data
        with open(self.prepocessedDataFile, 'r') as f:
            return json.load(f)

    def get_table_ids(self, data):
        tables = []
        for table in data:
            tables.append(table)
        return tables

    def convert_number_to_string(self, number):
        zeros = 4 - len(str(number))
        prefixString = ""
        for i in range(0, zeros):
            prefixString = prefixString + '0'
        value = prefixString + str(number)
        return value

    def get_data_file_location(self):
        return self.data_location + self.filePrefix + self.convert_number_to_string(self.currentIndex) + self.suffix
