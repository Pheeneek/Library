import json
import re
from tkinter import *
from tkinter import ttk
from tkinter.ttk import Radiobutton
from tkinter import messagebox


def add_book():
    if add_name.get() and add_autor.get() and add_janr.get():
        new_book = [add_name.get(), add_autor.get(), add_janr.get()]
        with open("library.lib", "a", encoding="utf-8")as f:
            json.dump(new_book, f, ensure_ascii=False)
            f.write("\n")
    else:
        add_message.configure(text="Заполните все данные по книге!")
        return False
    messagebox.showinfo("Успех!", "Книга успешно добавлена в базу!")
    add_name.delete(0, END)
    add_autor.delete(0, END)
    add_janr.delete(0, END)


def clearing():
    find_name.configure(state="normal")
    find_name.delete(0, END)
    find_name.configure(state="disabled")
    find_autor.configure(state="normal")
    find_autor.delete(0, END)
    find_autor.configure(state="disabled")
    find_janr.configure(state="normal")
    find_janr.delete(0, END)
    find_janr.configure(state="disabled")


def find_book():
    clearing()
    pattern = find_usl.get()
    with open("library.lib", "r", encoding="utf-8")as f:
        # result=[]
        while True:
            a = json.loads(f.readline()[:-1])
            b = re.search(pattern, str(a))
            if b:
                # result.append(a)
                find_name.configure(state="normal")
                find_name.delete(0, END)
                find_name.insert(0, a[0])
                find_name.configure(state="disabled")
                find_autor.configure(state="normal")
                find_autor.delete(0, END)
                find_autor.insert(0, a[1])
                find_autor.configure(state="disabled")
                find_janr.configure(state="normal")
                find_janr.delete(0, END)
                find_janr.insert(0, a[2])
                find_janr.configure(state="disabled")
            return None



def next_book():
    pass


root = Tk()
root.title("Библиотека")
root.geometry("600x250")
tab_control = ttk.Notebook(root)
add_tab = ttk.Frame(tab_control)
find_tab = ttk.Frame(tab_control)
tab_control.add(add_tab, text="Добавить книгу")
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

tab_control.add(find_tab, text="Поиск книги")
tab_control.pack(expand=1, fill="both")


rad1 = Radiobutton(find_tab, text='Искать по названию', value=1)
rad2 = Radiobutton(find_tab, text='Искать по автору', value=2)
rad3 = Radiobutton(find_tab, text='Искать по жанру', value=3)
rad1.grid(column=0, row=0)
rad2.grid(column=1, row=0)
rad3.grid(column=2, row=0)

add_first_string = Label(find_tab, text="Введите условия поиска:")
add_first_string.grid(column=0, row=1, padx=10, pady=10)

find_usl = Entry(find_tab, width=40)
find_usl.grid(column=1, row=1, padx=0, pady=0)

find_message = Label(find_tab)
find_message.grid(column=0, row=5, pady=0)

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

find_button = Button(find_tab, text="Искать", command=find_book)
find_button.grid(column=1, row=9, pady=10)
find_next_button = Button(find_tab, text="Искать далее", command=next_book, state="disabled")
find_next_button.grid(column=2, row=9, pady=10)

root.mainloop()

