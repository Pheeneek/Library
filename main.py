import pymysql
import os
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import json
import csv


class Book:
    def __init__(self, name, author, janr):
        self.name = name
        self.author = author
        self.janr = janr


class Connection:
    @staticmethod
    def connect():
        try:
            con = pymysql.connect('localhost', f'{tkgui.login_DB_entry.get()}',
                                  f'{tkgui.password_DB_entry.get()}', f'{tkgui.name_DB_entry.get()}')
            print(f"Успешное подключение к базе данных '{tkgui.name_DB_entry.get()}'!")
            return con
        except pymysql.err.OperationalError:
            print("Не удалось подключиться к базе данных!")


class JsonDriverBuilder:
    def __init__(self, filename):
        filename = filename.strip()
        if not str(filename).endswith(".json"):
            filename = filename + ".json"
        self.filename = filename

    def write(self, data):
        with open(self.filename, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False)

    def read(self):
        with open(self.filename, "r", encoding="utf-8") as f:
            data = json.load(f)
            con = Connection.connect()
            with con:
                cur = con.cursor()
                for i in data:
                    new_book = Book(i[1], i[2], i[3])
                    cur.execute(f"INSERT INTO `bookshelf`.`books` (`name`, `author`, `janr`)\
                                    VALUES ('{new_book.name}', '{new_book.author}', '{new_book.janr}');")
                con.commit()


class CSVDriverBuilder:
    def __init__(self, filename):
        filename = filename.strip()
        if not filename.endswith(".csv"):
            filename = filename + ".scv"
        self.filename = filename

    def write(self, data):
        with open(self.filename, "w", encoding="utf-8") as f:
            writer = csv.writer(f)
            for i in data:
                writer.writerow(i)

    def read(self):
        with open(self.filename, "r", encoding="utf-8") as f:
            file_reader = csv.reader(f, delimiter=",")
            con = Connection.connect()
            with con:
                cur = con.cursor()
                for i in file_reader:
                    if i:
                        new_book = Book(i[1], i[2], i[3])
                        cur.execute(f"INSERT INTO `bookshelf`.`books` (`name`, `author`, `janr`)\
                                        VALUES ('{new_book.name}', '{new_book.author}', '{new_book.janr}');")
                con.commit()


class TxtDriverBuilder:
    def __init__(self, filename):
        filename = filename.strip()
        if not str(filename).endswith(".txt"):
            filename = filename + ".txt"
        self.filename = filename

    def write(self, data):
        with open(self.filename, "w", encoding="utf-8") as f:
            for i in data:
                json.dump(i, f, ensure_ascii=False)
                f.write("\n")

    def read(self):
        with open(self.filename, "r", encoding="utf-8") as f:
            data = []
            for i in f.readlines():
                if len(i) > 1:
                    data.append(json.loads(i[:-1]))
            con = Connection.connect()
            with con:
                cur = con.cursor()
                for i in data:
                    new_book = Book(i[1], i[2], i[3])
                    cur.execute(f"INSERT INTO `bookshelf`.`books` (`name`, `author`, `janr`)\
                                    VALUES ('{new_book.name}', '{new_book.author}', '{new_book.janr}');")
                con.commit()


class SaveLoad:
    def __init__(self, data, filename):
        if tkgui.writer_var.get() == 1:
            self.driver = JsonDriverBuilder(filename)
        elif tkgui.writer_var.get() == 2:
            self.driver = CSVDriverBuilder(filename)
        elif tkgui.writer_var.get() == 3:
            self.driver = TxtDriverBuilder(filename)
        self.data = data

    def write(self):
        self.driver.write(self.data)

    def read(self):
        return self.driver.read()


