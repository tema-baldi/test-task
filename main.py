import json
import os
import string
from datetime import datetime


from library import Library

# Все сообщения программы собраны в кучу, что бы в случае изменения какого-либо из них
# не пришлось искать однотипные сообщения по всему проекту и изменить их
messages = {
    'dont_name_book': 'Книга не может быть без названия. Пожалуйста, напишите корректное название!',
    'dont_have_author': 'У книги должен быть автор. Пожалуйста, заполните это поле! В случае, если автор книги неизвестен, то напишите в поле "н/д".',
    'instruction_for_add': 'Что бы добавить книгу в библиотеку следуйте следующей инструкции:',
    'check_add': 'Завершите процесс добавления: "1" - добавить книгу, "2" - изменить данные, "3" - отменить добавление',
    'add_success': '*** Книга успешно добавлена в библиотеку! ***',
    'none_instruction': 'Введенное значение не соответствует инструкции. Пожалуйста, повторите попытку!',
    'check_int': 'Введенное значение должно быть положительным числом! Пожалуйста, повторите попытку!',
    'year': 'Введите год написания книги',
    'year_zero': 'Год не может быть нулевым! Пожалуйста, измените данные!',
    'year_big': 'Год написания книги не может быть больше текущего года! Пожалуйста, измените данные!',
    'id_for_del': 'Введите id книги, которую хотите удалить (для отмены операции, введите - "0")',
    'id_not_found': 'Книги с таким id нет в данной библиотеке. Попробуйте поиск заново!',
    'id_change': 'Введите id книги, чей статус хотите изменить (для отмены операции, введите - "0")',
    'check_del': 'Вы уверены, что хотите удалить книгу с id = {}? \n'
                      f'Если уверены то введите - "1", для отмены операции удаления - "0"',
    'del_success': '*** Книга успешно удалена! ***',
    'del_close': 'Операция удаления отменена!',
    'find_option': 'По какому параметру вы хотите искать книгу \n'
                   '1 - Название книги, 2 - Автор книги, 3 - Год написания книги, 0 - Выходит из процесса поиска',
    'find_success': '*** В данной библиотеке не найдена ни одна книга с заданными параметрами для поиска ***',
    'not_books': '*** В данной библиотеке пока что нет книг ***',
    'new_status': 'Выберите новый статус книги \n'
                  '"1" - книга в наличии, "2" - книга выдана, "3" - для перехода назад к выбору id книги, "0" - для отмены '
                                   'операции изменения статуса',
    'status_change_success': '*** Статус книги успешно изменен ***',
    'status_not_change': '*** Статус книги и так соответствует тому, на который вы хотели его сменить ***',
    'name_file': 'Придумайте название для файла вашей библиотеки: ',
    'exit': '*** Спасибо, что посетили нашу библиотеку! До скорых встреч! ***',
    'hello': 'Добро пожаловать в нашу электронную библиотеку!',
    'new_or_old_lib': 'Вы хотите открыть существующую библиотеку или создать новую ("0" - Создать новую, "1" - Отркыть существующую)?',
    'new_lib': 'К сожалению, существующих библиотек пока нет, поэтому мы создали вам новую!',
    'choice_lib': 'Выберите из списка библиотеку, которая вас интересует: {}',
    'save_file': '*** Файл успешно сохранен! Путь к нему относительно текущей директории - {} ***',
    'create_file_name_error': 'Имя файла не должно содеражть специальных символов "!\"#$%&\'()*+,./:;<=>?@[\\]^_`{|}~"',
    'also_have_this_name': 'Файл с таким именем уже существует в электронной библиотеке! Пожалуйста, придумайте другое название!',
    'empty_name': 'Название файла не может быть пустое! Пожалуйста, придумайте корректное название',
}

def create_file_name() -> str:
    """Функция формирует и возвращает имя json-файла"""

    # Валидация введенного пользователем названия файла
    # Убираем все лишние пробелы до и после названия
    # Если между словами стоят пробелы, меняем их на тире
    # Не допускаем наличия в названии файла спец. символо, кроме тире
    # Проверяем есть ли в папке уже файлы с таким именем, что бы избежать перезаписи какой-либо библиотеки
    # Отлавливаем ошибку отсутствия директории (lib), в которой должны храниться файлы-библиотеки. Создаем новую папку в случае ошибки
    while True:
        name = input(messages['name_file']).strip().lower()
        name = '-'.join(name.split())
        if not name:
            print(messages['empty_name'])
            continue
        for ch in name:
            if ch in string.punctuation.replace('-', ''):
                print(messages['create_file_name_error'])
                break
        else:
            try:
                if name + '.json' in os.listdir('lib/'):
                    print(messages['also_have_this_name'])
                    continue
                else:
                    break
            except FileNotFoundError:
                os.mkdir('lib')
                break
    file = 'lib/' + name + '.json'
    return file

