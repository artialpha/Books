import os
from time import perf_counter
from collections import defaultdict
from AnalyzeText.AnalyzeText import AnalyzeText


print(f'{os.listdir()}')
with open(r'AnalyzeText\data for tests\texts\Forgetting', mode='r', encoding='utf-8') as f:
    text = f.read()

an = AnalyzeText(text)
start = perf_counter()

###

words_with_context = an.get_words_with_context()

#######

for word, context in words_with_context.items():
    print(f'{word=}\n{context=}')
end = perf_counter()
print(end - start)









