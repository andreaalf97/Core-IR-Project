from src.data_processing import data_loader
import pandas as pd
from src.data_processing import dbPedia_entity_loader

loader = data_loader.data_loader()
dbPediaLoader = dbPedia_entity_loader.dbPediaEntityLoader()

df = pd.DataFrame()



for i in range(loader.start, loader.end):
    loader.load_preprocessed_data()
    tables = loader.get_table_ids(data=loader.currentData)
    #Use an inner loop to get the individual data
    for j in range(0, len(tables)):
        tableID = tables[j]
        '''
        if 'title' in loader.currentData[tableID]:
            print(loader.currentData[tableID]['title'])
        if 'pgTitle' in loader.currentData[tableID]:
            print(loader.currentData[tableID]['pgTitle'])
        if 'caption' in loader.currentData[tableID]:
            print(loader.currentData[tableID]['caption'])
        if 'secondTitle' in loader.currentData[tableID]:
            print(loader.currentData[tableID]['secondTitle'])
        '''
        if 'data' in loader.currentData[tableID]:
            print(dbPediaLoader.get_core_column_entities(loader.currentData[tableID]['data']))
