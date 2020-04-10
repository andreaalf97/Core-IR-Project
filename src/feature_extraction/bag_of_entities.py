import pandas as pd
import numpy as np
import datetime
import time

from src.data_processing import data_loader
from src.data_processing import dbPedia_entity_loader
from src.data_processing.relevance_loader import RelevanceLoader
from src.utils import bagUtils
from src.utils import similarity

loader = data_loader.DataLoader()
dbPediaLoader = dbPedia_entity_loader.dbPediaEntityLoader()
relevance = RelevanceLoader()
table_data = loader.load_preprocessed_data()

currentQuery = 0
df = pd.DataFrame()
queryDf = pd.DataFrame()
ts = time.time()

early = []
late_max = []
late_sum = []
late_avg = []


def get_related_entities_vector(entities):
    related = []
    related.extend(entities)
    for j in entities:
        if "Category:" not in j:
            relatedEntity = dbPediaLoader.get_dbPedia_related_entities(j)
            if len(relatedEntity) > 0:
                related = related + relatedEntity
    return related

#Get json data
#Iterate through query table pairs
for i in range(0, len(relevance.data)):
    if currentQuery is not int(relevance.data[i][0]):
        del queryDf
        queryDf = pd.DataFrame()
        currentQuery = int(relevance.data[i][0])
        print(currentQuery)
        ts = time.time()
        print(datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S'))
        queryTerms = bagUtils.getQueryTerms(currentQuery)
        for j in range(0, len(queryTerms)):
            #Use a higher limit to ensure that you get as many entities as possible for matching.
            entities = dbPediaLoader.get_entity_robust(queryTerms[j], limit=8, excludeCategories=False, onlyDbpedia=True)
            relatedEntities = get_related_entities_vector(entities)
            queryDf = bagUtils.addResourceVectorToBag(relatedEntities, queryDf, "query" + str(currentQuery) + "_" + queryTerms[j])
    tableId = relevance.data[i][1]
    table = table_data[tableId]
    if 'pgTitle' in table:
        entities = dbPediaLoader.get_entity_robust(table['pgTitle'], limit=4, excludeCategories=False, onlyDbpedia=True)
        relatedEntities = get_related_entities_vector(entities)
        df = bagUtils.addResourceVectorToBag(relatedEntities, df, tableId + "pgTitle")
    if 'secondTitle' in table:
        entities = dbPediaLoader.get_entity_robust(table['secondTitle'], limit=4, excludeCategories=False, onlyDbpedia=True)
        relatedEntities = get_related_entities_vector(entities)
        df = bagUtils.addResourceVectorToBag(relatedEntities, df, tableId + "secondTitle")
    if 'data' in table:
        entities = dbPediaLoader.get_core_column_entities(table['data'])
        relatedEntities = get_related_entities_vector(entities)
        df = bagUtils.addResourceVectorToBag(relatedEntities, df, tableId + "data")
    if 'title' in table:
        entities = dbPediaLoader.get_core_title_entities(table['title'])
        relatedEntities = get_related_entities_vector(entities)
        df = bagUtils.addResourceVectorToBag(relatedEntities, df, tableId + "title")
    if 'caption' in table:
        entities = dbPediaLoader.get_entity_robust(table['caption'], limit=4, excludeCategories=False, onlyDbpedia=True)
        relatedEntities = get_related_entities_vector(entities)
        df = bagUtils.addResourceVectorToBag(relatedEntities, df, tableId + "caption")
    # Place query and tables bag of words in same dataframe to ensure that we can get equalized vector lengths
    df = pd.concat([df, queryDf], axis=0, ignore_index=False).fillna(0)
    # Query/Table pair comparisons and similarity scores.
    sim = bagUtils.compute_similarity_metrics(df)
    early.append("%.4f" % sim["early"])
    late_max.append("%.4f" % sim["late-max"])
    late_sum.append("%.4f" % sim["late-sum"])
    late_avg.append("%.4f" % sim["late-avg"])

    #Reset dataframe once bags are generated
    del df
    df = pd.DataFrame()

similarity_measures = pd.DataFrame({
    'eearly': early,
    'emax': late_max,
    'esum': late_sum,
    'eavg': late_avg
})
similarity_measures.to_csv("entity_features.csv")
