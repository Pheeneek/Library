import json
import re
from tkinter import *
from tkinter import ttk
from tkinter.ttk import Radiobutton
from tkinter import messagebox


def add_book():
    """
    Функция проверяет введенные пользователем данные и,
    в случае корректности, записывает их в конец файла "library.lib"
    :return:
    """
    if add_name.get() and add_autor.get() and add_janr.get():
        new_book = [add_name.get(), add_autor.get(), add_janr.get()]
        with open("library.lib", "a", encoding="utf-8")as f:
            json.dump(new_book, f, ensure_ascii=False)
            f.write("\n")
    else:
        add_message.configure(text="Заполните все данные по книге!")
        return False
    messagebox.showinfo("Успех!", "Книга успешно добавлена в базу!")
    add_clearing()


def add_clearing():
    """
    Функция очищает поля вкладки "Добавление книги"
    :return:
    """
    add_name.delete(0, END)
    add_autor.delete(0, END)
    add_janr.delete(0, END)


def finder(length):
    """
    Функция получает длину списка книг, считывает условия поиска
    и осуществляет поиск в списке книг по паттерну
    :param length: Количество строк в файле библиотеки (количество книг)
    :return: result - список книг, удовлетворяющих условию поиска
    """
    pattern = find_usl.get()
    result = []
    if not pattern:
        return result
    with open("library.lib", "r", encoding="utf-8")as f:
        if find_var.get() == 1:
            n = 0
        elif find_var.get() == 2:
            n = 1
        else:
            n = 2
        for _ in range(length):
            a = json.loads(f.readline())
            b = re.search(pattern, str(a[n]))
            if b:
                result.append(a)
    return result


def find_book():
    """
    Функция сбрасывает результаты предыдущего поиска,
    считает длину списка книг в библиотеке, передает ее в
    функцию finder(), получает список с результатами,
    записывает результаты поиска в файл "search.txt"
    :return:
    """
    find_clearing()
    pattern = r"\n"
    with open("library.lib", "r", encoding="utf-8")as f:
        length = len(re.findall(pattern, f.read()))
        result = finder(length)
    if result:
        with open("search.txt", "w", encoding="utf-8")as f:
            for i in result:
                json.dump(i, f, ensure_ascii=False)
                f.write("\n")
    result_print(result)


def result_print(result):
    """
    Функция выводит первое значение из списка результатов поиска,
    если он не пустой. После этого, если в списке больше 1 значения,
    активирует кнопки листинга.
    :param result: список книг, удовлетворяющий условиям поиска
    :return:
    """
    find_message.configure(text=f"Найдено книг: {len(result)}")
    if result:
        find_name.configure(state="normal")
        find_name.delete(0, END)
        find_name.insert(0, result[0][0])
        find_name.configure(state="disabled")
        find_autor.configure(state="normal")
        find_autor.delete(0, END)
        find_autor.insert(0, result[0][1])
        find_autor.configure(state="disabled")
        find_janr.configure(state="normal")
        find_janr.delete(0, END)
        find_janr.insert(0, result[0][2])
        find_janr.configure(state="disabled")
        change_button.configure(state="normal")
        del_button.configure(state="normal")
    if len(result) > 1:
        find_next_button.configure(state="normal")
        find_prev_button.configure(state="normal")


def next_result():
    """
    Функция выводит следующее значение из списка результатов поиска
    :return: Возвращает None, если достигнут конец списка
    """
    pattern = [find_name.get(), find_autor.get(), find_janr.get()]
    with open("search.txt", "r", encoding="utf-8")as f:
        result_list = []
        for i in f.readlines():
            result_list.append(json.loads(i))
    for i in result_list:
        if i == pattern:
            current_pos = result_list.index(i)
    if current_pos == len(result_list) - 1:
        return None
    find_name.configure(state="normal")
    find_name.delete(0, END)
    find_name.insert(0, result_list[current_pos + 1][0])
    find_name.configure(state="disabled")
    find_autor.configure(state="normal")
    find_autor.delete(0, END)
    find_autor.insert(0, result_list[current_pos + 1][1])
    find_autor.configure(state="disabled")
    find_janr.configure(state="normal")
    find_janr.delete(0, END)
    find_janr.insert(0, result_list[current_pos + 1][2])
    find_janr.configure(state="disabled")


