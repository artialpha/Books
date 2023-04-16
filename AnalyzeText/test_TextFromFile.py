from unittest import TestCase
from os import listdir, chdir
from TextFromFile import get_text_from_file


class Test(TestCase):

    def setUp(self) -> None:
        chdir('..')

    def test_get_text_from_file(self):
        print(listdir())
        get_text_from_file(r"books\01 Harry Potter and the Sorcerer's Stone - J.K. Rowling.epub")
