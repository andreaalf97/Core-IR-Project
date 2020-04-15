from sklearn.ensemble import RandomForestRegressor, RandomForestClassifier
from sklearn.metrics import ndcg_score, f1_score, explained_variance_score, max_error, mean_squared_error
from sklearn.model_selection import cross_validate, train_test_split
import numpy as np
import pandas as pd


class Model:
    baseDroppedFeatures = ["relevance", "tableId", "queryContents", "queryNumber"]
    baseFeatures = ["queryLength", "queryStringLength", "numCols",
                    "numRows", "firstColHits", "secondColHits", "pageTitle_idf",
                    "sectionTitle_idf", "tableCaption_idf", "tableHeading_idf",
                    "tableBody_idf", "all_idf"]

    def __init__(self, data=[], featuresToAddToBase=[], featureToRemoveFromTotal="", useBaseFeatures=False):
        self.data = data
        self.featuresToAddToBase = featuresToAddToBase
        self.featureToRemoveFromTotal = featureToRemoveFromTotal
        self.useBaseFeatures = useBaseFeatures
        self.extractFeaturesAndLabels()

    def extractFeaturesAndLabels(self):
        # Construct features array
        self.labels = self.data["relevance"]
        #Remove labels from features. We also remove any strings because they can't be converted to floats.
        if self.useBaseFeatures:
            if len(self.featuresToAddToBase) > 0:
                self.features = self.data[self.baseFeatures + self.featuresToAddToBase]
            else:
                self.features = self.data[self.baseFeatures]
        elif len(self.featureToRemoveFromTotal) > 0 :
            self.features = self.data
            self.features = self.features.drop(self.baseDroppedFeatures, axis=1)
            self.features = self.features.drop([self.featureToRemoveFromTotal], axis=1)
        else:
            self.features = self.data
            self.features = self.features.drop(self.baseDroppedFeatures, axis=1)
        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(self.features, self.labels,
                                                                                test_size=0.2, random_state=0,
                                                                                stratify=self.labels)

    def train(self, hyperParams={}):
        max_depth = 5
        min_sample_split = 3
        if "max_depth" in hyperParams:
            max_depth = hyperParams["max_depth"]
        if "min_sample_split" in hyperParams:
            min_sample_split = hyperParams["min_sample_split"]
        self.clf = RandomForestRegressor(max_depth=max_depth, min_samples_split=min_sample_split, random_state=0, oob_score=True)
        results = cross_validate(self.clf, self.features, self.labels, cv=5, verbose=1,
                           scoring=['explained_variance', 'max_error', "neg_mean_squared_error"], n_jobs=-1)
        self.clf.fit(self.X_train, self.y_train)
        test_predictions = self.clf.predict(self.X_test)
        testExplainedVarianceScore = explained_variance_score(self.y_test, test_predictions)
        testMaxError = max_error(self.y_test, test_predictions)
        testMeanSquaredError = mean_squared_error(self.y_test, test_predictions)
        test_results = { 'variance_score': testExplainedVarianceScore, 'test_max_error': testMaxError, 'test_mean_squared_error': testMeanSquaredError }
        return results, test_results

    def predict(self, item):
        cls =self.clf.predict(item)
        return cls

    def getRankingForQuery(self, queryNumber):
        rankings = []
        if self.useBaseFeatures:
            if len(self.featuresToAddToBase) > 0:
                self.rankingData = self.data[self.baseFeatures + self.featuresToAddToBase + self.baseDroppedFeatures]
            else:
                self.rankingData = self.data[self.baseFeatures + self.baseDroppedFeatures]
        elif len(self.featureToRemoveFromTotal) > 0:
            self.rankingData = self.data
            self.rankingData = self.rankingData.drop([self.featureToRemoveFromTotal], axis=1)
        else:
            self.rankingData = self.data
        for index, row in self.rankingData.iterrows():
            if int(row["queryNumber"]) == queryNumber:
                tableId = row["tableId"]
                rowFrame = row.to_frame().transpose()
                table = rowFrame.drop(self.baseDroppedFeatures, axis=1)
                cls = self.predict(table)
                rankings.append([tableId, cls[0]])
        #Sort the rankings by relevance before returning it.
        rankings.sort(key=self.comparator, reverse=True)
        return rankings

    def comparator(self, item):
        return item[1]

    # Rankings is the list of scores for the tables being evaluated for a query.
    # Query number is the query being evaluated
    # K is the number of scores to take into account in the NDCG scoring. E.g., k=20 just looks at top 20 in the ranking.
    def ndcg_scoring(self, rankings, queryNumber, k=20):
        #Get true scores
        trueScores = []
        targetScores = []
        for i in range(0, len(rankings)):
            data = self.data.loc[(self.data['tableId'] == rankings[i][0]) & (self.data['queryNumber'] == queryNumber)]
            trueScores.append(rankings[i][1])
            targetScores.append(int(data["relevance"].iat[0]))
        return ndcg_score(y_true=np.asarray([trueScores]), y_score=np.asarray([targetScores]), k=k)

    def gini_feature_selection(self, path="../resources/results/giniSelection.csv"):
        classifier = RandomForestClassifier(max_depth=5, min_samples_split=3, random_state=0, oob_score=True)
        classifier.fit(self.X_train, self.y_train)

        gini_scores = zip(self.features, classifier.feature_importances_)
        gini_scores = sorted(list(gini_scores), key = lambda x: x[1], reverse=True)

        df = pd.DataFrame()
        df["feature"] = [element[0] for element in gini_scores]
        df["gini_score"] = [element[1] for element in gini_scores]

        with open(path, "w") as file:
            df.to_csv(file)
