import ebooklib
from ebooklib import epub
from bs4 import BeautifulSoup

# https://andrew-muller.medium.com/getting-text-from-epub-files-in-python-fbfe5df5c2da
# https://pypi.org/project/epub2txt/
# https://pypi.org/project/mobi/i


def get_contents_page(path):
    extension = path.split('.')[-1]
    if extension == 'epub':
        book = epub.read_epub(path)
        items = list(book.get_items_of_type(ebooklib.ITEM_DOCUMENT))
    return items


def get_text_from_item(item):
    soup = BeautifulSoup(item.get_body_content(), 'html.parser')
    text = [para.get_text() for para in soup.find_all('p')]
    text = ' '.join(text)
    return text


def show_content_page(path, show_some_text=False):
    contents_page = get_contents_page(fr"books\{path}")
    print("This is the contents page:")
    for index, item in enumerate(contents_page):
        print(f'{index}: {item.get_name()}')
        if show_some_text:
            text = get_text_from_item(item)
            print(text[:200], '\n')


def get_text_from_items(path, start, end):
    contents_page = get_contents_page(fr"books\{path}")
    text = ''
    for item in contents_page[start: end+1]:
        text += get_text_from_item(item)
    return text


