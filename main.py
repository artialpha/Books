from AnalyzeText.TextFromFile import get_contents_page, show_content_page, get_text_from_items
from bs4 import BeautifulSoup
from AnalyzeText.AnalyzeText import AnalyzeText
from AnalyzeText.TestFromText import TestFromText

if __name__ == '__main__':
    leave_program = False

    while not leave_program:
        print("Hello, I see you are an english learner. Would you like to learn some vocabulary with me?\n"
              "Give me the name of a file that is inside 'books' folder and that you want to work with:")
        #path = input()
        # path = "01 Harry Potter and the Sorcerer's Stone - J.K. Rowling.epub"
        path = "Thomas Ligotti, Ray Brassier - The Conspiracy against the Human Race_ A Contrivance of Horror-Hippocampus Press (2011).epub"
        print(f"\nSo we will work with a file: {path}\n")
        print('Options:\n'
              '1. I want to see a contents page. \n'
              '2. I want to see a contents page and some text from it.\n'
              '3. Get text from contents and create files with two lists: words and words + contexts: '
              'x. Quit\n')
        #option = input()
        option = '3'

        if option == '1':
            show_content_page(path)
        elif option == '2':
            show_content_page(path, show_some_text=True)
        elif option == '3':
            print('type the range you want to get the text from (eg. 1-2 OR 1-15)')
            #rng = input()
            rng = '10-10'
            start, end = rng.split('-')
            text = get_text_from_items(path, int(start), int(end))
            text = text.replace('\n', ' ').replace('\r', '')
            #print(text)

            # text to analyze
            an = AnalyzeText(text)
            print(an.get_c1_words_from_text())

            # 2. I pick a zipf range
            an.c1_zipf_ceiling = 4
            an.c1_zipf_floor = 0

            # 3. I get words and contexts from the text
            words_with_context = an.get_words_with_context()
            #print(f"{words_with_context=}")

            # 4. I save vocabulary
            an.save_words(words_with_context, save_lemmas=True)
            an.save_words_and_context(words_with_context)

            # 5. There I can make some changes to words list and if so, then I need to get contexts again
            # words = an.get_words_list_from_file()
            # words_with_context = an.get_words_with_context(words)
            # print(f"{words_with_context=}")

            # 6. I create a test from the given vocabulary
            test = TestFromText(words_with_context, path, path)
            test.create_test_file_with_questions_answers_txt()
            # print("I created a test?")

            # 7. I create anki cards from the given vocabulary
            test.create_anki_cards()

        leave_program = True



