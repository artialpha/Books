from unittest import TestCase
from AnalyzeText import AnalyzeText

tests = [
    {
        "test": "Sir, I protest. I am not a merry man!",
        "result": ['Sir', 'protest', 'merry', 'man']
    }
]


class TestAnalyzeText(TestCase):

    def test_filtering(self):
        for test in tests:
            an = AnalyzeText(test['test'])
            filtered = an.get_words()
            print(filtered)
            self.assertEqual(test['result'], filtered)


