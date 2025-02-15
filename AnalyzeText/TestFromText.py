import re
from random import sample, shuffle

from nltk import sent_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import nltk
from re import compile, sub
nltk.download("stopwords")


STOP_WORDS = stopwords.words("english")


class TestFromText:
    number_of_additional_choices_in_question = 3

    class QuestionWithAnswer:

        def __init__(self, word, options, context, index, source=''):
            self.index = index

            pattern = compile(word, re.IGNORECASE)
            self.context_without_word = pattern.sub("(...)", context)
            # self.context_without_word = context.replace(word, '(...)')
            self.options = options
            self.options_line = [f'{chr(index+65)}. {op:<20}' for index, op in enumerate(options, 0)]

            self.word = word
            self.context = context
            self.correct_choice = f'{chr(options.index(word) + 65)}'

            self.options_links = [f'https://dictionary.cambridge.org/dictionary/english/{op}\n' for op in options]

            self.source = source

        def __str__(self):
            return f'{self.index}. {self.context_without_word}\n' \
                   f'{"".join(self.options_line)}\n' \
                   f'{self.index}. Correct answer: {self.correct_choice}. {self.word}\n' \
                   f'Full context: {self.context}\n' \
                   f'{"".join(self.options_links)}\n'

        def anki_card(self):
            temp = [op.rstrip("\n") for op in self.options_links]
            temp = [f'<a href="{op}">{op}</a>' for op in temp]

            lemmatizer = WordNetLemmatizer()

            for el in self.options:
                #data = LDO.data_about_word(el)
                #print(data, '\n')

                print(f"{el=}; {lemmatizer.lemmatize(el)=}")

            return f"{self.context_without_word};{'<br>'.join(self.options_line)};" \
                   f"Correct answer: <b>{self.correct_choice}. {self.word}</b>;Full context: <br>{self.context};" \
                   f"{'<br>'.join(temp)}; {self.source}\n"

    def __init__(self, words_with_context=None, test_path='test', source=""):
        self.words_with_context = words_with_context
        self.test_path = test_path
        self.source = source

    @classmethod
    def get_options_line(cls, words, word):
        # Need to make so that possible answers and word are the same part of speech

        possible_answers = sample(words, cls.number_of_additional_choices_in_question)
        if word in possible_answers:
            possible_answers = cls.get_options_line(words, word)
        else:
            possible_answers.append(word)
        shuffle(possible_answers)
        return possible_answers

    def create_questions_with_answers_list(self):
        questions_with_answers_list = []
        words = sorted(self.words_with_context.keys())
        index = 1

        for word, contexts in self.words_with_context.items():
            for c in contexts:
                """
                half = int(len(c)/2)
                first_letter_index = c.find(word, half-len(word))

                word_list = word_tokenize(c)
                tagged = nltk.pos_tag(word_list)

                print(f"{word=}, \n{len(c)=} {c=}\n{half=}")
                print(f"{c[first_letter_index:first_letter_index+len(word)]}: this should be word")
                print(f"{tagged=}\n\n")
                """
                # Need to make so that possible answers and word are the same part of speech
                # words that I pass here and word should be the same part of speech

                options = self.get_options_line(words, word)
                qwa = self.QuestionWithAnswer(word, options, c, index, self.source)
                questions_with_answers_list.append(qwa)
                index += 1

        return questions_with_answers_list

    def create_test_file_with_questions_answers_txt(self):
        questions_with_answers_list = self.create_questions_with_answers_list()
        questions_with_answers_list = [str(qwa).splitlines() for qwa in questions_with_answers_list]

        with open(f'{self.test_path} questions.txt', 'w', encoding="utf-8") as file:
            for qwa in questions_with_answers_list:
                text = '\n'.join(qwa[:2])
                file.write(f'{text}\n\n')

        with open(f'{self.test_path} answers.txt', 'w', encoding="utf-8") as file:
            for qwa in questions_with_answers_list:
                text = '\n'.join(qwa[2:])
                file.write(f'{text}\n\n')

    def create_anki_cards(self):
        questions_with_answers_list = self.create_questions_with_answers_list()

        with open(f'{self.test_path} anki cards.txt', 'w', encoding="utf-8") as file:
            for qwa in questions_with_answers_list:
                # print(qwa.anki_card())
                file.write(qwa.anki_card())




