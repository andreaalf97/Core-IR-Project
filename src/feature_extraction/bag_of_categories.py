from src.data_processing import data_loader
from src.data_processing.wiki_api_categories import WikiApiCategories
import pandas as pd
from datetime import datetime


if __name__ == '__main__':

    # Creates an instance of the dataloader, it automatically starts from index = 1
    loader = data_loader.data_loader()

    # Creates an instance of the WikiApiCategories class, used to retrieve categories from Wikipedia APIs
    categoryLoader = WikiApiCategories()

    df = pd.DataFrame()
    print("Started Processing")

    # For each table index from start to end
    for i in range(loader.start, loader.end):
        print(datetime.now())
        print(i)
        jsonTable = loader.load_file_data(incrementCurrentIndex=True)
        tables = loader.get_table_ids(data=jsonTable)

        # Use an inner loop to get the individual data
        for tableId in tables:
            # Get category by page title
            if 'pgTitle' in jsonTable[tableId]:
                categories = categoryLoader.get_data(jsonTable[tableId]['pgTitle'])  # Queries Wikipedia
                categoryFrameColumns = []
                rowValues = []
                # Construct row
                for category in categories:
                    categoryFrameColumns.append(category)
                    rowValues.append(1)
                categoryFrame = pd.DataFrame(data=[rowValues], columns=categoryFrameColumns, index=[tableId])
                df = df.append(categoryFrame).fillna(0)
                categories = None
    df.to_csv("bag_of_categories.csv")
