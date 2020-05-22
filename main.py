import json
from tkinter import *
from tkinter import ttk
# library = {"Мастер и Маргарита": ["М.А.Булгаков", "роман", "Фантастика", "1", "1", "1"],
#            "Трудно быть богом": ["А. и Б. Стругацкие", "роман", "Фантастика", "1", "1", "2"]}
#
# with open("library.lib", "w", encoding="utf-8")as f:
#     json.dump(library, f, indent=4, ensure_ascii=False)
#
# with open("library.lib", "r", encoding="utf-8")as f:
#     library = json.load(f)
#     for i in library.items():
#         print(i)

def add_book():
    new_book = {str(add_name.get()):[add_autor.get(),add_janr.get()]}
    with open("library.lib", "a", encoding="utf-8")as f:
        json.dump(new_book, f, indent=4, ensure_ascii=False)


root = Tk()
root.title("Библиотека")
root.geometry("600x250")
tab_control = ttk.Notebook(root)
add_tab = ttk.Frame(tab_control)
find_tab = ttk.Frame(tab_control)
tab_control.add(add_tab, text="Добавить книгу")
add_first_string = Label(add_tab, text="Введите данные добавляемой книги:")
add_first_string.grid(column=0, row=0, padx=10, pady=10)
add_name_string = Label(add_tab, text="Наименование книги:")
add_name_string.grid(column=0, row=1, padx=0, pady=0)
add_name = Entry(add_tab, width="40")
add_name.grid(column=1, row=1, padx=10)
add_autor = Label(add_tab, text="Автор:")
add_autor.grid(column=0, row=2, pady=10)
add_autor = Entry(add_tab, width="40")
add_autor.grid(column=1, row=2, padx=10)
add_janr = Label(add_tab, text="Жанр:")
add_janr.grid(column=0, row=3, pady=0)
add_janr = Entry(add_tab, width="40")
add_janr.grid(column=1, row=3, padx=0)
add_button = Button(add_tab, text="ДОБАВИТЬ В БАЗУ", command=add_book)
add_button.grid(column=1, row=4, pady=10)
tab_control.add(find_tab, text="Поиск книги")
tab_control.pack(expand=1, fill="both")

root.mainloop()

