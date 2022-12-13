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
                        "I told Ms. Blackhole to buy a chair made of wood.",
                        "I had to go for a chair by myself.",
                        "After all, Mrs. Steel "
                        "who likes Mr. Leg who is Ms. Dog's' brother was given the chair which was "
                        "too small for Mrs. Ball who is obese and what makes things worse her husbad "
                        "Mr. Dog is fat too."
                    ],
                    ["I told Ms. Blackhole to buy a chair made of wood."],
                    [
                        "She obviously ignored what I had asked for and bought a sofa.",
                        "I had to go for a chair by myself.",
                        "After all, Mrs. Steel "
                        "who likes Mr. Leg who is Ms. Dog's' brother was given the chair which was "
                        "too small for Mrs. Ball who is obese and what makes things worse her husbad "
                        "Mr. Dog is fat too."
                    ]
                ]
            },
            {

                "text": "I'd like to eat something sweet. "
                        "Candies or a bar of chocolate crossed my mind. "
                        "I think I will buy ice cream! "
                        "But unlucky - I have run out of money. "
                        "Can you lend me some? "
                        "I promise I will pay you back within a week or so."
                        "Why are you calling me a beggar, you are so mean! "
                        "I will never forget that you refused to give me a couple of dollars! "
                        "I wish I had a brother who is not cheap. "
                        "Pulling a face like that is not a solution, you know? "
                        "There will be a day when you will be the one who asks for a favour, "
                        "and I will refuse with a huge smile of satisfaction on my face. "
                        "You are so annoying... Will you change your mind if I ask nicely?",
                "words": [
                    "eat", "ice", "run", "lend", "unlucky", "like", "refuse", "annoy"
                ],
                "sentences": [
                    ["I'd like to eat something sweet."],           # eat
                    ["I think I will buy ice cream!"],              # ice
                    ["But unlucky - I have run out of money."],     # run
                    ["Can you lend me some?"],                      # lend
                    ["But unlucky - I have run out of money."],     # unlucky
                    ["I'd like to eat something sweet.",            # like
                     "Pulling a face like that is not a solution, you know?"],
                    ["I will never forget that you refused to give me a couple of dollars!",    # refuse
                     "There will be a day when you will be the one who asks for a favour,"
                     " and I will refuse with a huge smile of satisfaction on my face."],
                    ["You are so annoying ..."]                     # annoy
                ]
            }
        ]
        for test in tests:
            for word, sentences in zip(test['words'], test['sentences']):
                result = AnalyzeText.get_sentences_for_word(test['text'], word)
                #print(f"result: {result}")
                #print(f"sentenes from test: {sentences}")
                self.assertEqual(result, sentences)





