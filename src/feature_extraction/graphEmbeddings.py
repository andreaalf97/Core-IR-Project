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
ts = time.time()

early = []
late_max = []
late_sum = []
late_avg = []
table_vectors_dict: dict = {}

print("Loading DB2Ve dataset...")
nlp = Word2Vec.load("../resources/datasets/DB2Vec_cbow_500_5_5_2_500", mmap="r")
print("Finished loading")


# Gets the graph embeddings of given entities from loaded DB2Vec data
def get_graph_embeddings(entities):
    prefix = "http://dbpedia.org/resource/Category:"
    bagUtils.replace_prefix(entities, prefix, 'dct:')
    prefix = "http://dbpedia.org/resource/"
    bagUtils.replace_prefix(entities, prefix, 'dbr:')
    return [np.asarray(nlp.wv[entity]) for entity in entities if entity in nlp.wv.vocab]


# Gets the graph embeddings of a table
def extract_table_graph_embeddings(table):
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
    return tableVector


# Get json data
# Iterate through query table pairs
for i in range(0, len(relevance.data)):
    if currentQuery is not int(relevance.data[i][0]):
        currentQuery = int(relevance.data[i][0])

        # Print progress
        print(currentQuery)
        ts = time.time()
        print(datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S'))

        # Extract query entities
        queryTerms = bagUtils.getQueryTerms(currentQuery)
        entities = []
        for j in range(0, len(queryTerms)):
            entities += dbPediaLoader.get_entity_robust(queryTerms[j], limit=8, excludeCategories=False, onlyDbpedia=True)
        entities = bagUtils.remove_duplicates_from_list(entities)

        # Extract query embeddings from entities
        queryVector = get_graph_embeddings(entities)

    tableId = relevance.data[i][1]
    # Use stored embeddings if available
    if tableId in table_vectors_dict:
        tableVector = table_vectors_dict[tableId]
    else:
        # Else get the embeddings and store them
        table = table_data[tableId]
        tableVector = extract_table_graph_embeddings(table)
        table_vectors_dict[tableId] = tableVector
    fusion_dict = similarity.fusion(tableVector, queryVector, 500)

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