class Actions:
    @staticmethod
    def add_book():
        """
        Функция проверяет введенные пользователем данные и,
        в случае корректности, записывает их в базу данных
        :return: None
        """
        if tkgui.add_name.get() and tkgui.add_autor.get() and tkgui.add_janr.get():
            new_book = Book(tkgui.add_name.get(), tkgui.add_autor.get(), tkgui.add_janr.get())
            con = Connection.connect()
            with con:
                cur = con.cursor()
                cur.execute(f"INSERT INTO `bookshelf`.`books` (`name`, `author`, `janr`)\
                             VALUES ('{new_book.name}', '{new_book.author}', '{new_book.janr}');")
                con.commit()
        else:
            messagebox.showinfo("Ошибка!", "Заполните все данные по книге!")
            return
        messagebox.showinfo("Успех!", "Книга успешно добавлена в базу!")
        Actions.add_clearing()

    @staticmethod
    def add_clearing():
        """
        Функция очищает поля вкладки "Добавление книги"
        :return: None
        """
        tkgui.add_name.delete(0, END)
        tkgui.add_autor.delete(0, END)
        tkgui.add_janr.delete(0, END)

    @staticmethod
    def finder():
        """
        Функция получает длину списка книг, считывает условия поиска
        и осуществляет поиск в списке книг по паттерну
        :param
        :return: result - список книг, удовлетворяющих условию поиска
        """
        pattern = tkgui.find_usl.get()
        con = Connection.connect()
        with con:
            cur = con.cursor()
            if tkgui.find_var.get() == 1:
                cur.execute(f"SELECT * FROM `bookshelf`.`books` WHERE name LIKE '%{pattern}%';")
            elif tkgui.find_var.get() == 2:
                cur.execute(f"SELECT * FROM `bookshelf`.`books` WHERE author LIKE '%{pattern}%';")
            else:
                cur.execute(f"SELECT * FROM `bookshelf`.`books` WHERE janr LIKE '%{pattern}%';")
            result = list(cur.fetchall())
        return result

    @staticmethod
    def find_book():
        """
        Функция сбрасывает результаты предыдущего поиска,
        считает длину списка книг в библиотеке, передает ее в
        функцию finder(), получает список с результатами,
        записывает результаты поиска в файл "search.txt"
        :return: result
        """
        Actions.find_clearing()
        result = Actions.finder()
        Actions.result_print(result)
        return result

    @staticmethod
    def result_print(result, index=0):
        """
        Функция выводит первое значение из списка результатов поиска,
        если он не пустой. После этого, если в списке больше 1 значения,
        активирует кнопки листинга.
        :param index: индекс выводимого элемента из списка результатов
        :param result: список книг, удовлетворяющий условиям поиска
        :return: None
        """
        tkgui.find_message.configure(text=f"Результат поиска: {index + 1 if len(result) != 0 else 0} из {len(result)}")
        if result:
            tkgui.find_name.configure(state="normal")
            tkgui.find_name.delete(0, END)
            tkgui.find_name.insert(0, result[index][1])
            tkgui.find_name.configure(state="disabled")
            tkgui.find_autor.configure(state="normal")
            tkgui.find_autor.delete(0, END)
            tkgui.find_autor.insert(0, result[index][2])
            tkgui.find_autor.configure(state="disabled")
            tkgui.find_janr.configure(state="normal")
            tkgui.find_janr.delete(0, END)
            tkgui.find_janr.insert(0, result[index][3])
            tkgui.find_janr.configure(state="disabled")
            tkgui.change_button.configure(state="normal")
            tkgui.del_button.configure(state="normal")
        if len(result) > 1:
            tkgui.find_next_button.configure(state="normal")
            tkgui.find_prev_button.configure(state="normal")
        return result[index][0]

    @staticmethod
    def next_result(result_list):
        """
        Функция выводит следующее значение из списка результатов поиска
        :return: None
        """
        current_pos = 0
        for i in result_list:
            if i[1] == tkgui.find_name.get() and i[2] == tkgui.find_autor.get() and i[3] == tkgui.find_janr.get():
                current_pos = result_list.index(i)
        if current_pos == len(result_list) - 1:
            return
        book_id = Actions.result_print(result_list, current_pos + 1)
        return book_id

    @staticmethod
    def prev_result(result_list):
        """
        Функция выводит предыдущее значение из списка результатов поиска
        :return: None
        """
        current_pos = 0
        for i in result_list:
            if i[1] == tkgui.find_name.get() and i[2] == tkgui.find_autor.get() and i[3] == tkgui.find_janr.get():
                current_pos = result_list.index(i)
        if current_pos == 0:
            return
        book_id = Actions.result_print(result_list, current_pos - 1)
        return book_id

    @staticmethod
    def find_clearing():
        """
        Функция очищает поля и сбрасывает состояние кнопок
        на вкладке "Поиск книги"
        :return:
        """
        tkgui.find_name.configure(state="normal")
        tkgui.find_name.delete(0, END)
        tkgui.find_name.configure(state="disabled")
        tkgui.find_autor.configure(state="normal")
        tkgui.find_autor.delete(0, END)
        tkgui.find_autor.configure(state="disabled")
        tkgui.find_janr.configure(state="normal")
        tkgui.find_janr.delete(0, END)
        tkgui.find_janr.configure(state="disabled")
        tkgui.find_next_button.configure(state="disabled")
        tkgui.find_prev_button.configure(state="disabled")
        tkgui.find_message.configure(text="")
        tkgui.change_button.configure(state="disabled")
        tkgui.save_button.configure(state="disabled")
        tkgui.del_button.configure(state="disabled")

    @staticmethod
    def del_book(result_list):
        """
        Функция удаляет книгу, которая выведена в текущий момент в поисковых
        полях, из базы данных
        :return: None
        """
        del_book_id = 0
        for i in result_list:
            if i[1] == tkgui.find_name.get() and i[2] == tkgui.find_autor.get() and i[3] == tkgui.find_janr.get():
                del_book_id = i[0]
        con = Connection.connect()
        with con:
            cur = con.cursor()
            cur.execute(f"DELETE FROM books WHERE idbooks = '{del_book_id}';")
            con.commit()
        messagebox.showinfo("Успех!", "Книга удалена из базы!")
        Actions.find_clearing()

    @staticmethod
    def save_book(book_id):
        """
        Функция сохраняет введенные изменения по книге в библиотеку
        :return:
        """
        con = Connection.connect()
        with con:
            cur = con.cursor()
            cur.execute(f"UPDATE bookshelf.books \
            SET name = '{tkgui.find_name.get()}', \
            author = '{tkgui.find_autor.get()}', \
            janr = '{tkgui.find_janr.get()}' \
            WHERE (idbooks = '{book_id}');")
            con.commit()
            messagebox.showinfo("Успех!", "Изменения внесены в базу!")
            Actions.find_clearing()

    @staticmethod
    def change_book(book_id):
        """
        Функция кнопки "Внести изменения". Делает доступными соответствубщие кнопки и поля
        :return:
        """
        tkgui.change_button.configure(state="disabled")
        Actions.change_config()
        return book_id

    @staticmethod
    def change_config():
        tkgui.find_name.configure(state="normal")
        tkgui.find_autor.configure(state="normal")
        tkgui.find_janr.configure(state="normal")
        tkgui.del_button.configure(state="disabled")
        tkgui.find_next_button.configure(state="disabled")
        tkgui.find_prev_button.configure(state="disabled")
        tkgui.save_button.configure(state="normal")

    def save_config(self):
        pass


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

        self.add_button = Button(self.add_tab, text="ДОБАВИТЬ В БАЗУ", command=Actions.add_book)
        self.add_button.grid(column=1, row=4, pady=10)

        # ---------------- Заполение вкладки "Поиск книги"--------------------
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

        # ---------------- Заполение вкладки "Настройки"--------------------
        # ---------------- Заполение данных "Настройки БД"--------------------
        self.config_DB_string = Label(self.config_tab, text="Настройки БД:")
        self.config_DB_string.grid(column=0, row=0, padx=10, pady=10, sticky=W)

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

        self.save_conf_button = Button(self.config_tab, text="Проверить подключение", command=Connection.connect,
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

    def main(self):
        self.root.mainloop()

    def search(self):
        self.result = Actions.find_book()
        self.book_id = self.result[0][0]

    def next_result(self):
        self.book_id = Actions.next_result(self.result)

    def prev_result(self):
        self.book_id = Actions.prev_result(self.result)

    def delete_book(self):
        Actions.del_book(self.result)

    def change_book(self):
        Actions.change_book(self.book_id)

    def save_book(self):
        Actions.save_book(self.book_id)

    def save_file(self):
        TkGUI.verify_path(self.file_entry.get())
        con = Connection.connect()
        with con:
            cur = con.cursor()
            if tkgui.find_var.get() == 1:
                cur.execute(f"SELECT * FROM `bookshelf`.`books`;")
            self.data = list(cur.fetchall())
        self.save_driver = SaveLoad(self.data, self.file_entry.get())
        self.save_driver.write()

    def load_file(self):
        self.save_driver = SaveLoad(self.data, self.file_entry.get())
        self.save_driver.read()

    @staticmethod
    def verify_path(path):
        counter = len(path)
        while counter > 0:
            print(path[-1], type(path[-1]))
            if path[-1] == "/" or path[-1] == "\\":
                path = path[:-1]
                break
            else:
                path = path[:-1]
                counter -= 1
        if len(path) and not os.path.exists(path):
            os.makedirs(path)
        print(path)


if __name__ == '__main__':
    tkgui = TkGUI()
    tkgui.main()
