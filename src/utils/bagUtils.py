import pandas as pd
import itertools
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

from src.data_processing.query_loader import QueryLoader
from src.utils import similarity
import numpy as np

nltk.download('stopwords')
queryLoader = QueryLoader()

def remove_prefix(categories, prefix):
    for i in range(0, len(categories)):
        categories[i] = categories[i].replace(prefix, '')
    return categories

def remove_duplicates_from_list(items):
    items = list(dict.fromkeys(items))
    return items

# Add bag of something row to the bag
def addCategoryVectorToBag(vector, bag, index):
    prefix = "http://dbpedia.org/resource/Category:"
    vector = remove_duplicates_from_list(remove_prefix(vector, prefix))
    if len(vector) > 0:
        row = [1]*len(vector)
        rowFrame = pd.DataFrame(data=[row], columns=vector, index=[index])
        bag = bag.append(rowFrame).fillna(0)
        del rowFrame
        return bag
    else:
        return bag

# Add bag of something row to the bag
def addResourceVectorToBag(vector, bag, index):
    prefix = "http://dbpedia.org/resource/"
    vector = remove_duplicates_from_list(remove_prefix(vector, prefix))
    if len(vector) > 0:
        row = [1] * len(vector)
        rowFrame = pd.DataFrame(data=[row], columns=vector, index=[index])
        bag = bag.append(rowFrame).fillna(0)
        del rowFrame
        return bag
    else:
        return bag

# Returns the search terms used for getting entities for a query
def getQueryTerms(queryNumber):
    query = queryLoader.data[queryNumber - 1][1]
    queryTerms = [" ".join(query)]
    # Run through combinations of the query terms to get richer entity representation
    for i in range(1, len(query)):
        combinations = list(itertools.combinations(query, i))
        for j in range(0, len(combinations)):
            combinationString = " ".join(combinations[j])
            # Make sure string does not contain only stopwords
            text_tokens = word_tokenize(combinationString)
            tokens_without_sw = [word for word in text_tokens if word not in stopwords.words()]
            #If the word contains word that is not a stopword, and it is more than 2 characters, enter it in the query terms.
            if len(tokens_without_sw) > 0 and len(combinationString) > 2:
                queryTerms.append(combinationString)
    return queryTerms

def compute_similarity_metrics(frame):
    query_vectors = []
    table_vectors = []
    for row in frame.itertuples(index=True):
        index = row[0]
        if index.startswith("table-"):
            table_vectors.append(np.array(row[1:]))
        else:
            query_vectors.append(np.array(row[1:]))
    fusion_dict: dict = similarity.fusion(table_terms=list(table_vectors),
                                          query_terms=list(query_vectors),
                                          vector_size=len(query_vectors[0]))
    return fusion_dict