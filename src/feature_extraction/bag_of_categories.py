from src.data_processing import data_loader
import pandas as pd
from src.data_processing import dbPedia_entity_loader
from src.data_processing.relevance_loader import RelevanceLoader

loader = data_loader.DataLoader()
relevance = RelevanceLoader()
dbPediaLoader = dbPedia_entity_loader.dbPediaEntityLoader()

table_data = loader.load_preprocessed_data()

df = pd.DataFrame()

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

#Get json data
#Iterate through query table pairs
for i in range(0, len(relevance.data)):
    print(relevance.data[i][0])
    print(relevance.data[i][1])
    tableId = relevance.data[i][1]
    table = table_data[tableId]
    vectorRepresentation = pd.DataFrame()
    if 'pgTitle' in table:
        entities = dbPediaLoader.get_entity_robust(table['pgTitle'], limit=3, excludeCategories=False)
        categories = getCategoryVector(entities)
    if 'secondTitle' in table:
        entities = dbPediaLoader.get_entity_robust(table['secondTitle'], limit=3, excludeCategories=False)
        categories = getCategoryVector(entities)
    if 'data' in table:
        entities = dbPediaLoader.get_core_column_entities(table['data'])
        categories = getCategoryVector(entities)
    if 'caption' in table:
        entities = dbPediaLoader.get_entity_robust(table['caption'], limit=3, excludeCategories=False)
        categories = getCategoryVector(entities)