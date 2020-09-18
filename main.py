import json
import pymysql
# import re
from tkinter import *
from tkinter import ttk
from tkinter import messagebox


class Book:
    def __init__(self, name, author, janr):
        self.name = name
        self.author = author
        self.janr = janr


class Actions:
    @staticmethod
    def add_book():
        """
        Функция проверяет введенные пользователем данные и,
        в случае корректности, записывает их в конец файла "library.lib"
        :return:
        """
        if tkgui.add_name.get() and tkgui.add_autor.get() and tkgui.add_janr.get():
            new_book = [tkgui.add_name.get(), tkgui.add_autor.get(), tkgui.add_janr.get()]
            with open("library.lib", "a", encoding="utf-8")as f:
                json.dump(new_book, f, ensure_ascii=False)
                f.write("\n")
        else:
            tkgui.add_message.configure(text="Заполните все данные по книге!")
            return False
        messagebox.showinfo("Успех!", "Книга успешно добавлена в базу!")
        Actions.add_clearing()

    @staticmethod
    def add_clearing():
        """
        Функция очищает поля вкладки "Добавление книги"
        :return:
        """
        tkgui.add_name.delete(0, END)
        tkgui.add_autor.delete(0, END)
        tkgui.add_janr.delete(0, END)

    @staticmethod
    def finder(length):
        """
        Функция получает длину списка книг, считывает условия поиска
        и осуществляет поиск в списке книг по паттерну
        :param length: Количество строк в файле библиотеки (количество книг)
        :return: result - список книг, удовлетворяющих условию поиска
        """
        pattern = tkgui.find_usl.get()
        result = []
        with open("library.lib", "r", encoding="utf-8")as f:
            if tkgui.find_var.get() == 1:
                n = 0
            elif tkgui.find_var.get() == 2:
                n = 1
            else:
                n = 2
            for _ in range(length):
                a = json.loads(f.readline())
                b = re.search(pattern, str(a[n]))
                if b:
                    result.append(a)
        return result

    @staticmethod
    def find_book():
        """
        Функция сбрасывает результаты предыдущего поиска,
        считает длину списка книг в библиотеке, передает ее в
        функцию finder(), получает список с результатами,
        записывает результаты поиска в файл "search.txt"
        :return:
        """
        Actions.find_clearing()
        pattern = r"\n"
        with open("library.lib", "r", encoding="utf-8")as f:
            length = len(re.findall(pattern, f.read()))
            result = Actions.finder(length)
        if result:
            with open("search.txt", "w", encoding="utf-8")as f:
                for i in result:
                    json.dump(i, f, ensure_ascii=False)
                    f.write("\n")
        Actions.result_print(result)

    @staticmethod
    def result_print(result):
        """
        Функция выводит первое значение из списка результатов поиска,
        если он не пустой. После этого, если в списке больше 1 значения,
        активирует кнопки листинга.
        :param result: список книг, удовлетворяющий условиям поиска
        :return:
        """
        tkgui.find_message.configure(text=f"Найдено книг: {len(result)}")
        if result:
            tkgui.find_name.configure(state="normal")
            tkgui.find_name.delete(0, END)
            tkgui.find_name.insert(0, result[0][0])
            tkgui.find_name.configure(state="disabled")
            tkgui.find_autor.configure(state="normal")
            tkgui.find_autor.delete(0, END)
            tkgui.find_autor.insert(0, result[0][1])
            tkgui.find_autor.configure(state="disabled")
            tkgui.find_janr.configure(state="normal")
            tkgui.find_janr.delete(0, END)
            tkgui.find_janr.insert(0, result[0][2])
            tkgui.find_janr.configure(state="disabled")
            tkgui.change_button.configure(state="normal")
            tkgui.del_button.configure(state="normal")
        if len(result) > 1:
            tkgui.find_next_button.configure(state="normal")
            tkgui.find_prev_button.configure(state="normal")

    @staticmethod
    def next_result():
        """
        Функция выводит следующее значение из списка результатов поиска
        :return: Возвращает None, если достигнут конец списка
        """
        pattern = [tkgui.find_name.get(), tkgui.find_autor.get(), tkgui.find_janr.get()]
        with open("search.txt", "r", encoding="utf-8")as f:
            result_list = []
            for i in f.readlines():
                result_list.append(json.loads(i))
        for i in result_list:
            if i == pattern:
                current_pos = result_list.index(i)
        if current_pos == len(result_list) - 1:
            return None
        tkgui.find_name.configure(state="normal")
        tkgui.find_name.delete(0, END)
        tkgui.find_name.insert(0, result_list[current_pos + 1][0])
        tkgui.find_name.configure(state="disabled")
        tkgui.find_autor.configure(state="normal")
        tkgui.find_autor.delete(0, END)
        tkgui.find_autor.insert(0, result_list[current_pos + 1][1])
        tkgui.find_autor.configure(state="disabled")
        tkgui.find_janr.configure(state="normal")
        tkgui.find_janr.delete(0, END)
        tkgui.find_janr.insert(0, result_list[current_pos + 1][2])
        tkgui.find_janr.configure(state="disabled")

    @staticmethod
    def prev_result():
        """
        Функция выводит предыдущее значение из списка результатов поиска
        :return: Возвращает None, если достигнуто начало списка
        """
        pattern = [tkgui.find_name.get(), tkgui.find_autor.get(), tkgui.find_janr.get()]
        with open("search.txt", "r", encoding="utf-8")as f:
            result_list = []
            for i in f.readlines():
                result_list.append(json.loads(i))
        for i in result_list:
            if i == pattern:
                current_pos = result_list.index(i)
        if current_pos == 0:
            return None
        tkgui.find_name.configure(state="normal")
        tkgui.find_name.delete(0, END)
        tkgui.find_name.insert(0, result_list[current_pos-1][0])
        tkgui.find_name.configure(state="disabled")
        tkgui.find_autor.configure(state="normal")
        tkgui.find_autor.delete(0, END)
        tkgui.find_autor.insert(0, result_list[current_pos-1][1])
        tkgui.find_autor.configure(state="disabled")
        tkgui.find_janr.configure(state="normal")
        tkgui.find_janr.delete(0, END)
        tkgui.find_janr.insert(0, result_list[current_pos-1][2])
        tkgui.find_janr.configure(state="disabled")

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
    def del_book():
        """
        Функция удаляет книгу, которая выведена в текущий момент в поисковых
        полях, из файла "library.lib"
        :return: Возвращает None, если поле с наименованием книги пустое
        """
        if not tkgui.find_name.get():
            return None
        del_list = []
        with open("library.lib", "r", encoding="utf-8") as f:
            for i in f.readlines():
                del_list.append(json.loads(i))
        for i in del_list:
            if i == [tkgui.find_name.get(), tkgui.find_autor.get(), tkgui.find_janr.get()]:
                del_index = del_list.index(i)
        del_list.pop(del_index)
        with open("library.lib", "w", encoding="utf-8") as f:
            for i in del_list:
                json.dump(i, f, ensure_ascii=False)
                f.write("\n")
        messagebox.showinfo("Успех!", "Книга удалена из базы!")
        Actions.find_clearing()

    @staticmethod
    def save_book():
        """
        Функция сохраняет введенные изменения по книге в библиотеку
        :return:
        """
        new_book = f'["{tkgui.find_name.get()}", "{tkgui.find_autor.get()}", "{tkgui.find_janr.get()}"]\n'
        with open("library.lib", "r", encoding="utf-8") as f:
            lib = f.read()
        with open("change.txt", "r", encoding="utf-8") as f:
            change = f.read()
        lib = lib.replace(change, new_book)
        with open("library.lib", "w", encoding="utf-8") as f:
            f.write(lib)
            messagebox.showinfo("Успех!", "Изменения внесены в базу!")
            Actions.find_clearing()

    @staticmethod
    def change_book():
        """
        Функция кнопки "Внести изменения". Делает доступными соответствубщие кнопки и поля
        :return:
        """
        tkgui.change_button.configure(state="disabled")
        changing_book = [tkgui.find_name.get(), tkgui.find_autor.get(), tkgui.find_janr.get()]
        with open("change.txt", "w", encoding="utf-8")as f:
            json.dump(changing_book, f, ensure_ascii=False)
            f.write("\n")
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

        self.add_message = Label(self.add_tab)
        self.add_message.grid(column=0, row=5, pady=0)
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

        self.find_prev_button = Button(self.find_tab, text="<<<", command=Actions.prev_result, state="disabled")
        self.find_prev_button.grid(column=0, row=9, pady=10)

        self.find_button = Button(self.find_tab, text="Искать", command=Actions.find_book)
        self.find_button.grid(column=1, row=9, pady=10)

        self.find_next_button = Button(self.find_tab, text=">>>", command=Actions.next_result, state="disabled")
        self.find_next_button.grid(column=2, row=9, pady=10)

        self.change_button = Button(self.find_tab, text="    Изменить данные    ", command=Actions.change_book, state="disabled")
        self.change_button.grid(column=2, row=6)

        self.save_button = Button(self.find_tab, text="Сохранить изменения", command=Actions.save_book, state="disabled")
        self.save_button.grid(column=2, row=7)

        self.del_button = Button(self.find_tab, text="Удалить книгу из базы", command=Actions.del_book, state="disabled")
        self.del_button.grid(column=2, row=8)

        # ---------------- Заполение вкладки "Настройки"--------------------
        # ---------------- Заполение данных "Настройки БД"--------------------
        self.config_DB_string = Label(self.config_tab, text="Настройки БД:")
        self.config_DB_string.grid(column=0, row=0, padx=10, pady=10, sticky=W)

        self.login_DB_string = Label(self.config_tab, text="Логин:")
        self.login_DB_string.grid(column=0, row=1, padx=10, pady=5, sticky=E)

        self.login_DB_entry = Entry(self.config_tab, width="10", state="normal")
        self.login_DB_entry.grid(column=1, row=1, padx=10, sticky=W)

        self.password_DB_string = Label(self.config_tab, text="Пароль:")
        self.password_DB_string.grid(column=2, row=1, padx=10, pady=5, sticky=W)

        self.password_DB_entry = Entry(self.config_tab, width="10", state="normal")
        self.password_DB_entry.grid(column=3, row=1, padx=10, sticky=W)

        self.name_DB_string = Label(self.config_tab, text="Имя БД:")
        self.name_DB_string.grid(column=4, row=1, padx=10, pady=5, sticky=W)

        self.name_DB_entry = Entry(self.config_tab, width="10", state="normal")
        self.name_DB_entry.grid(column=5, row=1, padx=10, sticky=W)

        self.save_conf_button = Button(self.config_tab, text="Сохранить", command=self.save_config, state="normal")
        self.save_conf_button.grid(column=1, row=2)

        # ---------------- Заполение данных "Насторойки выгрузки"--------------------

        self.config_writer_string = Label(self.config_tab, text="Настройки выгрузки:")
        self.config_writer_string.grid(column=0, row=3, padx=10, pady=10, sticky=W)

        self.writer_var = IntVar()
        self.writer_var.set(1)
        self.rad1 = ttk.Radiobutton(self.config_tab, text='в JSON', variable=self.writer_var, value=1)
        self.rad2 = ttk.Radiobutton(self.config_tab, text='в CSV', variable=self.writer_var, value=2)
        self.rad3 = ttk.Radiobutton(self.config_tab, text='в TXT', variable=self.writer_var, value=3)
        self.rad1.grid(column=1, row=3)
        self.rad2.grid(column=2, row=3)
        self.rad3.grid(column=3, row=3)


    def main(self):
        self.root.mainloop()

    def search(self):
        if self.checkbox == 1:
            field = self.find_usl.text

    def save_config(self):
        pass

if __name__ == '__main__':
    tkgui = TkGUI()
    tkgui.main()
