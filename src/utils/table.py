from src.data_processing.data_loader import data_loader

class Table:
    '''This class is used to represent a table object and its parameters'''

    def __init__(self, pageTitle, sectionTitle, tableCaption, tableHeadings, tableBody):
        '''To initialize this class manually'''
        self.pageTitle = pageTitle
        self.sectionTitle = sectionTitle
        self.tableCaption = tableCaption
        self.tableHeadings = tableHeadings
        self.tableBody = tableBody

    # Still working on this
    def __init__(self, jsonData):
        '''To initialize this class from a JSON file'''
        self.pageTitle = jsonData
        self.sectionTitle = jsonData
        self.tableCaption = jsonData
        self.tableHeadings = jsonData
        self.tableBody = jsonData
