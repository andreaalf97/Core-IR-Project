import pandas as pd
from sklearn.metrics import ndcg_score
import numpy as np

from src.data_processing.relevance_loader import RelevanceLoader
# Used to get NGDC scores for the lucene queries

queries = [1, 15, 26]
queryLoader = RelevanceLoader()
queryRelevanceData = queryLoader.data
scores = []

for i in range(0, len(queries)):
    queryNumber = queries[i]
    relevanceScores = []
    ranking = []
    df = pd.read_csv("../resources/results/lucene_baseline/Query " + str(queryNumber) + ".csv")
    for j in range(0, len(queryRelevanceData)):
        relData = queryRelevanceData[j]
        if int(relData[0]) == queryNumber:
            relevanceScores.append(float(relData[2]))
            found = False
            for index, row in df.iterrows():
                tableId = row["tables"]
                score = float(row["scores"])
                if tableId == relData[1]:
                    found = True
                    ranking.append(score)
            if found == False:
                ranking.append(0)
    score = ndcg_score(y_true=np.asarray([ranking]), y_score=np.asarray([relevanceScores]), k=20)
    scores.append(score)
    print(score)
print(sum(scores)/len(scores))
