import os
from unittest import TestCase
from AnalyzeText import AnalyzeText
from os.path import exists
from os import listdir, chdir, getcwd, remove
from pickle import load
from json import load as json_load
from collections import defaultdict


c1_words = ["audible", "asset"]


# noinspection PyCallingNonCallable
class TestAnalyzeTextZIPF(TestCase):
    def setUp(self):
        print('setup before a test!!!')
        print(f'in setup: {os.listdir()}. getcwd: {os.getcwd()}')

        '''
        remove everything to make sure that I will get median even if those files do not exist
        '''
        os.chdir('..')
        if exists(r"AnalyzeText\c1_zipf"):
            os.remove(r'AnalyzeText\c1_zipf')
        if exists(r"AnalyzeText\word lists\c1 list from pdf"):
            os.remove(r'AnalyzeText\word lists\c1 list from pdf')
        if exists(r"AnalyzeText\word lists\median from c1 list pdf"):
            os.remove(r'AnalyzeText\word lists\median from c1 list pdf')
        if exists(r"AnalyzeText\word lists\c1 list from website"):
            os.remove(r'AnalyzeText\word lists\c1 list from website')
        if exists(r"AnalyzeText\word lists\median from c1 list website"):
            os.remove(r'AnalyzeText\word lists\median from c1 list website')

    def tearDown(self):
        print('tear down after a test')
        os.chdir(r'AnalyzeText')
        print(f'{os.listdir()=}')

    def test_c1_zipf_ceiling(self):
        an = AnalyzeText()

        c1_zipf_ceiling = an.c1_zipf_ceiling
        self.assertEqual(4, c1_zipf_ceiling)

        file_with_c1_zipf_ceiling = exists(r"AnalyzeText\c1_zipf")
        self.assertTrue(file_with_c1_zipf_ceiling)

        words_from_c1_list = exists(r"AnalyzeText\word lists\c1 list from pdf")
        self.assertTrue(words_from_c1_list, 'file with words from a c1 list does not exist!')
        median_from_c1_list = exists(r"AnalyzeText\word lists\median from c1 list pdf")
        self.assertTrue(median_from_c1_list, 'file with median from a c1 list does not exist!')

        words_from_c1_list = exists(r"AnalyzeText\word lists\c1 list from website")
        self.assertTrue(words_from_c1_list, 'file with words from a c1 list does not exist!')
        median_from_c1_list = exists(r"AnalyzeText\word lists\median from c1 list website")
        self.assertTrue(median_from_c1_list, 'file with median from a c1 list does not exist!')

    def test_get_median_from_list(self):
        an = AnalyzeText()
        print(f'list of files: {listdir()}')
        pdf_file_exist = exists(r"AnalyzeText\word lists\c1.pdf")
        self.assertTrue(pdf_file_exist, 'list with c1 words does not exist!')

        median = an.get_medium_c1_frequency_from_list()
        print(f'median returned by a function: {median}')
        self.assertEqual(4.14, median)

        words_from_c1_list = exists(r"AnalyzeText\word lists\c1 list from pdf")
        self.assertTrue(words_from_c1_list, 'file with words from a c1 list does not exist!')
        median_from_c1_list = exists(r"AnalyzeText\word lists\median from c1 list pdf")
        self.assertTrue(median_from_c1_list, 'file with median from a c1 list does not exist!')

        with open(r"AnalyzeText\word lists\median from c1 list pdf", mode='rb') as file:
            median_from_file = load(file)
            print(f'median from a file: {median_from_file}')
        self.assertEqual(median, median_from_file)

    def test_get_medium_from_website(self):
        an = AnalyzeText()
        print(f'in test: list of files: {listdir()}')

        median = an.get_medium_c1_frequency_from_website()
        print(f'median returned by a function: {median}')
        self.assertEqual(3.89, median)

        words_from_c1_list = exists(r"AnalyzeText\word lists\c1 list from website")
        self.assertTrue(words_from_c1_list, 'file with words from a c1 list does not exist!')
        median_from_c1_list = exists(r"AnalyzeText\word lists\median from c1 list website")
        self.assertTrue(median_from_c1_list, 'file with median from a c1 list does not exist!')

        with open(r"AnalyzeText\word lists\median from c1 list website", mode='rb') as file:
            median_from_file = load(file)
            print(f'median from a file: {median_from_file}')
        self.assertEqual(median, median_from_file)


# noinspection PyCallingNonCallable
class TestAnalyzeText(TestCase):

    def test_words_from_string(self):
        tests_words_from_text = [
            {
                "test": "Sir, I protest. I am not a merry man!",
                "result": ['sir', 'protest', 'merry', 'man']
            },
            {
                "test": "Hello? Hello? Hello? It is you. It's a miracle",
                "result": ["hello", "miracle"]
            },
            {
                "test": "I have referred to youth seeking light, where many of the old school accuse them "
                "of thoughtlessly seeking only pleasure. I consider this a libel on modern youth.",
                "result": ["referred", 'youth', 'seeking', 'light', 'many', 'old', 'school',
                           'accuse', 'thoughtlessly', 'pleasure', 'consider', 'libel', 'modern']
            }
        ]

        for test in tests_words_from_text:
            an = AnalyzeText(test['test'], path_c1_zipf='c1_zipf')
            #an.get_words()
            filtered = an.words_from_text
            print(filtered)
            self.assertEqual(sorted(test['result']), sorted(filtered))
            #print(f'zipf: {an.get_word_frequency()}')

    def test_words_from_text_forgetting(self):
        with open(fr"data for tests\texts\Forgetting", 'r') as text_file:
            text = text_file.read()
            analyze = AnalyzeText(text)
            words_list = analyze.words_from_text

            self.assertIn('forgetful', words_list)
            self.assertIn('remember', words_list)
            self.assertIn('research', words_list)
            self.assertIn('neuroscientists', words_list)
            self.assertIn('dementia', words_list)
            self.assertIn('lead', words_list)
            self.assertIn('smoothly', words_list)
            self.assertIn('information', words_list)
            self.assertIn('tasks', words_list)
            self.assertIn('no-longer-relevant', words_list)

            self.assertNotIn('are', words_list)
            self.assertNotIn('is', words_list)
            self.assertNotIn('can', words_list)
            self.assertNotIn('a', words_list)
            self.assertNotIn('our', words_list)
            self.assertNotIn('while', words_list)
            self.assertNotIn('she', words_list)
            self.assertNotIn('it', words_list)
            self.assertNotIn("n't", words_list)

            print(f'{words_list=}')



    def test_indices_for_word(self):
        with open(r"data for tests\texts\tests", 'r') as test_file:
            tests = json_load(test_file)

            for test in tests['texts']:
                with open(fr"data for tests\texts\{test['file_name']}", 'r') as text_file:
                    text = text_file.read()

                    for word in test['words']:
                        positions = AnalyzeText.get_word_positions(text, word)

                        for p in positions:
                            self.assertEqual(word, text[p.start():p.end()].lower())
                            print(AnalyzeText.get_context_around_index(text, p.start()))

    def test_gen(self):
        words_with_context = defaultdict(list)
        words_with_context['dog'].append('My dog is filthy')
        words_with_context['cat'].append('A stray cat has to hunt birds to survive')
        words_with_context['cow'].append('cow is a source of milk')
        words_with_context['cow'].append('I have eaten a cow alive')
        AnalyzeText.save_words(words_with_context)
        AnalyzeText.save_words_and_context(words_with_context)

        words = AnalyzeText.get_words_list_from_file()
        self.assertEqual(list(words_with_context.keys()), words)
        remove(r'words list.txt')
        remove(r'words with context list.txt')
