import os
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import logging

from connection import Connection
from Drivers import SaveLoad, Search


class Book:
    def __init__(self, name, author, janr):
        self.name = name
        self.author = author
        self.janr = janr

    def __str__(self):
        return f"('{self.name}', '{self.author}', '{self.janr}')"


class Actions:
    def __init__(self, tkgui):
        self.tkgui = tkgui

    def add_clearing(self):
        """
        Функция очищает поля вкладки "Добавление книги"
        :return: None
        """
        self.tkgui.add_name.delete(0, END)
        self.tkgui.add_autor.delete(0, END)
        self.tkgui.add_janr.delete(0, END)

    def finder(self):
        """
        Ищет книги в БД по паттерну
        :return: result - список с книгами, найденными по паттерну
        """
        pattern = tkgui.find_usl.get()
        con = self.tkgui.getconnect()
        with con:
            cur = con.cursor()
            if self.tkgui.find_var.get() == 1:
                cur.execute(f"SELECT * FROM `books` WHERE name LIKE '%{pattern}%';")
            elif self.tkgui.find_var.get() == 2:
                cur.execute(f"SELECT * FROM `books` WHERE author LIKE '%{pattern}%';")
            else:
                cur.execute(f"SELECT * FROM `books` WHERE janr LIKE '%{pattern}%';")
            result = list(cur.fetchall())
        return result

    def find_book(self):
        """
        Функция сбрасывает результаты предыдущего поиска,
        запускает функцию finder(), получает список с результатами,
        запускает функцию вывода первого результата
        :return: result - список с результатами поиска
        """
        self.find_clearing()
        result = self.finder()
        self.result_print(result)
        return result

    def result_print(self, result, index=0):
        """
        Выводит книгу из списка результатов поиска по параметру index
        :param result: список результатов поиска
        :param index: индекс выводимой книги
        :return: порядковый номер книги в БД
        """
        self.tkgui.find_message.configure(text=f"Результат поиска: {index + 1 if len(result) != 0 else 0} из {len(result)}")
        if result:
            self.tkgui.find_name.configure(state="normal")
            self.tkgui.find_name.delete(0, END)
            self.tkgui.find_name.insert(0, result[index][1])
            self.tkgui.find_name.configure(state="disabled")
            self.tkgui.find_autor.configure(state="normal")
            self.tkgui.find_autor.delete(0, END)
            self.tkgui.find_autor.insert(0, result[index][2])
            self.tkgui.find_autor.configure(state="disabled")
            self.tkgui.find_janr.configure(state="normal")
            self.tkgui.find_janr.delete(0, END)
            self.tkgui.find_janr.insert(0, result[index][3])
            self.tkgui.find_janr.configure(state="disabled")
            self.tkgui.change_button.configure(state="normal")
            self.tkgui.del_button.configure(state="normal")
        if len(result) > 1:
            self.tkgui.find_next_button.configure(state="normal")
            self.tkgui.find_prev_button.configure(state="normal")
        return result[index][0]

    def next_result(self, result_list):
        """
        Функция выводит следующее значение из списка результатов поиска
        :param result_list: список с результатами поиска
        :return: порядковый номер книги в БД
        """
        current_pos = 0
        for i in result_list:
            if i[1] == self.tkgui.find_name.get() and i[2] == self.tkgui.find_autor.get() and i[3] == self.tkgui.find_janr.get():
                current_pos = result_list.index(i)
        if current_pos == len(result_list) - 1:
            return
        book_id = self.result_print(result_list, current_pos + 1)
        return book_id

    def prev_result(self, result_list):
        """
        Функция выводит предыдущее значение из списка результатов поиска
        :param result_list: список с результатами поиска
        :return: порядковый номер книги в БД
        """
        current_pos = 0
        for i in result_list:
            if i[1] == self.tkgui.find_name.get() and i[2] == self.tkgui.find_autor.get() and i[3] == self.tkgui.find_janr.get():
                current_pos = result_list.index(i)
        if current_pos == 0:
            return
        book_id = self.result_print(result_list, current_pos - 1)
        return book_id

    def find_clearing(self):
        """
        Функция очищает поля и сбрасывает состояние кнопок
        на вкладке "Поиск книги"
        :return: None
        """
        self.tkgui.find_name.configure(state="normal")
        self.tkgui.find_name.delete(0, END)
        self.tkgui.find_name.configure(state="disabled")
        self.tkgui.find_autor.configure(state="normal")
        self.tkgui.find_autor.delete(0, END)
        self.tkgui.find_autor.configure(state="disabled")
        self.tkgui.find_janr.configure(state="normal")
        self.tkgui.find_janr.delete(0, END)
        self.tkgui.find_janr.configure(state="disabled")
        self.tkgui.find_next_button.configure(state="disabled")
        self.tkgui.find_prev_button.configure(state="disabled")
        self.tkgui.find_message.configure(text="")
        self.tkgui.change_button.configure(state="disabled")
        self.tkgui.save_button.configure(state="disabled")
        self.tkgui.del_button.configure(state="disabled")

    def del_book(self, result_list):
        """
        Функция удаляет книгу, которая выведена в текущий момент в поисковых
        полях, из базы данных
        :param result_list: список с результатами поиска
        :return: None
        """
        del_book_id = 0
        for i in result_list:
            if i[1] == self.tkgui.find_name.get() and i[2] == self.tkgui.find_autor.get() and i[3] == self.tkgui.find_janr.get():
                del_book_id = i[0]
        con = self.tkgui.getconnect()
        with con:
            cur = con.cursor()
            cur.execute(f"DELETE FROM books WHERE idbooks = '{del_book_id}';")
            con.commit()
        messagebox.showinfo("Успех!", "Книга удалена из базы!")
        Actions.find_clearing()

    def save_book(self, book_id):
        """
        Функция сохраняет введенные изменения по книге в БД
        :param book_id: Порядковый номер книги в БД
        :return: None
        """
        con = self.tkgui.getconnect()
        with con:
            cur = con.cursor()
            cur.execute(f"UPDATE books \
            SET name = '{tkgui.find_name.get()}', \
            author = '{tkgui.find_autor.get()}', \
            janr = '{tkgui.find_janr.get()}' \
            WHERE (idbooks = '{book_id}');")
            con.commit()
            messagebox.showinfo("Успех!", "Изменения внесены в базу!")
            self.find_clearing()

    def change_book(self, book_id):
        """
        Функция кнопки "Внести изменения". Делает доступными соответствубщие кнопки и поля
        :param book_id: Порядковый номер книги в БД
        :return: book_id - Порядковый номер книги в БД
        """
        self.tkgui.change_button.configure(state="disabled")
        self.change_config()
        return book_id

    def change_config(self):
        """
        Делает доступными соответствубщие кнопки и поля
        :return: None
        """
        self.tkgui.find_name.configure(state="normal")
        self.tkgui.find_autor.configure(state="normal")
        self.tkgui.find_janr.configure(state="normal")
        self.tkgui.del_button.configure(state="disabled")
        self.tkgui.find_next_button.configure(state="disabled")
        self.tkgui.find_prev_button.configure(state="disabled")
        self.tkgui.save_button.configure(state="normal")

    def add_book(self):
        """
        Функция проверяет введенные пользователем данные и,
        в случае корректности, записывает их в базу данных
        :return: None
        """
        if self.tkgui.add_name.get() and self.tkgui.add_autor.get() and self.tkgui.add_janr.get():
            new_book = Book(self.tkgui.add_name.get(), self.tkgui.add_autor.get(), self.tkgui.add_janr.get())
            con = self.tkgui.getconnect()
            with con:
                cur = con.cursor()
                if Search.search_for_book((f'{new_book.name}', f'{new_book.author}', f'{new_book.janr}'), con):
                    cur.execute(f"INSERT INTO `books` (`name`, `author`, `janr`)\
                                VALUES ('{new_book.name}', '{new_book.author}', '{new_book.janr}');")
                    con.commit()
                    messagebox.showinfo("Успех!", "Книга успешно добавлена в базу!")
                    self.add_clearing()
                else:
                    messagebox.showinfo("Ошибка!", "Книга уже есть в базе!")
        else:
            messagebox.showinfo("Ошибка!", "Заполните все данные по книге!")


