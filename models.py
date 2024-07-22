from json import dump, load
from uuid import uuid4


class Book:
    """Класс книги"""
    params = ["id", "title", "author", "year", "status"]

    def __init__(self, id=None, title="Без имени", author="Неизвестен", year="Неизвестен", status="в наличии"):
        """
        Конструктор книги
        id — идентификатор книги (по умолч. None)
        title — заголовок книги (по умолч. "Без имени"),
        author — автор книги (по умолч. "Неизвестен"),
        year — год написания книги (по умолч. "Неизвестен")
        status — статус книги (по умолч. "в наличии")
        """
        if year != "Неизвестен" and not year.isdigit():
            raise ValueError("Некорректно введен год книги")

        self.__id = str(uuid4()) if not id else id
        self.__title = title
        self.__author = author
        self.__year = year
        self.__status = status

    def __str__(self):
        """
        Метод возвращает строковое представление все параметров книги
        """
        return "\n".join([f"Книга {self.__id}:", f"\ttitle: {self.__title}", f"\tauthor: {self.__author}",
                          f"\tyear: {self.__year}", f"\tstatus: {self.__status}\n"])

    def get_attr(self, param) -> str:
        """
        функция возврата значения параметра param данной книги
        param — строковое представление параметра из params
        """
        # return getattr(self, f"__{param}")

        if param == "id":
            return self.__id
        elif param == "title":
            return self.__title
        elif param == "author":
            return self.__author
        elif param == "year":
            return self.__year
        elif param == "status":
            return self.__status
        else:
            raise ValueError("ВВЕДЕН НЕВЕРНЫЙ ПАРАМЕТР КНИГИ")

    def get_dict(self) -> dict:
        """
        Возвращает словарь параметров книги
        """
        return {
            "id": self.__id,
            "title": self.__title,
            "author": self.__author,
            "year": self.__year,
            "status": self.__status
        }

    def set_status(self, new_status: str) -> None:
        """
         Устанавливает новый статус книге
         new_status - представление нового статуса
        """
        self.__status = new_status

    @staticmethod
    def get_book_from_json(json_obj):
        """
        Функция перевода json книги в объект класса Book
        json_obj — представление книги, которое необходимо преобразовать
        """
        return Book(json_obj["id"], json_obj["title"], json_obj["author"], json_obj["year"], json_obj["status"])


class Library:
    """
    Класс библиотеки
    """
    status_set = ["в наличии", "выдана"] # список допустимых статусов книги [статическое свойство]

    def __init__(self, db_file_name: str):
        """
        Конструктор библиотеки
        db_file_name — строковое представление пути в файлу БД
        """
        self.__db_file_name = db_file_name
        self.__book_set = []

    def get_book_set(self):
        return self.__book_set

    def load_db(self) -> None:
        """
        Функция считывания вайла БД
        """
        try:
            with open(self.__db_file_name, 'r', encoding='utf-8') as file:
                self.__book_set = [Book.get_book_from_json(book) for book in load(file)]
        except FileNotFoundError:
            raise Exception("НЕВЕРНЫЙ ПУТЬ К ФАЙЛУ")


    def update_db(self) -> None:
        """
        Функция обновления БД
        """
        with open(self.__db_file_name, 'w', encoding='utf-8') as file:
            dump([book.get_dict() for book in self.__book_set], file, ensure_ascii=False, indent=4)

    def add_book(self, book: Book) -> None:
        """
        Функция добавления книги
        book — объект класса Book
        """
        self.__book_set.append(book)
        self.update_db()

    def delete_book(self, book_id: str) -> None:
        """
        Функция удаления книги из библиотеки
        book_id — идентификатор книги
        """
        check = -1 # заведомо несуществующее значение индекса удаляемой книги

        for i in range(len(self.__book_set)):
            if self.__book_set[i].get_attr("id") == book_id:
                check = i
                break

        if check == -1: # попадаем сюда, если книги не нашлось
            raise Exception("НЕВЕРНО ВВЕДЕН ID КНИГИ")

        self.__book_set.pop(check)
        self.update_db()

        print(" ", "-" * 100, "\n КНИГА УДАЛЕНА\n ", "-" * 100)

    def find_books(self, param: str, value: str) -> list:
        """
        Функция возвращает список книг, у которых параметр param равен value
        param — текстовое представление параметра поиска
        value — значения для параметра
        """
        if param.lower() not in Book.params: # приводим к нижнему регистру, чтобы учесть ошибки пользователя при вводе
            raise ValueError("ВВЕДЕН НЕСУЩЕСТВУЮЩИЙ ПАРАМЕТР")

        relevant_books = [book for book in self.__book_set if value.lower() == book.get_attr(param)]

        if not relevant_books:
            raise ValueError("НЕВЕРНО ВВЕДЕН ИДЕНТИФИКАТОР КНИГИ")

        return relevant_books

    def view_book_set(self) -> None:
        """
        Функция вывода всех книг в библиотеке
        """
        if self.__book_set:
            print("-" * 100)
            print("БИБЛИОТЕКА:\n")
            for book in self.__book_set:
                print(book)
            print("-" * 100)
        else:
            raise Exception("Библиотека пуста")

    def change_book_status(self, id: str, new_status: str):
        """
        Функция изменения статуса книги
        """
        if new_status not in Library.status_set:
            raise ValueError(f"Некорректный статус! Выберите из [{', '.join(self.status_set)}]")
        try:
            self.find_books("id", id)[0].set_status(new_status)
        except:
            raise ValueError("НЕВЕРНО ВВЕДЕН ИДЕНТИФИКАТОР КНИГИ")




