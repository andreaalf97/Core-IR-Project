import requests

class WikiApiCategories:
    def __init__(self):
        self.S = requests.Session()  # Opens the session when the class is instantiated
        self.URL = "https://en.wikipedia.org/w/api.php"  # The URL of the API

    def get_data(self, pageTitle):
        '''Sends a request to the Wikipedia API and returns the category of the page given by pageTitle'''

        # The parameters for the query
        params = {
            "action": "query",
            "format": "json",
            "prop": "categories",
            "titles": pageTitle
        }

        response = self.S.get(url=self.URL, params=params)  # Sends the request and waits for the response
        response = response.json()  # Cast the response to a JSON object

        print(response)

        pages = response["query"]["pages"]

        data = []
        for k, v in pages.items():
            if 'categories' in v:
                for cat in v['categories']:
                    title = cat["title"]
                    prefix = "Category:"
                    if title.startswith(prefix):
                        data.append(title[len(prefix):])
                    else:
                        data.append(title)
        return data
