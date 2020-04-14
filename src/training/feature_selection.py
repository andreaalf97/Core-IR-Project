from src.training import train_model
import pandas as pd
#This is a script to test feature sets
from src.training.model import Model

df = pd.read_csv("../resources/extracted_features/features.csv")

features = ["earlyWE", "late-maxWE", "late-avgWE", "late-sumWE",
               "cearly", "cmax", "csum", "cavg", "google_early",
               "google_late_max", "google_late_avg", "google_late_sum",
               "eearly", "emax", "esum", "eavg"
]

print("Total Score")
total, _, _ = train_model.train(df=df, useBaseFeatures=False)
print(total)

for i in range(0, len(features)):
    #Remove one feature from the total list of features to determine its effects
    avg_score, _, _ = train_model.train(df=df, useBaseFeatures=False, featureToRemoveFromTotal=features[i])
    print(features[i])
    print(avg_score)
    print(total-avg_score)
