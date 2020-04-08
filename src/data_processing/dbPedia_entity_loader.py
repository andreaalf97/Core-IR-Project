import requests
import re
from SPARQLWrapper import SPARQLWrapper, JSON

# This is a class used for handling entities from dbPedia.
# Uses the following api
class dbPediaEntityLoader:
    def __init__(self):
        self.S = requests.Session()
        self.sparql = SPARQLWrapper("http://dbpedia.org/sparql")

    def get_dbpedia_entities(self, entityString, limit=10, excludeCategories=False):
        #SPARQL cannot handle apostrophes, quotes, and empty strings
        if len(entityString) < 1:
            return []
        entityString = entityString.replace("'", "")
        entityString = entityString.replace("\"", "")
        entityString = entityString.replace("\n", " ")
        entityString = entityString.strip()
        # This query gets the top 10 rdf:type values of an entity
        self.sparql.setReturnFormat(JSON)
        # Add 10 to the limit in case we want to filter stuff out later through Python
        query = '''SELECT DISTINCT ?s ( bif:search_excerpt ( bif:vector () , ?o ) ) WHERE {
            ?s ?p ?o .
            FILTER ( bif:contains ( ?o, '"''' + entityString + '''"' ) )
            FILTER(fn:starts-with(STR(?s),"http://dbpedia.org/resource/")).
        }
        LIMIT ''' + str(limit + 10)
        self.sparql.setQuery(query)

        # Map results to a list of types
        entity = self.sparql.query().convert()
        types = list(map(lambda x: x['s']['value'], entity['results']['bindings']))
        if excludeCategories is True:
            types = [x for x in types if "http://dbpedia.org/resource/Category:" not in x]
        types = types[:limit]
        return types

    def get_url_ids(self, cell):
        return list(map(lambda match: match[0], re.findall(r'\[(\w*)\|(.*)\]', cell)))

    def get_core_column_entities(self, table):
        if len(table) == 0:
            return []
        column_entities = [[] for x in range(len(table[0]))]
        for i in range(0, len(table)):
            for j in range(0, len(table[i])):
                cell_entities = self.get_url_ids(table[i][j])  # Get entities of a cell
                if cell_entities:
                    column_entities[j].extend(cell_entities)  # Append entities to current column
        return max(column_entities, key=len)  # Return core column with most entities

    # Takes the returned url of the entity and gets related categories
    def get_dbPedia_categories(self, entity):
        query = '''SELECT * WHERE { <''' + entity + '''> <http://purl.org/dc/terms/subject> ?categories .}'''
        self.sparql.setQuery(query)

        # Map results to a list of types
        categories = self.sparql.query().convert()
        types = map(lambda x: x['categories']['value'], categories['results']['bindings'])
        return list(types)

    # Construct a resource string using an entity label.
    def get_resource_string(self, entityLabel):
        return "<http://dbpedia.org/resource/" + entityLabel

    # This is a method that tries again with the last terms in a string if a query does not return any entities.
    # If a query only consists of two terms, it tries to use one of the terms.
    # If a query has only one term and nothing comes up, you're out of luck.
    def get_entity_robust(self, entityString, limit=10, excludeCategories=False):
        entities = self.get_dbpedia_entities(entityString, limit, excludeCategories)
        terms = entityString.split()
        if len(entities) > 0:
            return entities
        elif len(terms) > 1:
            if len(terms) > 2:
                secondTryString = terms[len(terms)-2] + " " + terms[len(terms)-1]
                entities = self.get_dbpedia_entities(secondTryString, limit, excludeCategories)
            else:
                secondTryString = terms[0]
                entities = self.get_dbpedia_entities(secondTryString, limit, excludeCategories)
        return entities