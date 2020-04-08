from src.data_processing import data_loader
import pandas as pd
from src.data_processing import dbPedia_entity_loader
from src.data_processing.relevance_loader import RelevanceLoader

loader = data_loader.DataLoader()
dbPediaLoader = dbPedia_entity_loader.dbPediaEntityLoader()
relevance = RelevanceLoader()
table_data = loader.load_preprocessed_data()

df = pd.DataFrame()

#Get json data
#Iterate through query table pairs
for i in range(0, len(relevance.data)):
    print(relevance.data[i][0])
    tableId = relevance.data[i][1]
    table = table_data[tableId]
    if 'pgTitle' in table:
        print(dbPediaLoader.get_entity_robust(table['pgTitle'], limit=10, excludeCategories=False))
    if 'secondTitle' in table:
        print(dbPediaLoader.get_entity_robust(table['secondTitle'], limit=10, excludeCategories=False))
    if 'data' in table:
        print(dbPediaLoader.get_core_column_entities(table['data']))
    if 'caption' in table:
        print(dbPediaLoader.get_entity_robust(table['caption'], limit=10, excludeCategories=False))