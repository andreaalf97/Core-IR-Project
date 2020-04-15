from src.training import train_model
import pandas as pd
from src.training.model import Model

#This is a simple script that can be used for getting multiple NDGC scores.

df = pd.read_csv("../resources/extracted_features/features.csv")

k = [5, 10, 15, 20]
model = Model(data=df)
scores, test_results = model.train()
avg_scores = []
for i in range(0, len(k)):
    all_scores = []
    for j in range(1, 61):
        #print(j)
        ranking = model.getRankingForQuery(j)
        #print(ranking)
        ndgc_score = model.ndcg_scoring(ranking, j, k=k[i])
        #print(ndgc_score)
        all_scores.append(ndgc_score)

    avg = sum(all_scores) / len(all_scores)
    print("NDGC: " + str(k[i]))
    print(avg)
    avg_scores.append(avg)