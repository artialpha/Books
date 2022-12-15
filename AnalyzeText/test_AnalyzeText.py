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
                # general test
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
                ],
                "lemma": False,
                "inflections": False
            },
            {
                # one word - one sentence
                # sentences that end only with periods
                # No lemma, No inflections
                "text": "I wish I had a motorbike. "
                        "But they are so expensive, I bet my parents would never buy me one. "
                        "I was brought up in a poor family and we can't afford such a thing. "
                        "I will buy a lottery ticket and if I'm lucky, I will have a brand-new machine in no time. "
                        "All my friends will be green with envy. ",
                "words": [
                    "motorbike", "expensive", "poor", "lottery", "envy"
                ],
                "sentences": [
                    ["I wish I had a motorbike."],                                                      # motorbike
                    ["But they are so expensive, I bet my parents would never buy me one."],            # expensive
                    ["I was brought up in a poor family and we can't afford such a thing."],            # poor
                    # lottery (the sentence below)
                    ["I will buy a lottery ticket and if I'm lucky, I will have a brand-new machine in no time."],
                    ["All my friends will be green with envy."],                                        # envy
                ],
                "lemma": False,
                "inflections": False
            },
            {
                # one word - one sentence
                # sentences that end only with various punctuation marks
                # No lemma, No inflections
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
                    "eat", "ice", "run", "lend", "unlucky", "like", "refuse", "annoying", "bar"
                ],
                "sentences": [
                    ["I'd like to eat something sweet."],           # eat
                    ["I think I will buy ice cream!"],              # ice
                    ["But unlucky - I have run out of money."],     # run
                    ["Can you lend me some?"],                      # lend
                    ["But unlucky - I have run out of money."],     # unlucky
                    ["I'd like to eat something sweet.",            # like
                     "Pulling a face like that is not a solution, you know?"],
                    ["There will be a day when you will be the one who asks for a favour,"  # refuse
                     " and I will refuse with a huge smile of satisfaction on my face."],
                    ["You are so annoying."],                       # annoying
                    ["Candies or a bar of chocolate crossed my mind."]                     # bar
                ],
                "lemma": False,
                "inflections": False
            },
            {
                # one word - one sentence
                # sentences that end only with various punctuation marks
                # USE lemma, No inflections
                # in 'words' that I look for i have an inflected word and I want a sentence that contains a lemma
                # eg
                # told - inflected, tell - lemma
                "text": "I'm going to tell her off for what she has done to my car. "
                        "She will go to any lengths to avoid the responsibility for the damaged cause! "
                        "I don't care that she has run out of money and that she has debts to pay back! "
                        "Why didn't she keep her hands off my car then? "
                        "She should learn how to use public transport! ",
                "words": [
                    "told", "gone", 'ran', 'kept', "used"
                ],
                "sentences": [
                    # inflected: told | lemma: tell
                    ["I'm going to tell her off for what she has done to my car."],

                    # inflected: gone | lemma: go
                    ["She will go to any lengths to avoid the responsibility for the damaged cause!"],

                    # inflected: ran | lemma: run
                    ["I don't care that she has run out of money and that she has debts to pay back!"],

                    # inflected: kept | lemma: keep
                    ["Why didn't she keep her hands off my car then?"],

                    # inflected: used | lemma: use
                    ["She should learn how to use public transport!"],
                ],
                "lemma": True,
                "inflections": False
            },
            {
                # one word - one sentence
                # sentences that end only with various punctuation marks
                # USE lemma, No inflections
                # in 'words' that I look for i have an inflected word
                # I want sentences that contain both a lemma and that word
                # eg
                # word that I have in list: told
                # inflected: told, lemma: tell
                # so I look for 'told' and 'tell'
                "text": "I told you not to touch a hot pot! "
                        "Why are you never listening to what I tell you? "
                        "You may have burned your hand! "
                        "As a punishment - you are forbidden to play computer games for a week. ",
                "words": [
                    "told", "burned", "played"
                ],
                "sentences": [
                    # word: inflected(told); sentences with: lemma(tell) + inflected(told)
                    #
                    ["I told you not to touch a hot pot!", "Why are you never listening to what I tell you?"],

                    # word: inflected(burned); sentences with: inflected(burned)
                    ["You may have burned your hand!"],

                    # word: inflected(played); sentences with: lemma(play)
                    ["As a punishment - you are forbidden to play computer games for a week."]
                ],
                "lemma": True,
                "inflections": False
            }
        ]
        for test in tests:
            for word, sentences in zip(test['words'], test['sentences']):
                if not test['lemma'] and not test['inflections']:
                    result = AnalyzeText.get_sentences_for_word(test['text'], word)
                    self.assertEqual(sentences, result)
                if test['lemma']:
                    result = AnalyzeText.get_sentences_for_word(test['text'], word, use_lemma=True)
                    self.assertEqual(sentences, result)
                if test['inflections']:
                    result = AnalyzeText.get_sentences_for_word(test['text'], word, use_inflections=True)
                    #self.assertEqual(sentences, result)




