from random import sample, shuffle


class TestFromBook:
    number_of_additional_choices_in_question = 3

    class Question:

        def __int__(self, word, options, context):
            self.word = word
            self.options = options
            self.context = context
            self.context_without_word = context.replace(word, '(...)')

    def __init__(self, words_with_context=None):
        self.words_with_context = words_with_context

    @classmethod
    def get_options_line(cls, words, word):
        possible_answers = sample(words, cls.number_of_additional_choices_in_question)
        if word in possible_answers:
            possible_answers = cls.get_options_line(words, word)
        else:
            possible_answers.append(word)
        shuffle(possible_answers)
        return possible_answers

    @staticmethod
    def create_question(word, options, context, index):
        context_without_word = context.replace(word, '(...)')
        options_line = [f'{chr(index+65)}. {op:<20}' for index, op in enumerate(options, 0)]
        options_links = [f'https://dictionary.cambridge.org/dictionary/english/{op}\n' for op in options]

        question = f'{index}. {context_without_word}\n' \
                   f'{"".join(options_line)}\n' \
                   f'Correct answer: {word}\n' \
                   f'Full context: {context}\n' \
                   f'{"".join(options_links)}'

        return question

    def create_questions_list(self):
        questions_list = []
        words = sorted(self.words_with_context.keys())
        index = 1

        for word, contexts in self.words_with_context.items():
            for c in contexts:
                options = self.get_options_line(words, word)
                question = self.create_question(word, options, c, index)
                questions_list.append(question)
                index += 1

        return questions_list

