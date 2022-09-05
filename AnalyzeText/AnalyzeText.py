import string

import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
nltk.download("stopwords")


class AnalyzeText:

    stop_words = set(stopwords.words("english"))

    def __init__(self, text):
        self.text = text

    #Get rid of stop words and punctuation marks
    def get_words(self):
        words = word_tokenize(self.text)
        filtered_list = [word for word in words if word.casefold()
                         not in self.stop_words and word not in string.punctuation]
        return filtered_list
