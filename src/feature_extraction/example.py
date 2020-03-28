from src.data_processing import data_loader

loader = data_loader.data_loader()

for i in range(loader.start, loader.start):
    loader.load_file_data(incrementCurrentIndex=True)
    tables = loader.get_table_ids(data=loader.currentData)
    #Use an inner loop to get the
    print(tables[0])
    print(loader.currentData[tables[0]])
    loader.currentIndex = i