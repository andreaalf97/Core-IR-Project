from src.training.model import Model
import pandas as pd


df = pd.read_csv("../resources/extracted_features/features.csv")
model = Model(data=df)
scores, test_results = model.train()
print(scores)
print(test_results)
all_scores = []
for i in range(1, 61):
    print(i)
    ranking = model.getRankingForQuery(i)
    print(ranking)
    ndgc_score = model.ndcg_scoring(ranking, i)
    print(ndgc_score)
    all_scores.append(ndgc_score)

print(sum(all_scores) / len(all_scores))