def input_title_or_author(option: int) -> str:
    """Функция для ввода и валидации введенных данных названия книги и автора"""

    options = {1: 'название', 2: 'автора'}
    error_message = {
        1: messages['dont_name_book'],
        2: messages['dont_have_author']
    }

    # Ввод значения пользователем с удалением пробелов до и после введенных данных
    result = input(f'Введите {options[option]} книги: ').strip()

    # Проверяем если пользователь оставил пустую строку
    if not result:
        print(error_message[option])
        result = input_title_or_author(option)

    # Убираем лишние пробелы между словами (если они есть) и возвращаем результат
    return ' '.join(result.split())

def check_int(text: str) -> int:
    """Функция проверят введенное значение пользователем, что бы оно было неотрицательным"""

    try:
        num = int(input(f'{text}: '))
        if num < 0:
            print(messages['check_int'])
            num = check_int(text)
    except ValueError:
        print(messages['check_int'])
        num = check_int(text)
    return num

def check_book_in_lib_for_id(lib: Library, pk: int) -> bool:
    """Проверка наличия книги в библиотеке с заданным id"""

    if not lib.check_book(pk):
        return False
    return True

def add_book_in_lib(lib: Library) -> None:
    """Функция добавления книги в заданную библиотеку"""

    print(messages['instruction_for_add'])

    # Ввод пользователем название книги, автора и год
    title = input_title_or_author(1)
    author = input_title_or_author(2)
    year = check_int(messages['year'])

    # Проверка валидности введенного года (1 <= year <= текущий год)
    while True:
        if year == 0:
            print(messages['year_zero'])
            year = check_int(messages['year'])
        elif year > datetime.now().year:
            print(messages['year_big'])
            year = check_int(messages['year'])
        else:
            break

    # Отмена операции / Изменение данных книги / Добавление книги в заданную библиотеку
    while True:
        check = check_int(messages['check_add'])
        if check == 3:
            return
        elif check == 2:
            add_book_in_lib(lib)
            return
        elif check == 1:
            lib.book_add(title, author, year)
            print(messages['add_success'])
            return
        print(messages['none_instruction'])

def delete_book_from_lib(lib: Library) -> None:
    """Функция удаления книги из библиотеки по id"""

    # Проверка наличия книг в библиотеке
    if not lib.books:
        print(messages['not_books'])
        return

    # Ввод id пользователем
    book_id = check_int(messages['id_for_del'])
    if book_id == 0:
        return

    # Проверка наличия книги с заданным id
    if not check_book_in_lib_for_id(lib, book_id):
        print(messages['id_not_found'])
        delete_book_from_lib(lib)
        return

    # Удаление книги
    check = check_int(messages['check_del'].format(book_id))
    while check > 2:
        print(messages['none_instruction'])
        check = check_int(messages['check_del'].format(book_id))
    if check == 1:
        lib.book_delete(book_id)
        print(messages['del_success'])
    else:
        print(messages['del_close'])

def find_book_in_lib(lib: Library) -> None:
    """Функция находит книгу в заданной библиотеке"""

    # Проверка наличия книг в библиотеке
    if not lib.books:
        print(messages['not_books'])
        return

    # Пользователь выбирает поле, по которому хочет произвести поиск
    find_option = check_int(messages['find_option'])
    if find_option not in {0, 1, 2, 3}:
        print(messages['none_instruction'])
        find_book_in_lib(lib)
        return
    if find_option == 0:
        return

    # Пользователь указывает год для поиска книги, либо автора / название книги
    if find_option == 3:
        option = check_int(messages['year'])
        # Валидация указанного года (1 <= option <= текущий год)
        while True:
            if option == 0:
                print(messages['year_zero'])
                check_int(messages['year'])
            if option > datetime.now().year:
                print(messages['year_big'])
                check_int(messages['year'])
            break
    else:
        option = input_title_or_author(find_option).lower()

    # Вывод всех найденных книг в библиотеке
    find_result = lib.find_book(find_option, option)
    if find_result:
        [print(f'{i+1}) {book}') for i, book in enumerate(find_result)]
    else:
        print(messages['find_success'])

def show_all_books_in_lib(lib: Library) -> None:
    """Функция выводит все найденные книги в заданной библиотеке"""

    find_result = lib.show_all_books()
    if find_result:
        [print(f'{i+ 1}) {book}') for i, book in enumerate(find_result)]
    else:
        print(messages['not_books'])

