from src.data_processing import data_loader
import pandas as pd

loader = data_loader.data_loader()

df = pd.DataFrame()

for i in range(loader.start, loader.end):
    loader.load_file_data(incrementCurrentIndex=True)
    tables = loader.get_table_ids(data=loader.currentData)
    #Use an inner loop to get the individual data
    for j in range(0, len(tables)):
        tableID = tables[j]
        if 'title' in loader.currentData[tableID]:
            print(loader.currentData[tableID]['title'])
        if 'pgTitle' in loader.currentData[tableID]:
            print(loader.currentData[tableID]['pgTitle'])
        if 'caption' in loader.currentData[tableID]:
            print(loader.currentData[tableID]['caption'])
        if 'secondTitle' in loader.currentData[tableID]:
            print(loader.currentData[tableID]['secondTitle'])
        if 'data' in loader.currentData[tableID]:
            print(loader.currentData[tableID]['data'])