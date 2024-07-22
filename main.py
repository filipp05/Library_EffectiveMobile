from models import Library, Book


def main():
    lib = Library("./db.json") # объект библиотеки
    lib.load_db() # считываем текущее состояние БД

    while True:
        try:
            command = input("\n".join(["\nВведите номер необходимой команды:",
                            "1) Добавить книгу",
                            "2) Удалить книгу",
                            "3) Найти книгу",
                            "4) Посмотреть все книги",
                            "5) Изменить статус книги",
                            "6) Выйти\n\nВвод: "])) # дописали выход из программы для удобства пользователя
            if command == "1":
                title = input("Введите название книги: ")
                author = input("Введите автора книги: ")
                year = input("Введите год издания книги: ")
                lib.add_book(Book(title=title, author=author, year=year))
            elif command == "2":
                book_id = input("Введите ID книги для удаления: ")
                lib.delete_book(book_id)
            elif command == "3":
                param = input("Введите название параметра [id, title, author, year, status]: ")

                if param not in Book.params:
                    raise Exception("ВВЕДЕН НЕВЕРНЫЙ ПАРАМЕТР ПОИСКА")

                value = input("Введите значение параметра: ")

                book_set = lib.find_books(param, value)

                print("-" * 100, "\nНАЙДЕННЫЕ КНИГИ:\n")
                for book in book_set:
                    print(book)
                print("-" * 100)
            elif command == "4":
                lib.view_book_set()
            elif command == "5":
                book_id = input("Введите ID книги для изменения статуса: ")
                new_status = input(f"Введите новый статус книги [{', '.join(Library.status_set)}]: ")
                lib.change_book_status(book_id, new_status)
                print("\n", "-" * 100, "\n Статус изменен\n", "-" * 100, "\n")
            elif command == "6":
                exit()
            else:
                raise ValueError("Введите корректный номер команды")
        except Exception as e:
            print("\n", "!" * 100, "\n")
            print(" ", e)
            print("\n", "!" * 100, "\n")



if __name__ == "__main__":
    main()