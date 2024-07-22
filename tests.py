import unittest
import os
import json

from models import Library, Book


class TestLibrary(unittest.TestCase):
    def setUp(self):
        self.test_filepath = 'test_db.json' # Создаем тестовый файл БД

        with open(self.test_filepath, 'w', encoding='utf-8') as file:
            json.dump([], file) # Физически создаем файл БД

        self.lib = Library(db_file_name=self.test_filepath)

    def test_add_book(self):
        self.lib.add_book(Book(title="A", author="A", year="1"))

        self.assertEqual(len(self.lib.get_book_set()), 1)
        self.assertEqual(self.lib.get_book_set()[0].get_attr("title"), "A")
        self.assertEqual(self.lib.get_book_set()[0].get_attr("author"), "A")
        self.assertEqual(self.lib.get_book_set()[0].get_attr("year"), "1")

    def test_delete_book(self):
        self.lib.add_book(Book(title="A", author="A", year="1"))

        book_id = self.lib.get_book_set()[0].get_attr("id")

        self.lib.delete_book(book_id)
        self.assertEqual(len(self.lib.get_book_set()), 0)

    def test_find_books(self):
        self.lib.add_book(Book(title="A", author="A", year="1"))
        self.lib.add_book(Book(title="A", author="B", year="1"))

        found_books_on_title = [book for book in self.lib.get_book_set() if book.get_attr("title") == "A"]
        found_books_on_author = [book for book in self.lib.get_book_set() if book.get_attr("author") == "B"]
        found_books_on_year = [book for book in self.lib.get_book_set() if book.get_attr("year") == "1"]

        self.assertEqual(len(found_books_on_title), 2)
        self.assertEqual(len(found_books_on_author), 1)
        self.assertEqual(len(found_books_on_year), 2)

    def test_set_status(self):
        self.lib.add_book(Book(title="A", author="A", year="1"))

        book_id = self.lib.get_book_set()[0].get_attr("id")

        self.lib.change_book_status(book_id, "выдана")
        self.assertEqual(self.lib.get_book_set()[0].get_attr("status"), "выдана")


    def tearDown(self):
        os.remove(self.test_filepath)

if __name__ == "__main__":
    unittest.main()
