from unittest import TestCase
from Gutenberg import Gutenberg

titles = ["Pride and Prejudice"]


# noinspection PyCallingNonCallable
class TestGutenberg(TestCase):
    def test_getting_title(self):
        guten = Gutenberg()
        for x in titles:
            result = guten.get_json(x)
            self.assertEqual(x, result['results'][0]['title'])
            text = guten.get_text(x)
            print(text)

    def test_get_json_of_title(self):
        guten = Gutenberg()
        for x in titles:
            json = guten.get_json(x).json()
            print(json)
