from string import punctuation, ascii_letters
import nltk
import numpy as np
import requests
from wordfreq import zipf_frequency  # https://pypi.org/project/wordfreq/
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from PyPDF2 import PdfReader
from pickle import dump, load
from os.path import exists
from os import listdir
from bs4 import BeautifulSoup
from lemminflect import getAllLemmas, getAllInflections  # https://lemminflect.readthedocs.io/en/latest/lemmatizer/
from urllib.request import urlretrieve
nltk.download("stopwords")
nltk.download('punkt')


class AnalyzeText:

    abbr = ["Mr", "Mrs", "Ms"]

    def __init__(self, text="", language='english', path_c1_zipf=r'AnalyzeText\c1_zipf'):
        self.text = text
        self._filtered_list = None
        self._frequency_list = None
        self.language = language
        self.stop_words = stopwords.words(language)
        self.stop_words.append("'s")

        self.median = None
        self.mean = None

        self.path_c1_zipf = path_c1_zipf
        self._c1_zipf_ceiling = None
        self.c1_zipf_floor = 0

    @property
    def filtered_list(self):
        if not self._filtered_list:
            words = word_tokenize(self.text)
            self._filtered_list = list({x for word in words if (x := word.casefold())
                                        not in self.stop_words and word not in punctuation})
        return self._filtered_list

    @filtered_list.setter
    def filtered_list(self, value):
        raise AttributeError("YOU CAN'T set filtered list - it can only be obtained from a text!")

    @property
    def frequency_list(self):
        if not self._frequency_list:
            self._frequency_list = np.array([zipf_frequency(word, self.language[:2]) for word in self.filtered_list])
            self.median = np.median(self._frequency_list)
            self.mean = np.mean(self._frequency_list)
        return self._frequency_list

    @frequency_list.setter
    def frequency_list(self, value):
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
        ls = [(word, zipf) for word in self.filtered_list
              if self.c1_zipf_floor < (zipf := zipf_frequency(word, self.language[:2])) < self.c1_zipf_ceiling]
        return ls

    @staticmethod
    def get_word_positions(text, word):
        positions = []
        offset = 0
        text = text.lower()

        while True:
            index = text.find(word, offset)

            if index == -1:
                return positions

            else:
                positions.append(index)
                offset = index + 1

    @staticmethod
    def __get_indices(text, word):
        indices = []
        offset = 0
        word = word
        while True:
            index = text.lower().find(word, offset)
            if index == -1:
                return indices

            if text[index-1] not in ascii_letters and text[(index + len(word))] not in ascii_letters:
                indices.append(index)
            offset = index + 1

    @classmethod
    def __find_dot(cls, text, index, side):
        dot_id = None
        endings = ['!', '?', '.', '...']

        if side == 'start':
            ls = [v for p in endings if (v := text.rfind(p, 0, index)) != -1]
            dot_id = max(ls) if ls else -1
        elif side == 'end':
            ls = [v for p in endings if (v := text.find(p, index + 1)) != -1]
            dot_id = min(ls) if ls else -1
        if dot_id != -1:
            for a in cls.abbr:
                chunk = text[dot_id-4:dot_id]
                if a in chunk:
                    dot_id = cls.__find_dot(text, dot_id, side)
        return dot_id

    @classmethod
    def __get_dots(cls, text, indices):
        dots = []
        for index in indices:
            if (start := cls.__find_dot(text, index, 'start')) == -1:
                start = 0
            else:
                start += 2
            end = cls.__find_dot(text, index, 'end')
            dots.append((start, end))
        return dots

    @classmethod
    def get_sentences_for_word(cls, text, word, *, use_inflections=False, use_lemma=False):
        # noinspection PyShadowingNames
        def get_sentences(text, word):
            indices = cls.__get_indices(text, word)
            dots = cls.__get_dots(text, indices)
            sentences = [text[start:end+1] for start, end in dots]
            return sentences

        sentences = get_sentences(text, word)
        words = set()
        words.add(word)
        if use_lemma:
            lemma = getAllLemmas(word)
            words = words | {lem[0] for lem in lemma.values()}
            # print(f'LEMMA: word: {word}, lemma: {lemma}')

        if use_inflections:
            for w in words:
                inflections = {inf[0] for inf in getAllInflections(w).values()}
                words = words | inflections
            # print(f'INFLECTIONS: {word}: {inflections}')

        print(f'all words: {words}')
        temp = []
        for w in words:
            s = get_sentences(text, w)
            temp.extend(s)
        sentences.extend(temp)

        return set(sentences)

    def get_sentences_for_filtered_words(self, use_inflections=False, use_lemma=False):
        sentences = dict()
        for word in self.filtered_list:
            temp = self.get_sentences_for_word(self.text, word, use_inflections=use_inflections, use_lemma=use_lemma)
            sentences[word] = temp
        return sentences
