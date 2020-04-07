import requests
from qwikidata.linked_data_interface import get_entity_dict_from_api

# This is a class used for handling entities from WikiData
class WikiDataEntityLoader:
    def __init__(self):
        self.S = requests.Session()
        self.wikiDataUrl = "https://www.wikidata.org/w/api.php?action=wbgetentities&format=json&sites=enwiki&normalize=1&titles="
        self.wikiDataEntityIDUrl = "https://www.wikidata.org/wiki/Special:EntityData/"

    #When provided with a string, it tries to get an entity in Wikipedia that matches that
    def retrieveEntityByName(self, entityString):
        # Get entity id
        R = self.S.get(url=self.wikiDataUrl + entityString)
        DATA = R.json()
        entities = DATA["entities"]
        #It really should just be one entity
        entityId = next(iter(entities))
        entity = entities[entityId]
        label = entity["labels"]["en"]["value"]
        return {'id': entityId, 'title': label}

    def retrieveEntityByID(self, entityID):
        # Get entity by id
        R = self.S.get(url=self.wikiDataEntityIDUrl + entityID + ".json")
        DATA = R.json()
        entity = DATA["entities"][entityID]
        label = entity["labels"]["en"]["value"]
        return {'id': entityID, 'title': label}


    # When provided with an entity, try to find all related main entities.
    # Allows for just a small number of entities to be returned if needed.
    def retrieveRelatedEntities(self, entityId, limit=None):
        entity_dict = get_entity_dict_from_api(entityId)
        list_of_entities = []
        claims = entity_dict["claims"]
        #Format of json data is quite nested
        for i in claims:
            for item in claims[i]:
                if "mainsnak" in item:
                    if item["mainsnak"]["datatype"] == "wikibase-item":
                        datavalue = item["mainsnak"]["datavalue"]
                        if datavalue["type"] == "wikibase-entityid":
                            entity = datavalue["value"]["id"]
                            list_of_entities.append(entity)
                            if limit is not None and len(list_of_entities) == limit:
                                return list_of_entities
        return list_of_entities
