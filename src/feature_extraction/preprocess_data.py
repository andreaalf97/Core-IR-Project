from src.data_processing import data_loader
from src.data_processing import relevance_loader
from src.data_processing.wiki_api_categories import WikiApiCategories
import json

#This is a script used for processing the 1.6m tables and retrieving just the tables that we need for unsupervised learning
loader = data_loader.data_loader()
relevance = relevance_loader.relevance_loader()
categoryLoader = WikiApiCategories()

data_set = {}

# Set up keys
for i in range(0, len(relevance.data)):
    if relevance.data[i][1] not in data_set:
        data_set[relevance.data[i][1]] = {}

# For each table, check if it is a table we need. If it is a table we need, add it to our data set after retrieving its categories.
found = 0
for i in range(loader.start, loader.end):
    print(i)
    loader.load_file_data(incrementCurrentIndex=True)
    tables = loader.get_table_ids(data=loader.currentData)
    #Use an inner loop to get the individual data
    for j in range(0, len(tables)):
        tableID = tables[j]
        if tableID in data_set:
            found = found + 1
            data_set[tableID] = loader.currentData[tableID]
            # Get category by page title
            if 'pgTitle' in loader.currentData[tableID]:
                data_set[tableID]["categories"] = categoryLoader.get_data(loader.currentData[tableID]['pgTitle'])

with open('data.json', 'w') as f:
    json.dump(data_set, f, indent=4, sort_keys=True)

#Should be about 2900 items because of duplicate tables appearing in qrels data.
print(found)
