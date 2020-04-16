import pandas as pd
import matplotlib.pyplot as plt


if __name__ == '__main__':

    with open("extracted_features/features.csv", "r") as file:
        df = pd.read_csv(file)

    # plt.hist(df[df["relevance"] == 0]["firstColHits"], bins=20, range=(0, 2))
    # plt.hist(df[df["relevance"] == 1]["firstColHits"], bins=20, range=(0, 2))
    # plt.hist(df[df["relevance"] == 2]["firstColHits"], bins=20, range=(0, 2))

    plt.hist(df[df["relevance"] == 1]["firstColHits"], label="1 relevance", range=(0, 5))
    plt.hist(df[df["relevance"] == 2]["firstColHits"], label="2 relevance", range=(0, 5))
    plt.xlabel("First column hits")

    plt.legend()

    plt.show()