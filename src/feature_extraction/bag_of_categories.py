from src.data_processing import data_loader, query_loader
import pandas as pd
from src.data_processing import dbPedia_entity_loader
from src.data_processing.relevance_loader import RelevanceLoader

from src.utils import bagUtils

import datetime
import time

loader = data_loader.DataLoader()
relevance = RelevanceLoader()
dbPediaLoader = dbPedia_entity_loader.dbPediaEntityLoader()
queryLoader = query_loader.QueryLoader()

table_data = loader.load_preprocessed_data()

def getCategoryVector(entities):
    categories = []
    for j in entities:
        if "Category:" in j:
            categories.append(j)
        else:
            category = dbPediaLoader.get_dbPedia_categories(j)
            if len(category) > 0:
                categories = categories + category
    return categories

currentQuery = 0
#Get json data
#Iterate through query table pairs
df = pd.DataFrame()
queryDf = pd.DataFrame()
ts = time.time()

early = []
late_max = []
late_sum = []
late_avg = []
print(datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S'))
for i in range(0, len(relevance.data)):
    tableId = relevance.data[i][1]
    table = table_data[tableId]
    # Logic for getting categories for the query.
    # Get new query representation when we get to a new set of query table pairs.
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
            categories = getCategoryVector(entities)
            queryDf = bagUtils.addCategoryVectorToBag(categories, queryDf, "query" + str(currentQuery) + "_" + queryTerms[j])
    if 'pgTitle' in table:
        entities = dbPediaLoader.get_entity_robust(table['pgTitle'], limit=4, excludeCategories=False, onlyDbpedia=True)
        categories = getCategoryVector(entities)
        df = bagUtils.addCategoryVectorToBag(categories, df, tableId + "pgTitle")
    if 'secondTitle' in table:
        entities = dbPediaLoader.get_entity_robust(table['secondTitle'], limit=4, excludeCategories=False, onlyDbpedia=True)
        categories = getCategoryVector(entities)
        df = bagUtils.addCategoryVectorToBag(categories, df, tableId + "secondTitle")
    if 'data' in table:
        entities = dbPediaLoader.get_core_column_entities(table['data'])
        categories = getCategoryVector(entities[:4])
        df = bagUtils.addCategoryVectorToBag(categories, df, tableId + "data")
    if 'title' in table:
        entities = dbPediaLoader.get_core_title_entities(table['title'])
        categories = getCategoryVector(entities[:4])
        df = bagUtils.addCategoryVectorToBag(categories, df, tableId + "title")
    if 'caption' in table:
        entities = dbPediaLoader.get_entity_robust(table['caption'], limit=4, excludeCategories=False, onlyDbpedia=True)
        categories = getCategoryVector(entities)
        df = bagUtils.addCategoryVectorToBag(categories, df, tableId + "caption")
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
    'cearly': early,
    'cmax': late_max,
    'csum': late_sum,
    'cavg': late_avg
})
similarity_measures.to_csv("category_features.csv")
