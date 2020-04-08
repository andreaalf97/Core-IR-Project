import requests
import re
from SPARQLWrapper import SPARQLWrapper, JSON

# This is a class used for handling entities from dbPedia.
# Uses the following api
class dbPediaEntityLoader:
    def __init__(self):
        self.S = requests.Session()
        self.sparql = SPARQLWrapper("http://dbpedia.org/sparql")

    def match_urls(self, cell):
        return re.match(r'\[(\w*)\|(.*)\]', cell)

    def get_dbpedia_entities(self, entityString):
        # This query gets the top 10 rdf:type values of an entity
        query = '''SELECT DISTINCT ?s ( bif:search_excerpt ( bif:vector () , ?o ) ) WHERE {
            ?s ?p ?o .
            FILTER ( bif:contains ( ?o, '"''' + entityString + '''"' ) )
            FILTER(fn:starts-with(STR(?s),"http://dbpedia.org/resource/")).
        }
        LIMIT 10'''
        self.sparql.setQuery(query)

        # Map results to a list of types
        entity = self.sparql.query().convert()
        types = map(lambda x: x['s']['value'], entity['results']['bindings'])
        return list(types)

    def get_dbpedia_entities_by_cell(self, cell):
        match = self.match_urls(cell)
        if match:
            self.sparql.setReturnFormat(JSON)
            return self.get_dbpedia_entities(match.group(1))

    def get_core_column_entities(self, table):
        if len(table) == 0:
            return []
        column_entities = [[] for x in range(len(table[0]))]
        for i in range(0, len(table)):
            for j in range(0, len(table[i])):
                cell_entities = self.get_dbpedia_entities_by_cell(table[i][j])  # Get entities of a cell
                if cell_entities:
                    column_entities[j].append(cell_entities)  # Append entities to current column
        return max(column_entities, key=len)  # Return core column with most entities

    # Takes the returned url of the entity and gets related categories
    def get_dbPedia_categories(self, entity):
        query = '''SELECT * WHERE { <''' + entity + '''> <http://purl.org/dc/terms/subject> ?categories .}'''
        self.sparql.setQuery(query)

        # Map results to a list of types
        categories = self.sparql.query().convert()
        types = map(lambda x: x['categories']['value'], categories['results']['bindings'])
        return list(types)