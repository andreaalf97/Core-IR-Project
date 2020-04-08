from src.utils.table import Table
from src.data_processing.data_loader import DataLoader
from src.data_processing.query_loader import QueryLoader

# This file contains the functions to quickly load the data from the CSV files


def getTableList() -> list:
    '''This function returns the lost of tables as Table objects'''

    df = DataLoader()  # Create a new data_loader object
    clean_data = df.load_preprocessed_data()  # load the tables from the clean data csv file

    tables = []  # this will contain all the Table objects
    for v in clean_data:
        tables.append(Table(v, clean_data[v]))

    return tables


def getQueryList() -> list:
    '''This function returns the list of queries as a list of [queryNumber: str, queryWords: [str]]'''

    ql = QueryLoader()  # Create a new query_loader object
    queries: list = ql.data  # retrieve the queries as a list of [query_number, query_string]

    return queries