class TkGUI:
    def __init__(self):
        # ---------------- отрисовка основного окна--------------------
        self.root = Tk()
        self.root.title("Библиотека")
        self.root.geometry("600x250")
        # ---------------- добавление вкладок--------------------
        self.tab_control = ttk.Notebook(self.root)

        self.add_tab = ttk.Frame(self.tab_control)
        self.find_tab = ttk.Frame(self.tab_control)
        self.config_tab = ttk.Frame(self.tab_control)

        self.tab_control.add(self.add_tab, text="Добавить книгу")
        self.tab_control.add(self.find_tab, text="Поиск книг")
        self.tab_control.add(self.config_tab, text="Настройки")

        self.tab_control.pack(expand=1, fill="both")
        # ---------------- заполение вкладки "Добавить книгу"--------------------
        self.add_first_string = Label(self.add_tab, text="Введите данные добавляемой книги:")
        self.add_first_string.grid(column=0, row=0, padx=10, pady=10, columnspan=2, sticky=W)

        self.add_name_string = Label(self.add_tab, text="Наименование книги:")
        self.add_name_string.grid(column=0, row=1, padx=10, pady=0, sticky=W)

        self.add_name = Entry(self.add_tab, width="40")
        self.add_name.grid(column=1, row=1, padx=10, sticky=W)

        self.add_autor_string = Label(self.add_tab, text="Автор:")
        self.add_autor_string.grid(column=0, row=2, pady=10, sticky=W, padx=10)

        self.add_autor = Entry(self.add_tab, width="40")
        self.add_autor.grid(column=1, row=2, padx=10, sticky=W)

        self.add_janr_string = Label(self.add_tab, text="Жанр:")
        self.add_janr_string.grid(column=0, row=3, pady=0, padx=10, sticky=W)

        self.add_janr = Entry(self.add_tab, width="40")
        self.add_janr.grid(column=1, row=3, padx=0)

        self.add_button = Button(self.add_tab, text="ДОБАВИТЬ В БАЗУ", command=self.add_book)
        self.add_button.grid(column=1, row=4, pady=10)

        # ---------------- Заполение вкладки "Поиск книги"--------------------
        self.tab_find_book()

        # ---------------- Заполение вкладки "Настройки"--------------------
        # ---------------- Заполение данных "Настройки БД"--------------------
        self.config_DB_string = Label(self.config_tab, text="Настройки БД:")
        self.config_DB_string.grid(column=0, row=0, padx=10, pady=10, sticky=W)

        self.bd_choice_var = IntVar()
        self.bd_choice_var.set(2)
        self.bd_choice1 = ttk.Radiobutton(self.config_tab, text='MySQL', variable=self.bd_choice_var, value=1)
        self.bd_choice2 = ttk.Radiobutton(self.config_tab, text='SQLite3', variable=self.bd_choice_var, value=2)
        self.bd_choice1.grid(column=1, row=0)
        self.bd_choice2.grid(column=2, row=0)

        self.login_DB_string = Label(self.config_tab, text="Логин:")
        self.login_DB_string.grid(column=0, row=1, padx=10, pady=5, sticky=E)

        self.login_DB_entry = Entry(self.config_tab, width="10", state="normal", text="Ravenom")
        self.login_DB_entry.grid(column=1, row=1, padx=10, sticky=W)
        self.login_DB_entry.insert(0, "Ravenom")

        self.password_DB_string = Label(self.config_tab, text="Пароль:")
        self.password_DB_string.grid(column=2, row=1, padx=10, pady=5, sticky=W)

        self.password_DB_entry = Entry(self.config_tab, width="10", state="normal")
        self.password_DB_entry.grid(column=3, row=1, padx=10, sticky=W)
        self.password_DB_entry.insert(0, "Ravenom01")

        self.name_DB_string = Label(self.config_tab, text="Имя БД:")
        self.name_DB_string.grid(column=4, row=1, padx=10, pady=5, sticky=W)

        self.name_DB_entry = Entry(self.config_tab, width="10", state="normal")
        self.name_DB_entry.grid(column=5, row=1, padx=10, sticky=W)
        self.name_DB_entry.insert(0, "Bookshelf")

        self.save_conf_button = Button(self.config_tab, text="Проверить подключение", command=self.getconnect,
                                       state="normal")
        self.save_conf_button.grid(column=0, row=2)

        # ---------------- Заполение данных "Насторойки выгрузки"--------------------

        self.config_writer_string = Label(self.config_tab, text="Настройки выгрузки:")
        self.config_writer_string.grid(column=0, row=3, padx=10, pady=10, sticky=W)

        self.writer_var = IntVar()
        self.writer_var.set(1)
        self.save1 = ttk.Radiobutton(self.config_tab, text='в JSON', variable=self.writer_var, value=1)
        self.save2 = ttk.Radiobutton(self.config_tab, text='в CSV', variable=self.writer_var, value=2)
        self.save3 = ttk.Radiobutton(self.config_tab, text='в TXT', variable=self.writer_var, value=3)
        self.save1.grid(column=1, row=3)
        self.save2.grid(column=2, row=3)
        self.save3.grid(column=3, row=3)

        self.save_file_button = Button(self.config_tab, text="Выгрузить в файл", command=self.save_file, state="normal")
        self.save_file_button.grid(column=0, row=4)

        self.file_string = Label(self.config_tab, text="Имя файла:")
        self.file_string.grid(column=1, row=4, padx=10, pady=10, sticky=W)

        self.file_entry = Entry(self.config_tab, width="10", state="normal")
        self.file_entry.grid(column=2, row=4, padx=10, sticky=W)

        self.load_file_button = Button(self.config_tab, text="загрузить", command=self.load_file, state="normal")
        self.load_file_button.grid(column=3, row=4)

        self.result = None
        self.book_id = None
        self.save_driver = None
        self.data = None

        self.action = Actions(self)

    def tab_find_book(self):
        self.find_var = IntVar()
        self.find_var.set(1)

        self.rad1 = ttk.Radiobutton(self.find_tab, text='Искать по названию', variable=self.find_var, value=1)
        self.rad2 = ttk.Radiobutton(self.find_tab, text='Искать по автору', variable=self.find_var, value=2)
        self.rad3 = ttk.Radiobutton(self.find_tab, text='Искать по жанру', variable=self.find_var, value=3)
        self.rad1.grid(column=0, row=0)
        self.rad2.grid(column=1, row=0)
        self.rad3.grid(column=2, row=0)

        self.add_first_string = Label(self.find_tab, text="Введите условия поиска:")
        self.add_first_string.grid(column=0, row=1, padx=10, pady=10)

        self.find_usl = Entry(self.find_tab, width=40)
        self.find_usl.grid(column=1, row=1, padx=0, pady=0)

        self.find_message = Label(self.find_tab)
        self.find_message.grid(column=1, row=5, pady=0)

        self.find_name_string = Label(self.find_tab, text="Наименование книги:")
        self.find_name_string.grid(column=0, row=6, padx=10, pady=0, sticky=W)

        self.find_name = Entry(self.find_tab, width="40", state="disabled")
        self.find_name.grid(column=1, row=6, padx=10, sticky=W)

        self.find_autor_string = Label(self.find_tab, text="Автор:")
        self.find_autor_string.grid(column=0, row=7, pady=10, sticky=W, padx=10)

        self.find_autor = Entry(self.find_tab, width="40", state="disabled")
        self.find_autor.grid(column=1, row=7, padx=10, sticky=W)

        self.find_janr_string = Label(self.find_tab, text="Жанр:")
        self.find_janr_string.grid(column=0, row=8, pady=0, padx=10, sticky=W)

        self.find_janr = Entry(self.find_tab, width="40", state="disabled")
        self.find_janr.grid(column=1, row=8, padx=0)

        self.find_prev_button = Button(self.find_tab, text="<<<", command=self.prev_result, state="disabled")
        self.find_prev_button.grid(column=0, row=9, pady=10)

        self.find_button = Button(self.find_tab, text="Искать", command=self.search)
        self.find_button.grid(column=1, row=9, pady=10)

        self.find_next_button = Button(self.find_tab, text=">>>", command=self.next_result, state="disabled")
        self.find_next_button.grid(column=2, row=9, pady=10)

        self.change_button = Button(self.find_tab, text="    Изменить данные    ", command=self.change_book,
                                    state="disabled")
        self.change_button.grid(column=2, row=6)

        self.save_button = Button(self.find_tab, text="Сохранить изменения", command=self.save_book,
                                  state="disabled")
        self.save_button.grid(column=2, row=7)

        self.del_button = Button(self.find_tab, text="Удалить книгу из базы", command=self.delete_book,
                                 state="disabled")
        self.del_button.grid(column=2, row=8)

    def main(self):
        """
        Запускает основное окно (цикл)
        :return: None
        """
        self.root.mainloop()

    def add_book(self):
        self.action.add_book()

    def search(self):
        """
        Функция кнопки поиска
        :return: None
        """
        self.result = self.action.find_book()
        self.book_id = self.result[0][0]

    def next_result(self):
        """
        Функция кнопки следующий результат
        :return: None
        """
        self.book_id = self.action.next_result(self.result)

    def prev_result(self):
        """
        Функция кнопки предыдущий результат
        :return: None
        """
        self.book_id = self.action.prev_result(self.result)

    def delete_book(self):
        """
        Функция кнопки удалить книгу
        :return: None
        """
        self.action.del_book(self.result)

    def change_book(self):
        """
        Функция кнопки изменить книгу
        :return: None
        """
        self.action.change_book(self.book_id)

    def save_book(self):
        """
        Функция кнопки сохранить изменения
        :return: None
        """
        self.action.save_book(self.book_id)

    def save_file(self):
        """
        Функция кнопки выгрузить книги в файл
        :return: None
        """
        self.verify_path(self.file_entry.get())
        con = self.getconnect()
        if self.file_entry.get():
            driver = SaveLoad(self.file_entry.get(), tkgui.writer_var.get(), con)
            driver.write()
        else:
            logging.warning("Не выбрано имя файла!")

    def load_file(self):
        """
        Функция кнопки загрузить книги из файла
        :return: None
        """
        if self.file_entry.get():
            con = self.getconnect()
            driver = SaveLoad(self.file_entry.get(), tkgui.writer_var.get(), con)
            driver.read()
        else:
            logging.warning("Не выбрано имя файла!")

    @staticmethod
    def verify_path(path):
        """
        Функция проверяет наличие пути, если отсутствует - создает его
        :param path: путь, указанный пользователем
        :return: None
        """
        counter = len(path)
        while counter > 0:
            if path[-1] == "/" or path[-1] == "\\":
                path = path[:-1]
                break
            else:
                path = path[:-1]
                counter -= 1
        if len(path) and not os.path.exists(path):
            os.makedirs(path)

    def getconnect(self):
        return Connection.connect(self.bd_choice_var.get(), self.name_DB_entry.get(),
                                  self.login_DB_entry.get(), self.password_DB_entry.get())


if __name__ == '__main__':
    tkgui = TkGUI()
    tkgui.main()
