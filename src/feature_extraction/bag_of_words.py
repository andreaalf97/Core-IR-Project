from src.data_processing import data_loader
import pandas as pd

loader = data_loader.data_loader()

df = pd.DataFrame()

for i in range(loader.start, loader.end):
    loader.load_file_data(incrementCurrentIndex=True)
    tables = loader.get_table_ids(data=loader.currentData)
    #Use an inner loop to get the individual data
    #print(len(tables))
    for j in range(0, len(tables)):
        print(j)
        id = tables[j]
        if "title" in loader.currentData[id]:
            print(loader.currentData[id].title)
