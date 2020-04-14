from src.training.model import Model
import pandas as pd


def train(df: pd.DataFrame, featureToRemoveFromTotal=[], featuresToAddToBase=[], hyperParams={}, k=20, useBaseFeatures=False):
    model = Model(data=df,
                  featureToRemoveFromTotal=featureToRemoveFromTotal,
                  featuresToAddToBase=featuresToAddToBase,
                  useBaseFeatures=useBaseFeatures)
    scores, test_results = model.train(hyperParams=hyperParams)
    print(scores)
    print(test_results)
    all_scores = []
    for i in range(1, 61):
        #print(i)
        ranking = model.getRankingForQuery(i)
        #print(ranking)
        ndgc_score = model.ndcg_scoring(ranking, i, k=k)
        #print(ndgc_score)
        all_scores.append(ndgc_score)

    return sum(all_scores) / len(all_scores)


def get_gini_index(df: pd.DataFrame, path="../resources/results/giniSelection.csv") -> None:
    model = Model(data=df)
    model.gini_feature_selection(path=path)

if __name__ == '__main__':
    df = pd.read_csv("../resources/extracted_features/features.csv")
    avg = train(df)
    print(avg)
    get_gini_index(df)
