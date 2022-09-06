from unittest import TestCase
from AnalyzeText import AnalyzeText

tests = [
    {
        "test": "Sir, I protest. I am not a merry man!",
        "result": ['sir', 'protest', 'merry', 'man']
    },
    {
        "test": "Hello? It is you.",
        "result": ["hello"]
    },
]


class TestAnalyzeText(TestCase):

    def test_filtering(self):
        for test in tests:
            an = AnalyzeText(test['test'])
            filtered = an.get_words()
            print(filtered)
            self.assertEqual(test['result'], filtered)
            print(an.get_word_frequency())


