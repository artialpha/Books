from unittest import TestCase
from AnalyzeText import AnalyzeText
from wordfreq import zipf_frequency

tests = [
    {
        "test": "Sir, I protest. I am not a merry man!",
        "result": ['sir', 'protest', 'merry', 'man']
    },
    {
        "test": "Hello? Hello? Hello? It is you. It's a miracle",
        "result": ["hello", "miracle"]
    },
]

c1_words = ["audible", "asset"]


# noinspection PyCallingNonCallable
class TestAnalyzeText(TestCase):

    def test_filtering(self):
        for test in tests:
            an = AnalyzeText(test['test'])
            filtered = an.get_words()
            print(filtered)
            self.assertEqual(sorted(test['result']), sorted(filtered))
            print(f'zipf: {an.get_word_frequency()}')

    def test_c1_freq(self):
        an = AnalyzeText()
        an.get_medium_c1_frequency()

    def test_zipf(self):
        for word in c1_words:
            print(f"zipf of a c1 word: {zipf_frequency(word, 'en')}")




