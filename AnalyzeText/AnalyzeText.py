import string
from wordfreq import zipf_frequency  # https://pypi.org/project/wordfreq/
import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
nltk.download("stopwords")


class AnalyzeText:

    def __init__(self, text, language='english'):
        self.text = text
        self.filtered_list = None
        self.frequency_list = None
        self.language = language
        self.stop_words = set(stopwords.words(language))

    #Get rid of stop words and punctuation marks
    def get_words(self):
        words = word_tokenize(self.text)
        print(f'tokenized {words}')
        filtered_list = [x for word in words if (x := word.casefold())
                         not in self.stop_words and word not in string.punctuation]
        self.filtered_list = filtered_list
        return filtered_list

    def get_word_frequency(self):
        self.frequency_list = [zipf_frequency(word, self.language[:2]) for word in self.filtered_list]
        return self.frequency_list
