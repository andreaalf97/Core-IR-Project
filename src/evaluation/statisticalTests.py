import pandas as pd
from scipy.stats import shapiro
from scipy.stats import mannwhitneyu


def shapiro_wilk_normality(df: pd.DataFrame, feature_name: str, confidence=0.05) -> (bool, float):
    '''This function returns true if the distribution is considered to be normal and
     the p-value given by the Shapiro-Wilk test of normality'''
    W, p_value = shapiro(df[feature_name])
    return p_value > confidence, p_value


def significance(df: pd.DataFrame, classes=[(0, 1), (0, 2), (1, 2)]) -> list:
    '''This functions receives two distributions and returns the p-value of the Mann-Whitney U test
    X should contain 2 columns: relevance and the considered feature
    If the returned p-value is small, it means the two distributions are very different and are therefore
    very significant for discriminancy'''

    p_values = []
    for t in classes:
        x = df[df["relevance"] == t[0]].drop("relevance", axis=1)
        y = df[df["relevance"] == t[1]].drop("relevance", axis=1)
        W, p_value = mannwhitneyu(x, y)
        p_values.append(p_value)

    return p_values

if __name__ == '__main__':
    with open("../resources/extracted_features/features.csv", "r") as file:
        df = pd.read_csv(file)

    confidence = 0.005
    df = df.drop(["queryNumber", "tableId", "queryContents"], axis=1)

    norm = df.drop("relevance", axis=1)
    found = False
    for feature in norm:
        isNormal, p_value = shapiro_wilk_normality(norm, feature, confidence=confidence)
        if isNormal:
            found = True

    if not found:
        print("All feature are not normally distributed with confidence of", confidence)

    results = {}
    for feature in norm:
        results[feature] = significance(df[["relevance", feature]])

    feature = []
    z_o = []
    z_t = []
    o_t = []
    for f in results:
        feature.append(str(f))
        z_o.append(results[f][0])
        z_t.append(results[f][1])
        o_t.append(results[f][2])

    print(feature)
    print(z_o)
    print(z_t)
    print(o_t)

    df = pd.DataFrame()
    df["feature"] = feature
    df["0_1"] = z_o
    df["0_2"] = z_t
    df["1_2"] = o_t

    with open("../resources/results/significancy.csv", "w") as file:
        df.to_csv(file, index=False)