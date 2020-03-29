from src.data_processing import data_loader
import pandas as pd

loader = data_loader.data_loader()

for i in range(loader.start, loader.end):
    loader.load_file_data(incrementCurrentIndex=True)
    tables = loader.get_table_ids(data=loader.currentData)
    #Use an inner loop to get the individual data
    for j in range(0, len(tables)):
        id = tables[j]
        print(loader.currentData[id])