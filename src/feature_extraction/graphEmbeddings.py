import pandas as pd
import numpy as np
import datetime
import time

from src.data_processing import data_loader
from src.data_processing import dbPedia_entity_loader
from src.data_processing.relevance_loader import RelevanceLoader
from src.utils import bagUtils
from src.utils import similarity
from gensim.models import Word2Vec

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

print("Loading w2v dataset...")
# Loads the word embeddings model
# en_core_web_lg is the largest word embeddings core model from spacy
nlp = Word2Vec.load("../resources/datasets/DB2Vec_cbow_500_5_5_2_500", mmap="r")
print("Finished loading")


def get_graph_embeddings(entities):
    prefix = "http://dbpedia.org/resource/Category:"
    bagUtils.replace_prefix(entities, prefix, 'dct:')
    prefix = "http://dbpedia.org/resource/"
    bagUtils.replace_prefix(entities, prefix, 'dbr:')
    return [nlp.wv[entity] for entity in entities if entity in nlp.wv.vocab]


# Get json data
# Iterate through query table pairs
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
            # Use a higher limit to ensure that you get as many entities as possible for matching.
            entities = dbPediaLoader.get_entity_robust(queryTerms[j], limit=8, excludeCategories=False, onlyDbpedia=True)
            queryVector = get_graph_embeddings(entities)
    tableId = relevance.data[i][1]
    table = table_data[tableId]
    tableVector = []
    if 'pgTitle' in table:
        entities = dbPediaLoader.get_entity_robust(table['pgTitle'], limit=4, excludeCategories=False, onlyDbpedia=True)
        tableVector += get_graph_embeddings(entities)
    if 'secondTitle' in table:
        entities = dbPediaLoader.get_entity_robust(table['secondTitle'], limit=4, excludeCategories=False, onlyDbpedia=True)
        tableVector += get_graph_embeddings(entities)
    if 'data' in table:
        entities = dbPediaLoader.get_core_column_entities(table['data'])
        tableVector += get_graph_embeddings(entities)
    if 'title' in table:
        entities = dbPediaLoader.get_core_title_entities(table['title'])
        tableVector += get_graph_embeddings(entities)
    if 'caption' in table:
        entities = dbPediaLoader.get_entity_robust(table['caption'], limit=4, excludeCategories=False, onlyDbpedia=True)
        tableVector += get_graph_embeddings(entities)

    fusion_dict = similarity.fusion(tableVector, queryVector)

    early.append("%.4f" % fusion_dict["early"])
    late_max.append("%.4f" % fusion_dict["late-max"])
    late_sum.append("%.4f" % fusion_dict["late-sum"])
    late_avg.append("%.4f" % fusion_dict["late-avg"])

similarity_measures = pd.DataFrame({
    'rdf_early': early,
    'rdf_late_max': late_max,
    'rdf_late_sum': late_sum,
    'rdf_late_avg': late_avg
})
similarity_measures.to_csv("graph_features.csv")
