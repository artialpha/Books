from random import sample, shuffle


class TestFromBook:
    number_of_additional_choices_in_question = 3

    class QuestionWithAnswer:

        def __init__(self, word, options, context, index):
            self.index = index
            self.context_without_word = context.replace(word, '(...)')
            self.options_line = [f'{chr(index+65)}. {op:<20}' for index, op in enumerate(options, 0)]

            self.word = word
            self.context = context
            self.correct_choice = f'{chr(options.index(word) + 65)}'

            self.options_links = [f'https://dictionary.cambridge.org/dictionary/english/{op}\n' for op in options]

        def __str__(self):
            return f'{self.index}. {self.context_without_word}\n' \
                   f'{"".join(self.options_line)}\n' \
                   f'{self.index}. Correct answer: {self.correct_choice}. {self.word}\n' \
                   f'Full context: {self.context}\n' \
                   f'{"".join(self.options_links)}\n'

    def __init__(self, words_with_context=None, test_path='test'):
        self.words_with_context = words_with_context
        self.test_path = test_path

    @classmethod
    def get_options_line(cls, words, word):
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
                options = self.get_options_line(words, word)
                qwa = self.QuestionWithAnswer(word, options, c, index)
                questions_with_answers_list.append(qwa)
                index += 1

        return questions_with_answers_list

    def create_test_file_with_questions_answers_txt(self):
        questions_with_answers_list = self.create_questions_with_answers_list()
        questions_with_answers_list = [str(qwa).splitlines() for qwa in questions_with_answers_list]

        with open(f'{self.test_path} questions.txt', 'w') as file:
            for qwa in questions_with_answers_list:
                text = '\n'.join(qwa[:2])
                file.write(f'{text}\n\n')

        with open(f'{self.test_path} answers.txt', 'w') as file:
            for qwa in questions_with_answers_list:
                text = '\n'.join(qwa[2:])
                file.write(f'{text}\n\n')




