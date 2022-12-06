from unittest import TestCase
from AnalyzeText import AnalyzeText
from wordfreq import zipf_frequency
from json import load

tests_filter = [
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
        for test in tests_filter:
            an = AnalyzeText(test['test'], path_c1_zipf='c1_zipf')
            filtered = an.get_words()
            print(filtered)
            self.assertEqual(sorted(test['result']), sorted(filtered))
            print(f'zipf: {an.get_word_frequency()}')

    def test_sentences_from_text(self):
        with open(r'data for tests\tests sentences', 'r', encoding='utf8') as f:
            tests_sentences = load(f)
            print(tests_sentences)
            print(type(tests_sentences))
            for test in tests_sentences:
                an = AnalyzeText(test['test'], path_c1_zipf='c1_zipf')
                for i, sent in enumerate(an.get_sentences_from_text()):
                    print(i, sent)

    def test_c1_freq(self):
        an = AnalyzeText()
        print(f'c1 zipf ceiling: {an.c1_zipf_ceiling}')

    def test_zipf(self):
        for word in c1_words:
            print(f"zipf of a c1 word: {zipf_frequency(word, 'en')}")




