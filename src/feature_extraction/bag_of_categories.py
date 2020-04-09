import nltk

from src.data_processing import data_loader, query_loader
import pandas as pd
from src.data_processing import dbPedia_entity_loader
from src.data_processing.relevance_loader import RelevanceLoader
import itertools
from nltk.corpus import stopwords
nltk.download('stopwords')
from nltk.tokenize import word_tokenize

loader = data_loader.DataLoader()
relevance = RelevanceLoader()
dbPediaLoader = dbPedia_entity_loader.dbPediaEntityLoader()
queryLoader = query_loader.QueryLoader()

table_data = loader.load_preprocessed_data()

df = pd.DataFrame()

def getCategoryVector(entities):
    categories = []
    for j in entities:
        if "Category:" in j:
            categories.append(j)
        else:
            category = dbPediaLoader.get_dbPedia_categories(j)
            if len(category) > 0:
                categories = categories + category
    return categories


# Returns the search terms used for getting entities for a query
def getQueryTerms(queryNumber):
    query = queryLoader.data[queryNumber - 1][1]
    queryTerms = [" ".join(query)]
    # Run through combinations of the query terms to get richer entity representation
    for i in range(2, len(query)):
        combinations = list(itertools.combinations(query, i))
        for j in range(0, len(combinations)):
            combinationString = " ".join(combinations[j])
            # Make sure string does not contain only stopwords
            text_tokens = word_tokenize(combinationString)
            tokens_without_sw = [word for word in text_tokens if word not in stopwords.words()]
            if len(tokens_without_sw) > 0:
                queryTerms.append(combinationString)
    return queryTerms

currentQuery = 0
queryRepresentation = []
#Get json data
#Iterate through query table pairs
for i in range(0, len(relevance.data)):
    print(relevance.data[i][0])
    print(relevance.data[i][1])
    tableId = relevance.data[i][1]
    table = table_data[tableId]
    vectorRepresentation = pd.DataFrame()
    # Logic for getting categories for the query.
    # Get new query representation when we get to a new set of query table pairs.
    if currentQuery is not int(relevance.data[i][0]):
        currentQuery = int(relevance.data[i][0])
        queryTerms = getQueryTerms(currentQuery)
        for j in range(0, len(queryTerms)):
            entities = dbPediaLoader.get_entity_robust(queryTerms[j], limit=5, excludeCategories=False, onlyDbpedia=True)
            categories = getCategoryVector(entities)
    if 'pgTitle' in table:
        entities = dbPediaLoader.get_entity_robust(table['pgTitle'], limit=3, excludeCategories=False)
        categories = getCategoryVector(entities)
    if 'secondTitle' in table:
        entities = dbPediaLoader.get_entity_robust(table['secondTitle'], limit=3, excludeCategories=False)
        categories = getCategoryVector(entities)
    if 'data' in table:
        entities = dbPediaLoader.get_core_column_entities(table['data'])
        categories = getCategoryVector(entities[:3])
    if 'caption' in table:
        entities = dbPediaLoader.get_entity_robust(table['caption'], limit=3, excludeCategories=False)
        categories = getCategoryVector(entities)