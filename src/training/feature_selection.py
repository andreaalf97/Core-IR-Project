from src.training import train_model
import pandas as pd
#This is a script to test feature sets
from src.training.model import Model

df = pd.read_csv("../resources/extracted_features/features.csv")

features = ["earlyWE", "late-maxWE", "late-avgWE", "late-sumWE",
               "cearly", "cmax", "csum", "cavg", "google_early",
               "google_late_max", "google_late_avg", "google_late_sum",
               "eearly", "emax", "esum", "eavg",
                "rdf_early", "rdf_late_max", "rdf_late_sum", "rdf_late_avg"
]

print("Total Score")
total, _, totalTest = train_model.train(df=df, useBaseFeatures=False)
print(total)
totalError = totalTest["test_mean_squared_error"]
print(totalError)

labels = []
ndcgDiff = []
meanErrorDiff = []

for i in range(0, len(features)):
    #Remove one feature from the total list of features to determine its effects
    avg_score, _, testScore = train_model.train(df=df, useBaseFeatures=False, featureToRemoveFromTotal=features[i])
    labels.append(features[i])
    print(avg_score)
    ndcgDiff.append(avg_score-total)
    print(testScore["test_mean_squared_error"])
    meanErrorDiff.append(testScore["test_mean_squared_error"] - totalError)

df = pd.DataFrame(columns=["feature", "NDCG20", "meansquarederror"])
df["feature"] = labels
df["NDCG20"] = ndcgDiff
df["meansquarederror"] = meanErrorDiff
df.to_csv("ablation.csv")
