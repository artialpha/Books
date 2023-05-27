# Books
Goal of the project
Create a tool which will help me to learn vocabulary from English books. 
From time to time I read a book which was written in English to brush up on my language skills. It comes as no surprise that I come across words that I don’t know and that I’d like to learn them. Ofcource, I could simply write down unknown vocabulary and later add it to a program which I use to learn English (anki) but I found it too time consuming and I figure out that it would be a good idea to automate this task. 

Short description
1. I use the wordfreq python library to get the use frequency (how often they apprear in texts for a given language) of words from a text.
2. I get two lists with words at C1 level to calculate the average use frequency of those words – I want to narrow down the number of words I get from a text.
3. I get the context for every word that I have obtained from a piece of text. I can get a lemma (the canonical form of a word) as well if I want. 
4. I can create a test which will help me learn the vocabulary from the text.
5. I save a list of words - later I can choose which words I'd like to learn and I can add them to a program I use to learn English (namely Anki)
