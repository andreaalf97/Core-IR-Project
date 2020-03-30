from src.data_processing import data_loader
from src.data_processing.wiki_api_categories import WikiApiCategories
import pandas as pd
from datetime import datetime

loader = data_loader.data_loader()
categoryLoader = WikiApiCategories()

df = pd.DataFrame()
print("Started Processing")
for i in range(loader.start, loader.end):
    print(datetime.now())
    print(i)
    loader.load_file_data(incrementCurrentIndex=True)
    tables = loader.get_table_ids(data=loader.currentData)
    #Use an inner loop to get the individual data
    for j in range(0, len(tables)):
        tableID = tables[j]
        # Get category by page title
        if 'pgTitle' in loader.currentData[tableID]:
            categories = categoryLoader.get_data(loader.currentData[tableID]['pgTitle'])
            categoryFrameColumns = []
            rowValues = []
            #Construct row
            for k in range(0, len(categories)):
                category = categories[k]
                categoryFrameColumns.append(category)
                rowValues.append(1)
            categoryFrame = pd.DataFrame(data=[rowValues], columns=categoryFrameColumns, index=[tableID])
            df = df.append(categoryFrame).fillna(0)
            categories = None
df.to_csv("bag_of_categories.csv")
