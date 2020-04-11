from src.training.model import Model
import pandas as pd


df = pd.read_csv("../resources/extracted_features/features.csv")
model = Model(data=df)
model.extractFeaturesAndLabels()
model.train()
model.getRankingForQuery(1)