def change_status_book_in_lib(lib: Library) -> None:
    """Функция изменения статуса книги"""

    # Проверка наличия книг в библиотеке
    if not lib.books:
        print(messages['not_books'])
        return

    # Пользователем указывает id книги для изменения статуса
    book_id = check_int(messages['id_change'])
    if book_id == 0:
        return

    # Проверка наличия книги с заданным id
    if not check_book_in_lib_for_id(lib, book_id):
        print(messages['id_not_found'])
        change_status_book_in_lib(lib)
        return

    # Пользователь выбирает новый статус книги
    while True:
        new_status = check_int(messages['new_status'])
        if new_status == 0:
            return
        if new_status == 3:
            change_status_book_in_lib(lib)
            return
        if new_status == 1 or new_status == 2:
            break
        print(messages['none_instruction'])

    # Изменение статуса
    new_status = True if new_status == 1 else False
    if lib.change_status(book_id, new_status):
        print(messages['status_change_success'])
    else:
        print(messages['status_not_change'])

def write_to_json(lib: Library) -> None:
    """Функция записывает всю библиотеку в JSON-файл c последующим закрытием программы"""

    # Проверяем открывалась ли существующая библиотека, либо создавалась новая
    # Если вносились изменения в уже существующую библиотеку, то обновляем ее
    # В противном случае создаем новый файл
    if lib.file:
        file = lib.file
    else:
        file = create_file_name()

    # Формируем данные для вывода в JSON-файл
    books = lib.books
    data = []
    for book in books:
        data.append({
            'book_id': book.book_id,
            'title': book.title,
            'author': book.author,
            'year': book.year,
            'status': book.status
        })

    # Запись сформированных данных в файл
    with open(file, 'w+') as f:
        json.dump(data, f)
    print(messages['save_file'].format(file))

    # Закрытие программы
    close_program(lib)

def close_program(lib: Library) -> None:
    """Функция для закрытия программы"""

    print(messages['exit'])
    exit()

def main() -> None:
    """Главная функция программы"""

    print(messages['hello'])

    # Возможные операции
    operations = {
        1: (add_book_in_lib, '1. Добавить книгу в библиотеку'),
        2: (delete_book_from_lib, '2. Удалить книгу из библиотеки'),
        3: (find_book_in_lib, '3. Найти книгу в библиотеке'),
        4: (show_all_books_in_lib, '4. Показать все книги в библиотеке'),
        5: (change_status_book_in_lib, '5. Изменить статус книги'),
        6: (write_to_json, '6. Закрыть программу с сохранением внесенных изменений'),
        7: (close_program, '7. Закрыть программу без сохранения изменений')
    }

    # Пользователь выбирает загрузить библиотеку, которая есть в наличии, либо создать новую
    while True:
        start = check_int(messages['new_or_old_lib'])
        if start == 1 or start == 0:
            break
        print(messages['none_instruction'])

    file = ''
    if start == 1:
        # Формируем список файлов (библиотек) для выбора пользователем
        # В случае, если отсутствует директория (lib) в проекте, то отлавливаем ошибку и создаем пустую папку, где будут храниться файлы
        cnt = 1
        libs = []
        try:
            for path in os.listdir('lib/'):
                if path.endswith('.json'):
                    path = path.rstrip('.json')
                    libs.append(f'{cnt}) {path}')
                    cnt += 1
        except FileNotFoundError:
            os.mkdir('lib')
        if not libs:
            print(messages['new_lib'])
        else:
            # Пользователем выбирает из списка библиотеку, которую хочет открыть
            choice = check_int(messages['choice_lib'].format(libs))

            # Валидация введенных данных пользователем
            while 0 >= choice or choice > len(libs):
                print(messages['none_instruction'])
                choice = check_int(messages['choice_lib'].format(libs))

            # Формирование пути файла для передачи в класс Library
            name = libs[choice - 1].split()[1]
            file = 'lib/' + name + '.json'
    lib = Library(file)

    # Работы программы
    while True:
        try:
            ans = int(input('\n'
                            f'{operations[1][1]} \n'
                            f'{operations[2][1]} \n'
                            f'{operations[3][1]} \n'
                            f'{operations[4][1]} \n'
                            f'{operations[5][1]} \n'
                            f'{operations[6][1]} \n'
                            f'{operations[7][1]} \n'
                            f'Выберите операцию из вышеперечисленного списка (1 - 7): '))
            print()
            if ans not in operations:
                print(messages['none_instruction'])
            else:
                operations[ans][0](lib)
        except ValueError:
            print(messages['none_instruction'])


if __name__ == '__main__':
    main()
