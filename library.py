import json
import pathlib
from json import JSONDecodeError


class Book:
    def __init__(self, book_id: int, title: str, author: str, year: int, status: bool = True) -> None:
        self.book_id = book_id
        self.title = title
        self.author = author
        self.year = year
        self.status = status

    def __str__(self):
        print_status = 'имеется в наличии' if self.status else 'книга выдана'
        return f'{self.book_id}: {self.author} - "{self.title}", {self.year} г., {print_status}'

class Library:

    def __init__(self, file):
        self.file = file
        self.books = self.create_books(file)

    def create_books(self, file) -> list:
        """Функция для создания списка книг. Возвращает список книг из json-файла, если он существует и доступен, либо возвращает пустой список"""

        # Проверям задан ли путь к файлу
        # Указывает ли путь на настоящий файл и является ли путь - файлом, а не папкой
        # Также проверяем доступ к файлу
        if file:
            path = pathlib.Path(file)
            if path.exists() and path.is_file():
                try:
                    with open(path, 'r', encoding='utf-8') as f:
                        data = sorted(json.load(f), key=lambda x: x['book_id'])
                        return [Book(**book) for book in data]
                except FileNotFoundError:
                    print('У вас нет доступа к этой библиотеке, поэтому мы создали вам новую!')
                    self.file = ''
                except JSONDecodeError:
                    print('Указанный файл не является библиотекой, поэтому мы создали вам новую библиотеку')
                    self.file = ''
        return []

    def check_book(self, pk: int):
        """Проверяет есть ли книга с переданным id в библиотеке и возвращает ее, если она есть"""
        for book in self.books:
            if book.book_id == pk:
                return book

    def id_generate(self) -> int:
        """Функция для генерации id"""

        if not self.books:
            return 1
        else:
            return self.books[-1].book_id + 1

    def book_add(self, title: str, author: str, year: int) -> None:
        """Функция добавления книги в библиотеку"""

        curr_id = self.id_generate()
        book = Book(curr_id, title, author, year)
        self.books.append(book)

    def book_delete(self, pk: int) -> bool:
        """Удаление книги из библиотеки"""

        book_for_del = self.check_book(pk)
        if book_for_del:
            self.books.remove(book_for_del)
            return True
        return False

    def find_book(self, find_option, option) -> list[Book]:
        """Функция находит и возвращает книги в зависимости от заданного поля поиска"""

        # Поиск книги по году
        if find_option == 3:
            return [book for book in self.books if book.year == option]

        # Поиск книги по автору
        elif find_option == 2:
            return [book for book in self.books if book.author.lower() == option]

        # Поиск книги по названию
        else:
            return [book for book in self.books if book.title.lower() == option]

    def show_all_books(self) -> list[Book]:
        """Возвращаем список всех книг"""

        return [book for book in self.books]

    def change_status(self, pk: int, new_status: bool) -> bool:
        """Изменение статуса книги по id"""

        book_for_change = self.check_book(pk)

        # Проверка текущего статуса книги. Если не совпадает с новым, то изменяем
        if book_for_change.status == new_status:
            return False
        else:
            book_for_change.status = new_status
            return True
