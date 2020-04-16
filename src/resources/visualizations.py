import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import patches


def visualize_gini(path="results/giniSelection.csv"):

    with open(path, "r") as file:
        df = pd.read_csv(file)

    print(df)

    baseFeatures = ["queryLength", "queryStringLength", "numCols",
                    "numRows", "firstColHits", "secondColHits", "pageTitle_idf",
                    "sectionTitle_idf", "tableCaption_idf", "tableHeading_idf",
                    "tableBody_idf", "all_idf"]

    colors = []
    for feature in df["feature"]:
        if feature in baseFeatures:
            colors.append("blue")
        else:
            colors.append("skyblue")

    plt.bar(df["feature"], df["gini_score"], color=colors)
    plt.xticks(rotation='vertical')
    plt.ylabel("Feature importance")
    plt.title("Feature importance based on the Gini score for all features")

    bl_patch = patches.Patch(color='blue', label='Baseline features')
    o_patch = patches.Patch(color='skyblue', label='Our features')
    plt.legend(handles=[bl_patch, o_patch])

    plt.show()


def plot_hist(feature: str, path="extracted_features/features.csv", bins=None, range=None):
    with open(path, "r") as file:
        df = pd.read_csv(file)

    plt.hist(df[df["relevance"] == 0][feature], bins=bins, range=range, label="Relevance 0")
    plt.hist(df[df["relevance"] == 1][feature], bins=bins, range=range, label="Relevance 1")
    plt.hist(df[df["relevance"] == 2][feature], bins=bins, range=range, label="Relevance 1")

    plt.xlabel(feature)
    plt.legend()
    plt.show()


if __name__ == '__main__':
    visualize_gini()
