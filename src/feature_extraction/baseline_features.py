from src.data_processing import relevance_loader
from src.data_processing import data_loader
from src.data_processing import query_loader
import pandas as pd

#This is a script that generates baseline features
relevance = relevance_loader.RelevanceLoader()
loader = data_loader.DataLoader()
queries = query_loader.QueryLoader()
featureColumns = ["queryNumber", "tableId", "queryContents", "relevance", "queryLength", "queryStringLength", "numCols", "numRows", "firstColHits", "secondColHits"]
features = []

#Get json data
table_data = loader.load_preprocessed_data()
for i in range(0, len(relevance.data)):
    #Table data
    table = table_data[relevance.data[i][1]]
    #Query related features
    queryNumber = int(relevance.data[i][0])
    relevanceScore = relevance.data[i][2]
    query = queries.data[queryNumber - 1]
    queryContents = " ".join(query[1])
    #Baseline features
    queryLength = len(query[1])
    queryStringLength = len(queryContents)
    numCols = table['numCols']
    numRows = table['numDataRows']
    #Calculate Hits
    tableData = table['data']
    firstColHits = 0
    secondColHits = 0
    #If there are rows and columns in the table, we can look for hit data
    if numRows > 0 and numCols > 0:
        for j in range(0, len(tableData)):
            if numRows > 0 and len(tableData[j]) > 0:
                for k in range(0, len(query[1])):
                    if query[1][k] in tableData[j][0]:
                        firstColHits = firstColHits + 1
            if numRows > 1 and len(tableData[j]) > 1:
                for k in range(0, len(query[1])):
                    if query[1][k] in tableData[j][1]:
                        secondColHits = secondColHits + 1
    final_row = [queryNumber, relevance.data[i][1], queryContents, relevanceScore, queryLength, queryStringLength, numCols, numRows, firstColHits, secondColHits]
    features.append(final_row)

output = pd.DataFrame(features, columns=featureColumns)
#Remove the index column
output.to_csv("features.csv", index=False)

