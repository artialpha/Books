from AnalyzeText.AnalyzeText import AnalyzeText
from time import perf_counter

with open(r'short stories\Bad blood.TXT', mode='r', encoding='utf-8') as f:
    text = f.read()

an = AnalyzeText(text)
start = perf_counter()
words_with_frequency = an.get_c1_words_from_text()
words = [word for (word, freq) in words_with_frequency]
print(f'words: {words_with_frequency}\nlen: {len(words)}')
sentences = an.get_sentences_for_filtered_words()
print(f'sentences: {sentences}\nlen: {len(sentences)}')
end = perf_counter()
print(end - start)









