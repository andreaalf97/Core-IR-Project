import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import patches


def significancy(path="results/significancy.csv") -> pd.DataFrame:
    with open(path, "r") as file:
        df = pd.read_csv(file)

    a = df.sort_values("0_1")
    a_val = list(a["0_1"])
    a = list(a["feature"])
    print("Minimum for a:", df["0_1"].min())
    # print(a)

    b = df.sort_values("0_2")
    b_val = list(b["0_2"])
    b = list(b["feature"])
    print("Minimum for b:", df["0_2"].min())

    c = df.sort_values("1_2")
    c_val = list(c["1_2"])
    c = list(c["feature"])
    print("Minimum for c:", df["1_2"].min())
    print(a)
    print(b)
    print(c)

    df = pd.DataFrame()
    df["0/1"] = a
    df["p-val(0/1)"] = ["%.2e" % i for i in a_val]
    df["0_2"] = b
    df["p-val(0/2)"] = ["%.2e" % i for i in b_val]
    df["1_2"] = c
    df["p-val(1/2)"] = ["%.2e" % i for i in c_val]

    df = df.head(n=10)
    return df


def visualize_gini(path="results/giniSelection.csv"):

    with open(path, "r") as file:
        df = pd.read_csv(file)

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
