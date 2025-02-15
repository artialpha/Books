import requests
import json
from bs4 import BeautifulSoup
from collections import namedtuple


class LDO:
    ldo = "https://www.ldoceonline.com/dictionary/"
    Meaning = namedtuple("Meaning", "definition examples")

    @classmethod
    def get_content(cls, word):
        url = f'{cls.ldo}{word}'

        headers = requests.utils.default_headers()
        headers.update({'User-Agent': 'My User Agent 1.0', })
        response = requests.get(url, headers={
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36"
        })

        soup = BeautifulSoup(response.content, 'html.parser')

        return soup

    @classmethod
    def get_entries(cls, soup):
        return soup.find_all("span", class_="dictentry")

    @classmethod
    def get_data_from_entry(cls, entry):
        senses = entry.find_all("span", class_="Sense")
        result = []

        for s in senses:
            if definition := s.find("span", class_="DEF"):
                examples = s.find_all("span", class_="EXAMPLE")
                examples = [ex.text for ex in examples]
                examples = [ex.lstrip('\n\xa0') for ex in examples]

                m = cls.Meaning(definition.text.lstrip(' '), examples)
                result.append(m)

        return result

    @classmethod
    def entry_into_string(cls, entry):
        dwe = cls.get_data_from_entry(entry)
        result = ""

        for one in dwe:
            result += one.definition + '\n'

            for ex in one.examples:
                result += ex + '\n'

            result += '+\n'

        return result[:-3]

    @classmethod
    def data_about_word(cls, word):
        word_content = LDO.get_content(word)
        word_entries = LDO.get_entries(word_content)

        pron = None
        if (pron := word_content.find("span", class_="PRON")) is None:
            if (pron := word_content.find("span", class_="PronCodes")) is None:
                pron = word_content.find("span", class_="PRON")

        if not pron:
            pron = " "
        else:
            pron = pron.text

        word = word.replace('-', ' ')

        text = f'{word} /{pron}/\n'

        for e in word_entries:
            res = LDO.entry_into_string(e)
            text += f'{res}\n++\n'

        return text[:-4]
