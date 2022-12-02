# https://github.com/garethbjohnson/gutendex
import requests


class Gutenberg:
    address = "https://gutendex.com/books/"
    search = "?search="

    def __init__(self):
        self.url = None

    def get_response(self, title):
        def adjust_title(t):
            return t.replace(" ", "%20")
        self.url = f'{self.address}{self.search}{adjust_title(title)}'
        return requests.get(self.url)

    def get_json(self, title):
        json = self.get_response(title).json()
        return json

    def get_text(self, title):
        json = self.get_json(title)
        for result in json['results']:
            formats = result['formats']
            if (text_url := formats.get("text/plain")) is not None:
                print(f'{title}\n'
                      f"number of results: {len(json['results'])}\n"
                      f'number of formats in a result: {len(formats)}\n'
                      f'URL: {self.url}\n'
                      f'Text url: {text_url}')
                text = requests.get(text_url).text
                return text


