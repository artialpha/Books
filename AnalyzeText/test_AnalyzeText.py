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

    def test_sentences_for_word(self):
        tests = [
            {
                "text": "I told Ms. Blackhole to buy a chair made of wood. She obviously ignored "
                        "what I had asked for and bought a sofa. It drives me crazy when she "
                        "ignores my requests. I had to go for a chair by myself. I keep the sofa "
                        "in the basement. It is covered by a thin layer of dust. After all, Mrs. Steel "
                        "who likes Mr. Leg who is Ms. Dog's' brother was given the chair which was "
                        "too small for Mrs. Ball who is obese and what makes things worse her husbad "
                        "Mr. Dog is fat too.",
                "words": ["chair", "told", "for"],
                "sentences": [
                    [
                        "I told Ms. Blackhole to buy a chair made of wood",
                        "I had to go for a chair by myself",
                        "After all, Mrs. Steel "
                        "who likes Mr. Leg who is Ms. Dog's' brother was given the chair which was "
                        "too small for Mrs. Ball who is obese and what makes things worse her husbad "
                        "Mr. Dog is fat too"
                    ],
                    ["I told Ms. Blackhole to buy a chair made of wood"],
                    [
                        "She obviously ignored what I had asked for and bought a sofa",
                        "I had to go for a chair by myself",
                        "After all, Mrs. Steel "
                        "who likes Mr. Leg who is Ms. Dog's' brother was given the chair which was "
                        "too small for Mrs. Ball who is obese and what makes things worse her husbad "
                        "Mr. Dog is fat too"
                    ]
                ]
            },
            {
                "text": "I'd like to eat something sweet. "
                        "I think I will buy ice cream! But unlucky - I have run out of money!",
                "words": [
                    "eat", "ice", "run"
                ],
                "sentences": [
                    ["I'd like to eat something sweet"], ["I think I will buy ice cream"],
                     ["But unlucky - I have run out of money"]
                ]
            }
        ]
        for test in tests:
            for word, sentences in zip(test['words'], test['sentences']):
                result = AnalyzeText.get_sentences_for_word(test['text'], word)
                print(f"result: {result}")
                print(f"sentenes from test: {sentences}")
                self.assertEqual(result, sentences)