def prev_result():
    """
    Функция выводит предыдущее значение из списка результатов поиска
    :return: Возвращает None, если достигнуто начало списка
    """
    pattern = [find_name.get(), find_autor.get(), find_janr.get()]
    with open("search.txt", "r", encoding="utf-8")as f:
        result_list = []
        for i in f.readlines():
            result_list.append(json.loads(i))
    for i in result_list:
        if i == pattern:
            current_pos = result_list.index(i)
    if current_pos == 0:
        return None
    find_name.configure(state="normal")
    find_name.delete(0, END)
    find_name.insert(0, result_list[current_pos-1][0])
    find_name.configure(state="disabled")
    find_autor.configure(state="normal")
    find_autor.delete(0, END)
    find_autor.insert(0, result_list[current_pos-1][1])
    find_autor.configure(state="disabled")
    find_janr.configure(state="normal")
    find_janr.delete(0, END)
    find_janr.insert(0, result_list[current_pos-1][2])
    find_janr.configure(state="disabled")


def find_clearing():
    """
    Функция очищает поля и сбрасывает состояние кнопок
    на вкладке "Поиск книги"
    :return:
    """
    find_name.configure(state="normal")
    find_name.delete(0, END)
    find_name.configure(state="disabled")
    find_autor.configure(state="normal")
    find_autor.delete(0, END)
    find_autor.configure(state="disabled")
    find_janr.configure(state="normal")
    find_janr.delete(0, END)
    find_janr.configure(state="disabled")
    find_next_button.configure(state="disabled")
    find_prev_button.configure(state="disabled")
    find_message.configure(text="")
    change_button.configure(state="disabled")
    save_button.configure(state="disabled")
    del_button.configure(state="disabled")


def del_book():
    """
    Функция удаляет книгу, которая выведена в текущий момент в поисковых
    полях, из файла "library.lib"
    :return: Возвращает None, если поле с наименованием книги пустое
    """
    if not find_name.get():
        return None
    del_list = []
    with open("library.lib", "r", encoding="utf-8") as f:
        for i in f.readlines():
            del_list.append(json.loads(i))
    for i in del_list:
        if i == [find_name.get(), find_autor.get(), find_janr.get()]:
            del_index = del_list.index(i)
    del_list.pop(del_index)
    with open("library.lib", "w", encoding="utf-8") as f:
        for i in del_list:
            json.dump(i, f, ensure_ascii=False)
            f.write("\n")
    messagebox.showinfo("Успех!", "Книга удалена из базы!")
    find_clearing()


def save_book():
    """
    Функция сохраняет введенные изменения по книге в библиотеку
    :return:
    """
    new_book = f'["{find_name.get()}", "{find_autor.get()}", "{find_janr.get()}"]\n'
    with open("library.lib", "r", encoding="utf-8") as f:
        lib = f.read()
    with open("change.txt", "r", encoding="utf-8") as f:
        change = f.read()
    lib = lib.replace(change, new_book)
    with open("library.lib", "w", encoding="utf-8") as f:
        f.write(lib)
        messagebox.showinfo("Успех!", "Изменения внесены в базу!")
        find_clearing()


def change_book():
    """
    Функция кнопки "Внести изменения". Делает доступными соответствубщие кнопки и поля
    :return:
    """
    change_button.configure(state="disabled")
    changing_book = [find_name.get(), find_autor.get(), find_janr.get()]
    with open("change.txt", "w", encoding="utf-8")as f:
        json.dump(changing_book, f, ensure_ascii=False)
        f.write("\n")
    find_name.configure(state="normal")
    find_autor.configure(state="normal")
    find_janr.configure(state="normal")
    del_button.configure(state="disabled")
    find_next_button.configure(state="disabled")
    find_prev_button.configure(state="disabled")
    save_button.configure(state="normal")

