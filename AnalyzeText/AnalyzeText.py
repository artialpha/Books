from string import punctuation
import nltk
import numpy as np
import requests
from wordfreq import zipf_frequency  # https://pypi.org/project/wordfreq/
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from PyPDF2 import PdfReader
from pickle import dump, load
from os.path import exists
from bs4 import BeautifulSoup
from collections import namedtuple
nltk.download("stopwords")


class AnalyzeText:

    def __init__(self, text="", language='english'):
        self.text = text
        self.filtered_dict = None
        self.frequency_list = None
        self.language = language
        self.stop_words = stopwords.words(language)
        self.stop_words.append("'s")

        self.median = None
        self.mean = None

    #Get rid of stop words, punctuation marks and there's no repetitions
    def get_words(self):
        words = word_tokenize(self.text)
        print(f'tokenized {words}')
        filtered_list = [x for word in words if (x := word.casefold())
                         not in self.stop_words and word not in punctuation]
        self.filtered_dict = list(set(filtered_list))
        return self.filtered_dict

    def get_word_frequency(self):
        self.frequency_list = np.array([zipf_frequency(word, self.language[:2]) for word in self.filtered_dict])
        self.median = np.median(self.frequency_list)
        self.mean = np.mean(self.frequency_list)

        print("a frequent word 'kind':", zipf_frequency("kind", self.language[:2])) # 5.45
        print("a rare word 'benevolence':", zipf_frequency("benevolence", self.language[:2]))   # 2.78

        return self.frequency_list

    def get_medium_c1_frequency_from_list(self):
        words = []
        if exists("c1 list 1"):
            with open("c1 list 1", "rb") as file:
                words = load(file)
        else:
            reader = PdfReader("c1.pdf")
            for page in reader.pages:
                for line in page.extract_text().splitlines():
                    if line.count("/") == 2:
                        line = line.split()
                        if len(line) == 1 or not line[1].isascii():
                            words.append(line[0])
            with open("c1 list 1", "wb+") as file:
                dump(words, file)
        print(words)
        print(len(words))
        mm = self.get_mean_median(words)
        print(f'MM from list:\n'
              f'mean: {mm.mean:.3}\n'
              f'median: {mm.median}')

    def get_medium_c1_frequency_from_website(self):
        #http://www.wordcyclopedia.com/english/c1
        words = []
        if exists("c1 list 2"):
            with open("c1 list 2", "rb") as file:
                words = load(file)
        else:
            url = "http://www.wordcyclopedia.com/english/c1"
            response = requests.get(url)
            soup = BeautifulSoup(response.content, "html.parser")
            elements = soup.find_all("a", class_="word")
            for word in elements:
                print(word.text)
                words.append(word.text)
            with open("c1 list 2", "wb+") as file:
                dump(words, file)
        mm = self.get_mean_median(words)
        print(f'MM from website:\n'
              f'mean: {mm.mean:.3}\n'
              f'median: {mm.median}')

    def get_mean_median(self, words):
        words = np.array([zipf_frequency(word, self.language[:2]) for word in words])
        mean = np.mean(words)
        median = np.median(words)
        MeanMedian = namedtuple("MeanMedian", "mean median")
        mm = MeanMedian(mean, median)
        return mm



