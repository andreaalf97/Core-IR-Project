import requests

class WikiApiCategories:
    def __init__(self):
        self.S = requests.Session()
        self.URL = "https://en.wikipedia.org/w/api.php"
        self.data = []

    def get_data(self, pageTitle):
        self.data = []
        PARAMS = {
            "action": "query",
            "format": "json",
            "prop": "categories",
            "titles": pageTitle
        }

        R = self.S.get(url=self.URL, params=PARAMS)
        DATA = R.json()

        PAGES = DATA["query"]["pages"]

        for k, v in PAGES.items():
            if 'categories' in v:
                for cat in v['categories']:
                    title = cat["title"]
                    prefix = "Category:"
                    if title.startswith(prefix):
                        self.data.append(title[len(prefix):])
                    else:
                        self.data.append(title)
        return self.data
