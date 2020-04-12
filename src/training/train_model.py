from src.training.model import Model
import pandas as pd


df = pd.read_csv("../resources/extracted_features/features.csv")
model = Model(data=df)
model.extractFeaturesAndLabels()
scores = model.train()
print(scores)
for i in range(1, 60):
    print(i)
    ranking = model.getRankingForQuery(i)
    print(ranking)
    print(model.ndcg_scoring(ranking, i))