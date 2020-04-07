import requests
from qwikidata.entity import WikidataItem, WikidataLexeme, WikidataProperty
from qwikidata.linked_data_interface import get_entity_dict_from_api
import json

class EntityLoader:
    def __init__(self):
        self.S = requests.Session()
        self.wikiDataUrl = "https://www.wikidata.org/w/api.php?action=wbgetentities&format=json&sites=enwiki&normalize=1&titles="

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

    def retrieveRelatedEntities(self, entityId):
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
        return list_of_entities
