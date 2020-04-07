from src.data_processing import data_loader
import pandas as pd
import re
from SPARQLWrapper import SPARQLWrapper, JSON

loader = data_loader.data_loader()

df = pd.DataFrame()


def match_urls(cell):
    return re.match(r'\[(\w*)\|(.*)\]', cell)


def get_dbpedia_entities(cell):
    match = match_urls(cell)
    if match:
        sparql = SPARQLWrapper("http://dbpedia.org/sparql")
        sparql.setReturnFormat(JSON)

        # This query gets the top 10 rdf:type values of an entity
        query = 'SELECT DISTINCT ?o WHERE { dbr:' + match.group(1) + ' ?p ?o } LIMIT 10'
        sparql.setQuery(query)

        # Map results to a list of types
        entity = sparql.query().convert()
        types = map(lambda x: x['o']['value'], entity['results']['bindings'])
        return list(types)


def get_content_entities(table):
    if len(table) == 0:
        return []
    column_entities = [[] for x in range(len(table[0]))]
    for i in range(0, len(table)):
        for j in range(0, len(table[i])):
            cell_entities = get_dbpedia_entities(table[i][j])  # Get entities of a cell
            if cell_entities:
                column_entities[j].append(cell_entities)  # Append entities to current column
    return max(column_entities, key=len)  # Return core column with most entities


for i in range(loader.start, loader.end):
    loader.load_preprocessed_data()
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
            print(get_content_entities(loader.currentData[tableID]['data']))
