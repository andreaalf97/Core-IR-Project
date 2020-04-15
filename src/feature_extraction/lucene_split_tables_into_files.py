from src.data_processing.data_loader import DataLoader

loader = DataLoader()
table_data = loader.load_preprocessed_data()

for table in table_data:
    f = open("tables/" + table + ".txt", "w+", encoding="utf-8")
    f.write(str(table_data[table]))
    f.close()