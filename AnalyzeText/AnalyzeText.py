from string import punctuation
import nltk
import numpy as np
from wordfreq import zipf_frequency  # https://pypi.org/project/wordfreq/
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from PyPDF2 import PdfReader
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

    @staticmethod
    def get_medium_c1_frequency():
        reader = PdfReader("c1.pdf")
        for page in reader.pages:
            for line in page.extract_text().splitlines():
                if line.count("/") == 2:
                    line = line.split()
                    if len(line) == 1 or not line[1].isascii():
                        print(line)

        # it must be one word + IPA or only one word (like in alternate)
        #['affluent', '/ˈæf.lu.ənt/'] False
        #['affluent', 'families/nations/neighbourhoods'] True
        

        
        
        #after learner example
        """
        for page in reader.pages:
            text += page.extract_text() + "\n"
        print(text)
        """
