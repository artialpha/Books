from string import punctuation, ascii_letters
import nltk
import numpy as np
import requests
from wordfreq import zipf_frequency  # https://pypi.org/project/wordfreq/
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords, wordnet
from PyPDF2 import PdfReader
from pickle import dump, load
from os.path import exists
from os import listdir
from bs4 import BeautifulSoup
from lemminflect import getAllLemmas, getAllInflections, getLemma  # https://lemminflect.readthedocs.io/en/latest/lemmatizer/
from urllib.request import urlretrieve
from re import finditer, IGNORECASE
from collections import defaultdict
nltk.download("stopwords")
nltk.download('punkt')
nltk.download('wordnet')


class AnalyzeText:

    abbr = ["Mr", "Mrs", "Ms"]

    def __init__(self, text="", language='english', path_c1_zipf=r'AnalyzeText\c1_zipf'):
        self.text = text
        self._words_from_text = None
        self._word_frequencies = None
        self._c1_list = None
        self.language = language
        self.stop_words = stopwords.words(language)
        self.stop_words.append("'s")
        self.stop_words.append("n't")
        self.stop_words.append("'ve")

        self.median = None
        self.mean = None

        self.path_c1_zipf = path_c1_zipf
        self._c1_zipf_ceiling = None
        self.c1_zipf_floor = 0

    @property
    def words_from_text(self):
        if not self._words_from_text:
            words = word_tokenize(self.text)
            self._words_from_text = list({x for word in words if (x := word.casefold())
                                          not in self.stop_words and word not in punctuation})
        return self._words_from_text

    @words_from_text.setter
    def words_from_text(self, value):
        raise AttributeError("YOU CAN'T set filtered list - it can only be obtained from a text!")

    @property
    def word_frequencies(self):
        if not self._word_frequencies:
            self._word_frequencies = np.array([zipf_frequency(word, self.language[:2]) for word in self.words_from_text])
            self.median = np.median(self._word_frequencies)
            self.mean = np.mean(self._word_frequencies)
        return self._word_frequencies

    @word_frequencies.setter
    def word_frequencies(self, value):
        raise AttributeError("YOU CAN'T set frequency list - it can only be obtained from a text!")

    @property
    def c1_zipf_ceiling(self):
        if not self._c1_zipf_ceiling:
            if exists(self.path_c1_zipf):
                with open(self.path_c1_zipf, 'rb') as f:
                    self._c1_zipf_ceiling = load(f)
                    print(f'Data loaded from file "c1_zipf": {self._c1_zipf_ceiling}')
            else:
                print('c1_zipf does not exist?')
                print(f'list of files: {listdir()}')
                median_list = self.get_medium_c1_frequency_from_list()
                median_website = self.get_medium_c1_frequency_from_website()
                self._c1_zipf_ceiling = round(min(median_list, median_website))
                print(f'c1 in get: {self._c1_zipf_ceiling}')
                with open(r'AnalyzeText\c1_zipf', 'wb+') as f:
                    print("I'd like to save this zipf in a file")
                    dump(self._c1_zipf_ceiling, f)
        return self._c1_zipf_ceiling

    @c1_zipf_ceiling.setter
    def c1_zipf_ceiling(self, value):
        if isinstance(value, int) or isinstance(value, float):
            self._c1_zipf_ceiling = value
        else:
            raise ValueError("c1_zipf_ceiling must either int or float")

    # https://www.toe.gr/pluginfile.php?file=%2F2143%2Fmod_resource%2Fcontent%2F1%2FLevel%20C1%20Word%20List.pdf
    def get_medium_c1_frequency_from_list(self):
        if exists(r"AnalyzeText\word lists\median from c1 list pdf"):
            with open(r"AnalyzeText\word lists\median from c1 list pdf", 'rb') as file:
                median = load(file)
                return median
        else:
            words = []
            if exists(r"AnalyzeText\word lists\c1 list from pdf"):
                with open(r"AnalyzeText\word lists\c1 list from pdf", "rb") as file:
                    words = load(file)
                    print("I OPEN A FILE WITH c1 words - LIST")
                    print(f'words: {words}')
            else:
                if not exists(r"AnalyzeText\word lists\c1.pdf"):
                    url = 'https://www.toe.gr/pluginfile.php?file=%2F2143%2Fmod_resource%2' \
                          'Fcontent%2F1%2FLevel%20C1%20Word%20List.pdf'
                    urlretrieve(url, r"AnalyzeText\word lists\c1.pdf")
                reader = PdfReader(r"AnalyzeText\word lists\c1.pdf")
                for page in reader.pages:
                    for line in page.extract_text().splitlines():
                        if line.count("/") == 2:
                            line = line.split()
                            if len(line) == 1 or not line[1].isascii():
                                words.append(line[0])
                with open(r"AnalyzeText\word lists\c1 list from pdf", "wb+") as file:
                    dump(words, file)
            frequencies = np.array([zipf_frequency(word, self.language[:2]) for word in words])
            median = np.median(frequencies).item()
            print(f'Median from list:\n'
                  f'median: {median}')
            with open(r"AnalyzeText\word lists\median from c1 list pdf", "wb+") as file:
                dump(median, file)
            return median

    def get_medium_c1_frequency_from_website(self):
        # http://www.wordcyclopedia.com/english/c1

        if exists(r"AnalyzeText\word lists\median from c1 list website"):
            with open(r"AnalyzeText\word lists\median from c1 list website", 'rb') as file:
                median = load(file)
                return median
        else:
            words = []
            if exists(r"AnalyzeText\word lists\c1 list from website"):
                with open(r"C:AnalyzeText\word lists\c1 list from website", "rb") as file:
                    words = load(file)
                    print("I OPEN A FILE WITH c1 words - WEBSITE")
                    print(f'words: {words}')
            else:
                url = "http://www.wordcyclopedia.com/english/c1"
                response = requests.get(url)
                soup = BeautifulSoup(response.content, "html.parser")
                elements = soup.find_all("a", class_="word")
                for word in elements:
                    #print(word.text)
                    words.append(word.text)
                with open(r"AnalyzeText\word lists\c1 list from website", "wb+") as file:
                    dump(words, file)
            frequencies = np.array([zipf_frequency(word, self.language[:2]) for word in words])
            median = np.median(frequencies).item()
            print(f'MM from website:\n'
                  f'median: {median}')
            with open(r"AnalyzeText\word lists\median from c1 list website", 'wb+') as file:
                dump(median, file)
            return median

    def get_c1_words_from_text(self):
        print(f'max zipf: {self.c1_zipf_ceiling}')
        ls = [(word, zipf) for word in self.words_from_text
              if self.c1_zipf_floor < (zipf := zipf_frequency(word, self.language[:2])) < self.c1_zipf_ceiling]
        return ls

    @staticmethod
    def get_word_positions(text, word, only_start=False):
        positions = finditer(fr'\b({word})\b', text, IGNORECASE)
        if only_start:
            positions = [p.start() for p in positions]
        return positions

    @staticmethod
    def get_context_around_index(text, index, distance=100, get_whole_word=True):
        if get_whole_word:
            start = end = distance

            if index - start > 0 and get_whole_word:
                while text[index-start].isalnum():
                    start -= 1
            else:
                start = index

            if index + end < len(text) and get_whole_word:
                while text[index+end].isalnum():
                    end += 1
            else:
                end = ((len(text)-1) - index)

            return f'"...{text[index-start:index+end]}..."'.replace('\n', '')

        else:
            return text[index-distance:index+distance]

    def get_words_with_context(self, words=None):
        if not words:
            words_with_frequency = self.get_c1_words_from_text()
            words = [word for (word, freq) in words_with_frequency]
        words_with_context = defaultdict(list)
        for word in words:
            positions = self.get_word_positions(self.text, word, only_start=True)
            for index in positions:
                words_with_context[word].append(self.get_context_around_index(self.text, index))

        return words_with_context

    @staticmethod
    def save_words(words_with_context, path='words list.txt', save_lemmas=False):
        lines_to_save = None
        words = [word for word in words_with_context.keys()]
        if save_lemmas:
            lines = []
            for word in words:
                lemma_part = 'lemma: '
                lemmas_dict = defaultdict(list)

                for tag, lemma in getAllLemmas(word).items():
                    lemmas_dict[lemma].append(tag)
                #print(f'{lemmas_dict=}')
                for lemma, tags in lemmas_dict.items():
                    lemma_part += f'{lemma[0]} ({tags[0]}) / '

                word_part = f'word from text: {word}'
                line = f'{lemma_part.rstrip(" /"):<60} {word_part:<30}'
                lines.append(line)
            lines_to_save = lines
        else:
            lines_to_save = words
        with open(path, 'w') as file:
            print(lines_to_save)
            file.write('\n'.join(str(line) for line in lines_to_save))

    @staticmethod
    def save_words_and_context(words_with_context, path='words with context list.txt'):
        words_with_context = [f'{word}: {", ".join(contexts)}\n' for word, contexts in words_with_context.items()]
        with open(path, 'w') as file:
            file.writelines(words_with_context)

    @staticmethod
    def get_words_list_from_file(path='words list.txt'):
        with open(path, 'r') as file:
            words = file.readlines()
            return [word.rstrip('\n') for word in words]

