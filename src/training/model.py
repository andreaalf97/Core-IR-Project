from sklearn.ensemble import RandomForestClassifier
import pandas as pd


class Model:
    def __init__(self, data=[]):
        self.data = data

    def extractFeaturesAndLabels(self):
        # Construct features array
        self.labels = self.data["relevance"]
        self.features = self.data
        #Remove labels from features. We also remove any strings because they can't be converted to floats.
        #TODO: Maybe we should remove the query number as well?
        self.features = self.features.drop(["relevance", "tableId", "queryContents"], axis=1)

    def train(self):
        self.clf = RandomForestClassifier(max_depth=5, random_state=0)
        self.clf.fit(self.features, self.labels)

    def predict(self, item):
        cls =self.clf.predict(item)
        return cls

    def getRankingForQuery(self, queryNumber):
        rankings = []
        for index, row in self.data.iterrows():
            if int(row["queryNumber"]) == queryNumber:
                tableId = row["tableId"]
                rowFrame = row.to_frame().transpose()
                table = rowFrame.drop(["relevance", "tableId", "queryContents"], axis=1)
                cls = self.predict(table)
                rankings.append([tableId, cls[0]])
        #Sort the rankings by relevance before returning it.
        return rankings
