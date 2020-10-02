import json
import csv
import logging


class SaveLoad:
    def __init__(self, filename, writer_var, con):
        if writer_var == 1:
            self.driver = JsonDriverBuilder(filename, con)
        elif writer_var == 2:
            self.driver = CSVDriverBuilder(filename, con)
        elif writer_var == 3:
            self.driver = TxtDriverBuilder(filename, con)

    def write(self):
        self.driver.write()

    def read(self):
        self.driver.read()


class JsonDriverBuilder:
    def __init__(self, filename, con):
        filename = filename.strip()
        if not str(filename).endswith(".json"):
            filename = filename + ".json"
        self.filename = filename
        self.con = con

    def write(self):
        """
        Функция записывает данные из текущей базу данных в файл в формате json
        :param data: список книг
        :return: None
        """
        with self.con:
            cur = self.con.cursor()
            cur.execute(f"SELECT * FROM `books`;")
            data = cur.fetchall()
        self.con.close()
        with open(self.filename, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False)

    def read(self):
        """
        Загружает в базу данных книги из файла формата json, в случае наличия книги
        в базе выдает предупреждение
        :return: None
        """
        with open(self.filename, "r", encoding="utf-8") as f:
            data = json.load(f)
            with self.con:
                cur = self.con.cursor()
                for i in data:
                    if Search.search_for_book((f'{i[1]}', f'{i[2]}', f'{i[3]}'), self.con):
                        cur.execute(f"INSERT INTO `books` (`name`, `author`, `janr`)\
                                        VALUES ('{i[1]}', '{i[2]}', '{i[3]}');")
                    else:
                        logging.warning("Ошибка добавления! Книга уже есть в базе!")
                self.con.commit()


class CSVDriverBuilder:
    def __init__(self, filename, con):
        filename = filename.strip()
        if not filename.endswith(".csv"):
            filename = filename + ".scv"
        self.filename = filename
        self.con = con

    def write(self):
        """
        Функция записывает данные из текущей базу данных в файл в формате csv
        :param data: список книг
        :return: None
        """
        with self.con:
            cur = self.con.cursor()
            cur.execute(f"SELECT * FROM `books`;")
            data = cur.fetchall()
        self.con.close()
        with open(self.filename, "w", encoding="utf-8") as f:
            writer = csv.writer(f)
            for i in data:
                writer.writerow(i)

    def read(self):
        """
        Загружает в базу данных книги из файла формата csv, в случае наличия книги
        в базе выдает предупреждение
        :return: None
        """
        with open(self.filename, "r", encoding="utf-8") as f:
            file_reader = csv.reader(f, delimiter=",")
            with self.con:
                cur = self.con.cursor()
                for i in file_reader:
                    if i:
                        if Search.search_for_book((f'{i[1]}', f'{i[2]}', f'{i[3]}'), self.con):
                            cur.execute(f"INSERT INTO `books` (`name`, `author`, `janr`)\
                                            VALUES ('{i[1]}', '{i[2]}', '{i[3]}');")
                            logging.warning("Ошибка добавления! Книга уже есть в базе!")
                self.con.commit()


class TxtDriverBuilder:
    def __init__(self, filename, con):
        filename = filename.strip()
        if not str(filename).endswith(".txt"):
            filename = filename + ".txt"
        self.filename = filename
        self.con = con

    def write(self):
        """
        Функция записывает данные из текущей базу данных в файл в формате txt
        :param data: список книг
        :return: None
        """
        with self.con:
            cur = self.con.cursor()
            cur.execute(f"SELECT * FROM `books`;")
            data = cur.fetchall()
        self.con.close()
        with open(self.filename, "w", encoding="utf-8") as f:
            for i in data:
                json.dump(i, f, ensure_ascii=False)
                f.write("\n")

    def read(self):
        """
        Загружает в базу данных книги из файла формата txt, в случае наличия книги
        в базе выдает предупреждение
        :return: None
        """
        with open(self.filename, "r", encoding="utf-8") as f:
            data = []
            for i in f.readlines():
                if len(i) > 1:
                    data.append(json.loads(i[:-1]))
            with self.con:
                cur = self.con.cursor()
                for i in data:
                    if Search.search_for_book((f'{i[1]}', f'{i[2]}', f'{i[3]}'), self.con):
                        cur.execute(f"INSERT INTO `books` (`name`, `author`, `janr`)\
                                        VALUES ('{i[1]}', '{i[2]}', '{i[3]}');")
                    else:
                        logging.warning("Ошибка добавления! Книга уже есть в базе!")
                self.con.commit()


class Search:
    @staticmethod
    def search_for_book(book, con):
        """

        :param book:
        :param con:
        :return:
        """
        with con:
            cur = con.cursor()
            cur.execute("SELECT name, author, janr FROM `books`")
            books = cur.fetchall()
            if book not in books:
                return True