# ---------------- отрисовка основного окна--------------------
root = Tk()
root.title("Библиотека")
root.geometry("600x250")
# ---------------- добавление вкладок--------------------
tab_control = ttk.Notebook(root)
add_tab = ttk.Frame(tab_control)
find_tab = ttk.Frame(tab_control)
remove_tab = ttk.Frame(tab_control)
tab_control.add(add_tab, text="Добавить книгу")
tab_control.add(find_tab, text="Поиск книг")
tab_control.pack(expand=1, fill="both")
# ---------------- заполение вкладки "Добавить книгу"--------------------
add_first_string = Label(add_tab, text="Введите данные добавляемой книги:")
add_first_string.grid(column=0, row=0, padx=10, pady=10, columnspan=2, sticky=W)
add_name_string = Label(add_tab, text="Наименование книги:")
add_name_string.grid(column=0, row=1, padx=10, pady=0, sticky=W)
add_name = Entry(add_tab, width="40")
add_name.grid(column=1, row=1, padx=10, sticky=W)
add_autor_string = Label(add_tab, text="Автор:")
add_autor_string.grid(column=0, row=2, pady=10, sticky=W, padx=10)
add_autor = Entry(add_tab, width="40")
add_autor.grid(column=1, row=2, padx=10, sticky=W)
add_janr_string = Label(add_tab, text="Жанр:")
add_janr_string.grid(column=0, row=3, pady=0, padx=10, sticky=W)
add_janr = Entry(add_tab, width="40")
add_janr.grid(column=1, row=3, padx=0)
add_button = Button(add_tab, text="ДОБАВИТЬ В БАЗУ", command=add_book)
add_button.grid(column=1, row=4, pady=10)
add_message = Label(add_tab)
add_message.grid(column=0, row=5, pady=0)
# ---------------- Заполение вкладки "Поиск книги"--------------------
find_var = IntVar()
find_var.set(1)
rad1 = Radiobutton(find_tab, text='Искать по названию', variable=find_var, value=1)
rad2 = Radiobutton(find_tab, text='Искать по автору', variable=find_var, value=2)
rad3 = Radiobutton(find_tab, text='Искать по жанру', variable=find_var, value=3)
rad1.grid(column=0, row=0)
rad2.grid(column=1, row=0)
rad3.grid(column=2, row=0)

add_first_string = Label(find_tab, text="Введите условия поиска:")
add_first_string.grid(column=0, row=1, padx=10, pady=10)

find_usl = Entry(find_tab, width=40)
find_usl.grid(column=1, row=1, padx=0, pady=0)

find_message = Label(find_tab)
find_message.grid(column=1, row=5, pady=0)

find_name_string = Label(find_tab, text="Наименование книги:")
find_name_string.grid(column=0, row=6, padx=10, pady=0, sticky=W)
find_name = Entry(find_tab, width="40", state="disabled")
find_name.grid(column=1, row=6, padx=10, sticky=W)
find_autor_string = Label(find_tab, text="Автор:")
find_autor_string.grid(column=0, row=7, pady=10, sticky=W, padx=10)
find_autor = Entry(find_tab, width="40", state="disabled")
find_autor.grid(column=1, row=7, padx=10, sticky=W)
find_janr_string = Label(find_tab, text="Жанр:")
find_janr_string.grid(column=0, row=8, pady=0, padx=10, sticky=W)
find_janr = Entry(find_tab, width="40", state="disabled")
find_janr.grid(column=1, row=8, padx=0)

find_prev_button = Button(find_tab, text="<<<", command=prev_result, state="disabled")
find_prev_button.grid(column=0, row=9, pady=10)

find_button = Button(find_tab, text="Искать", command=find_book)
find_button.grid(column=1, row=9, pady=10)

find_next_button = Button(find_tab, text=">>>", command=next_result, state="disabled")
find_next_button.grid(column=2, row=9, pady=10)

change_button = Button(find_tab, text="    Изменить данные    ", command=change_book, state="disabled")
change_button.grid(column=2, row=6)

save_button = Button(find_tab, text="Сохранить изменения", command=save_book, state="disabled")
save_button.grid(column=2, row=7)

del_button = Button(find_tab, text="Удалить книгу из базы", command=del_book, state="disabled")
del_button.grid(column=2, row=8)

root.mainloop()

