from typing import List

from src.data_processing.data_loader import data_loader
from src.data_processing.query_loader import query_loader
from src.utils.table import Table
import math
import pandas as pd


def queryIDF(query: list, tables: list) -> dict:
    '''
    query is the query I'm considering now, given as a list of words (strings).
    But tables is the list of ALL tables in the collection, given as a list of Table objects
    '''

    idf = {
        "pageTitle": 0,
        "sectionTitle": 0,
        "tableCaption": 0,
        "tableHeading": 0,
        "tableBody": 0,
        "all": 0
    }

    for word in query:

        occurrencies = {
            "pageTitle": 0,
            "sectionTitle": 0,
            "tableCaption": 0,
            "tableHeading": 0,
            "tableBody": 0,
            "all": 0
        }

        # For each table in the collection, we calculate how many times the word we are considering is in each field
        for table in tables:

            if word in table.pageTitle:
                occurrencies["pageTitle"] += 1

            if word in table.sectionTitle:
                occurrencies["sectionTitle"] += 1

            if word in table.tableCaption:
                occurrencies["tableCaption"] += 1

            if word in table.tableHeadings:
                occurrencies["tableHeading"] += 1

            body = ""
            for i in range(len(table.tableBody)):
                for j in range(len(table.tableBody[i])):
                    body += table.tableBody[i][j] + " "

            if word in body:
                occurrencies["tableBody"] += 1

            allTerms = table.getTableAsString()
            if word in allTerms:
                occurrencies["all"] += 1

        for v in occurrencies:
            idf[v] += round(
                math.log( (len(tables) - occurrencies[v] + 0.5) / (occurrencies[v] + 0.5)),
                4
            )

    return idf


if __name__ == '__main__':
    df = data_loader()  # Create a new data_loader object
    clean_data = df.load_preprocessed_data()  # load the tables from the clean data csv file

    tables = []  # this will contain all the Table objects
    for v in clean_data:
        tables.append(Table(v, clean_data[v]))

    ql = query_loader()  # Create a new query_loader object
    queries: list = ql.data  # retrieve the queries as a list of [query_number, query_string]

    # Open the csv feature file to add the new columns
    with open("../resources/extracted_features/features.csv", "r") as file:
        df = pd.read_csv(file)

    if "pageTitle_idf" in df:
        print("The IDF features are already in the CSV file")
        exit(-1)


    # Create all the new columns
    # df = df.assign(IDF_pageTitle=[0 for i in range(len(df))])
    # df = df.assign(IDF_sectionTitle=[0 for i in range(len(df))])
    # df = df.assign(IDF_tableCaption=[0 for i in range(len(df))])
    # df = df.assign(IDF_tableHeading=[0 for i in range(len(df))])
    # df = df.assign(IDF_tableBody=[0 for i in range(len(df))])
    # df = df.assign(IDF_all=[0 for i in range(len(df))])

    pageTitle_idf = []
    sectionTitle_idf = []
    tableCaption_idf = []
    tableHeading_idf = []
    tableBody_idf = []
    all_idf = []

    for query in queries:

        print(query)

        query_number = query[0]
        query_idf = queryIDF(query[1], tables)

        # idf = {
        #     "pageTitle": 0,
        #     "sectionTitle": 0,
        #     "tableCaption": 0,
        #     "tableHeading": 0,
        #     "tableBody": 0,
        #     "all": 0
        # }

        for i in range(len(df[df.queryNumber == int(query_number)])):
            pageTitle_idf.append("%.4f" % query_idf["pageTitle"])
            sectionTitle_idf.append("%.4f" % query_idf["sectionTitle"])
            tableCaption_idf.append("%.4f" % query_idf["tableCaption"])
            tableHeading_idf.append("%.4f" % query_idf["tableHeading"])
            tableBody_idf.append("%.4f" % query_idf["tableBody"])
            all_idf.append("%.4f" % query_idf["all"])

    df["pageTitle_idf"] = pageTitle_idf
    df["sectionTitle_idf"] = sectionTitle_idf
    df["tableCaption_idf"] = tableCaption_idf
    df["tableHeading_idf"] = tableHeading_idf
    df["tableBody_idf"] = tableBody_idf
    df["all_idf"] = all_idf

    print(df)

    with open("../resources/extracted_features/features.csv", "w") as file:
        df.to_csv(file)