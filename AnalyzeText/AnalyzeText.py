from string import punctuation
import nltk
import numpy as np
import requests
from wordfreq import zipf_frequency  # https://pypi.org/project/wordfreq/
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.corpus import stopwords
from PyPDF2 import PdfReader
from pickle import dump, load
from os.path import exists
from os import listdir
from bs4 import BeautifulSoup
from collections import namedtuple
import syntok.segmenter as segmenter

nltk.download("stopwords")


class AnalyzeText:

    def __init__(self, text="", language='english', path_c1_zipf=r'AnalyzeText\c1_zipf'):
        self.text = text
        self.filtered_list = None
        self.frequency_list = None
        self.language = language
        self.stop_words = stopwords.words(language)
        self.stop_words.append("'s")

        self.median = None
        self.mean = None

        self.path_c1_zipf = path_c1_zipf
        self.c1_zipf_ceiling = None
        self.get_c1_zipf_ceiling()

    #Get rid of stop words, punctuation marks and there's no repetitions
    #make it and frequency list (lazy)properties!
    def get_words(self):
        words = word_tokenize(self.text)
        #print(f'tokenized {words}')
        filtered_list = [x for word in words if (x := word.casefold())
                         not in self.stop_words and word not in punctuation]
        self.filtered_list = list(set(filtered_list))
        return self.filtered_list

    def get_word_frequency(self):
        self.frequency_list = np.array([zipf_frequency(word, self.language[:2]) for word in self.filtered_list])
        self.median = np.median(self.frequency_list)
        self.mean = np.mean(self.frequency_list)
        return self.frequency_list

    def get_c1_words_from_text(self):
        self.get_words()
        print(f'max zip: {self.c1_zipf_ceiling}')
        ls = [(word, zipf) for word in self.filtered_list if (zipf := zipf_frequency(word, self.language[:2])) <
              self.c1_zipf_ceiling]
        return ls

    def get_sentences_from_text(self):
        sent_detector = nltk.data.load('tokenizers/punkt/english.pickle')
        sentences = sent_detector.tokenize(self.text)
        return sentences

    def get_medium_c1_frequency_from_list(self):
        words = []
        if exists(r"AnalyzeText\word lists\c1 list 1"):
            with open(r"AnalyzeText\word lists\c1 list 1", "rb") as file:
                words = load(file)
        else:
            reader = PdfReader(r"AnalyzeText\word lists\c1.pdf")
            for page in reader.pages:
                for line in page.extract_text().splitlines():
                    if line.count("/") == 2:
                        line = line.split()
                        if len(line) == 1 or not line[1].isascii():
                            words.append(line[0])
            with open(r"AnalyzeText\word lists\c1 list 1", "wb+") as file:
                dump(words, file)
        mm = self.get_mean_median(words)
        print(f'MM from list:\n'
              f'mean: {mm.mean:.3}\n'
              f'median: {mm.median}')
        return mm

    def get_medium_c1_frequency_from_website(self):
        #http://www.wordcyclopedia.com/english/c1
        words = []
        if exists(r"AnalyzeText\word lists\c1 list 2"):
            with open(r"C:AnalyzeText\word lists\c1 list 2", "rb") as file:
                words = load(file)
        else:
            url = "http://www.wordcyclopedia.com/english/c1"
            response = requests.get(url)
            soup = BeautifulSoup(response.content, "html.parser")
            elements = soup.find_all("a", class_="word")
            for word in elements:
                print(word.text)
                words.append(word.text)
            with open(r"AnalyzeText\word lists\c1 list 2", "wb+") as file:
                dump(words, file)
        mm = self.get_mean_median(words)
        print(f'MM from website:\n'
              f'mean: {mm.mean:.3}\n'
              f'median: {mm.median}')
        return mm

    def get_mean_median(self, words):
        words = np.array([zipf_frequency(word, self.language[:2]) for word in words])
        mean = np.mean(words).item()            #item converts to native python type
        median = np.median(words).item()
        MeanMedian = namedtuple("MeanMedian", "mean median")
        mm = MeanMedian(mean, median)
        return mm

    def get_c1_zipf_ceiling(self):
        if exists(self.path_c1_zipf):
            with open(self.path_c1_zipf, 'rb') as f:
                self.c1_zipf_ceiling = load(f)
                print(f'Data loaded from file "c1_zipf": {self.c1_zipf_ceiling}')
        else:
            print('c1_zipf does not exist?')
            print(listdir())
            median_list = self.get_medium_c1_frequency_from_list().median
            median_website = self.get_medium_c1_frequency_from_website().median
            self.c1_zipf_ceiling = round(min(median_list, median_website))
            print(f'c1 in get: {self.c1_zipf_ceiling}')
            with open(r'AnalyzeText\c1_zipf', 'wb+') as f:
                dump(self.c1_zipf_ceiling, f)




