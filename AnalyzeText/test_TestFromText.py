from unittest import TestCase
from os import listdir, chdir
from TestFromText import TestFromText
from AnalyzeText import AnalyzeText
import inspect


class TestTestFromText(TestCase):

    def setUp(self):
        chdir('..')

    def test_get_question_line(self):
        words = ['dog', 'bird', 'cat', 'cow', 'bull', 'mouse', 'snake', 'crocodile', 'wolf', 'lion', 'goat', 'dragon',
                 'viper', 'sheep', 'doe', 'stag', 'cry', 'yell', 'speak', 'mutter', 'swim', 'speak', 'shut', 'resist']
        for word in words:
            abcd = TestFromText.get_options_line(words, word)
            self.assertEqual(1, abcd.count(word))
            print(abcd)

    def test_create_questions_list(self):
        print(f'{listdir()}')
        with open(r'AnalyzeText\data for tests\texts\Forgetting', mode='r', encoding='utf-8') as f:
            text = f.read()

        an = AnalyzeText(text)
        words_with_context = an.get_words_with_context()
        print(f'{words_with_context=}')
        test = TestFromText(words_with_context)
        questions_list = test.create_questions_with_answers_list()

        print("\nQUESTIONS: \n")
        for question in questions_list:
            print(f'{question}')

    def test_create_test_file_txt(self):
        with open(r'AnalyzeText\data for tests\texts\Forgetting', mode='r', encoding='utf-8') as f:
            text = f.read()

        an = AnalyzeText(text)
        words_with_context = an.get_words_with_context()
        print(f'{words_with_context=}')
        test = TestFromText(words_with_context)
        test.create_test_file_with_questions_answers_txt()

    def test_create_anki_cards(self):
        with open(r'AnalyzeText\data for tests\texts\Forgetting', mode='r', encoding='utf-8') as f:
            text = f.read()

        an = AnalyzeText(text)
        words_with_context = an.get_words_with_context()
        # print(f'{words_with_context=}')
        test = TestFromText(words_with_context)
        test.create_anki_cards()
