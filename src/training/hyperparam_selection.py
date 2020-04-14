from src.training import train_model
import pandas as pd
#I used this in addition to grid search to determine what params are best.
df = pd.read_csv("../resources/extracted_features/features.csv")
best_score = 0
best_depth = 0
for depth in range(1, 15):
    #I used to have an inner loop for the sample split, but found that changing it has no effect on error and variance.
    hyperparams = { "max_depth": depth, "min_sample_split": 2 }
    avg_score = train_model.train(df=df, hyperParams=hyperparams)
    print(depth)
    print(avg_score)
    if avg_score > best_score:
        best_score = avg_score
        best_depth = depth
        print("Update")
        print(best_score)
        print(best_depth)
print("Best Results:")
print(best_score)
print(best_depth)
