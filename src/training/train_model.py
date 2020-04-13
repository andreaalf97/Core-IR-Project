from src.training.model import Model
import pandas as pd


def train(df: pd.DataFrame) -> None:
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


def get_gini_index(df: pd.DataFrame, path="../resources/results/giniSelection.csv") -> None:
    model = Model(data=df)
    model.gini_feature_selection(path=path)


if __name__ == '__main__':
    df = pd.read_csv("../resources/extracted_features/features.csv")
    train(df)
    get_gini_index(df)
