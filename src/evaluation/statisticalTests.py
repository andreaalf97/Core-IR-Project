import pandas as pd
from scipy.stats import shapiro
from scipy.stats import mannwhitneyu


def shapiro_wilk_normality(df: pd.DataFrame, feature_name: str, confidence=0.05) -> (bool, float):
    '''This function returns true if the distribution is considered to be normal and
     the p-value given by the Shapiro-Wilk test of normality'''
    W, p_value = shapiro(df[feature_name])
    return p_value > confidence, p_value


def significance(x: pd.DataFrame, y: pd.DataFrame) -> float:
    '''This functions receives two distributions and returns the p-value of the Mann-Whitney U test
    If the returned p-value is small, it means the two distributions are very different and are therefore
    very significant for discriminancy'''
    W, p_value = mannwhitneyu(x, y)
    return p_value

if __name__ == '__main__':
    with open("../resources/extracted_features/features.csv", "r") as file:
        df = pd.read_csv(file)

    confidence = 0.005
    df = df.drop(["queryNumber", "tableId", "queryContents"], axis=1)

    found = False
    for feature in df:
        isNormal, p_value = shapiro_wilk_normality(df.drop(["relevance"], axis=1), feature, confidence=confidence)
        if isNormal:
            found = True

    if not found:
        print("All feature are not normally distributed with confidence of", confidence)

    for feature in df:
        if(feature != "relevance"):
            pass