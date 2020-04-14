from src.training import train_model
import pandas as pd
#This is a script to test feature sets
from src.training.model import Model

df = pd.read_csv("../resources/extracted_features/features.csv")

featureSets = [
    ["earlyWE", "late-maxWE", "late-avgWE", "late-sumWE"],
    ["cearly", "cmax", "csum", "cavg"],
    ["google_early", "google_late_max", "google_late_avg", "google_late_sum"],
    ["eearly", "emax", "esum", "eavg"]
]

labels = ["Word Embeddings", "Categories", "Google", "Entities"]

print("Just The Base")
base_score = train_model.train(df=df, useBaseFeatures=True)
print(base_score)

for i in range(0, len(featureSets)):
    print(labels[i])
    #Check individual features
    for j in range(0, len(featureSets[i])):
        avg_score = train_model.train(df=df, featuresToAddToBase=[featureSets[i][j]], useBaseFeatures=True)
        print(featureSets[i][j])
        print(avg_score)
        print(avg_score-base_score)
    #Check all features in list
    print("All")
    avg_score = train_model.train(df=df, featuresToAddToBase=featureSets[i], useBaseFeatures=True)
    print(avg_score)
    print(avg_score-base_score)
