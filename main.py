import json
import tkinter as tk

library = {"Мастер и Маргарита": ["М.А.Булгаков", "роман", "Фантастика", "1", "1", "1"]}

with open("library.lib", "w", encoding="utf-8")as f:
    json.dump(library, f, indent=4, ensure_ascii=False)

with open("library.lib", "r", encoding="utf-8")as f:
    print(json.load(f))