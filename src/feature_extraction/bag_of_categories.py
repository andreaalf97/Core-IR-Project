from src.data_processing import relevance_loader
from src.data_processing import data_loader
from src.data_processing import query_loader
import pandas as pd

loader = data_loader.DataLoader()
queries = query_loader.QueryLoader()
relevance = relevance_loader.RelevanceLoader()

table_data = loader.load_preprocessed_data()

print("Started Processing")
count = 0
for i in range(0, len(queries.data)):
    df = pd.DataFrame()
    queryNumber = i + 1
    for j in range(0, len(relevance.data)):
        if int(relevance.data[j][0]) is queryNumber:
            tableID = relevance.data[j][1]
            table = table_data[tableID]
            categories = table["categories"]
            categoryFrameColumns = []
            rowValues = []
            #Construct row
            for k in range(0, len(categories)):
                category = categories[k]
                categoryFrameColumns.append(category)
                rowValues.append(1)
            categoryFrame = pd.DataFrame(data=[rowValues], columns=categoryFrameColumns, index=[tableID])
            df = df.append(categoryFrame).fillna(0)
            categories = None
    # Add row for query?
    '''
    queryFrameColumns = []
    rowValues = []
    for j in range(0, len(queries.data[i][1])):
        term = queries.data[i][1][j]
        rowValues.append(1)
        queryFrameColumns.append(term)
    queryFrame = pd.DataFrame(data=[rowValues], columns=queryFrameColumns, index=["query " + str(i)])
    df = df.append(queryFrame).fillna(0)
    '''
    df.to_csv("bag_of_categories/bag_of_categories_" + str(queryNumber) + ".csv")
