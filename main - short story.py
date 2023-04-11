import os
from time import perf_counter
from collections import defaultdict
from AnalyzeText.AnalyzeText import AnalyzeText
from AnalyzeText.TestFromText import TestFromText


# 1. I choose a text to analyze
with open(r'AnalyzeText\data for tests\texts\Forgetting', mode='r', encoding='utf-8') as f:
    text = f.read()
an = AnalyzeText(text)

# 2. I pick a zipf range
an.c1_zipf_ceiling = 4
an.c1_zipf_floor = 1

# 3. I get words and contexts from the text
words_with_context = an.get_words_with_context()
for word, context in words_with_context.items():
    print(f'{word=}\n{context=}')

# 4. I save vocabulary
an.save_words(words_with_context)
an.save_words_and_context(words_with_context)

# 5. There I can make some changes to words list and if so, then I need to get contexts again
words = an.get_words_list_from_file()
words_with_context = an.get_words_with_context(words)
print(f'{words=}')

# 6. I create a test from the given vocabulary
test = TestFromText(words_with_context)
test.create_test_file_with_questions_answers_txt()









