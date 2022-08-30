# https://github.com/garethbjohnson/gutendex
import requests


class Gutenberg:
    address = "https://gutendex.com/books/"
    search = "?search="

    def __init__(self):
        pass

    def get_response_title(self, title):
        def adjust_title(t):
            return t.replace(" ", "%20")
        url = f'{self.address}{self.search}{adjust_title(title)}'
        return requests.get(url)

    def get_json_of_title(self, title):
        json = self.get_response_title(title).json()
        return json
