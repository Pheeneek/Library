import json


library = {"Мастер и Маргарита":["М.А.Булгаков", "роман", "Фантастика", "1", "1", "1"]}

with open("library.lib", "w", encoding="utf8")as f:
    json.dump(library, f)