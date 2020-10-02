import pymysql
import sqlite3
import logging


class Connection:
    @staticmethod
    def connect(choice, db_name, login=None, password=None):
        """
        Проверяет выбор пользователя, какую БД использовать и создает подключение.
        :return: con - подключение к БД
        """
        if choice == 2:
            con = sqlite3.connect(db_name)
            cur = con.cursor()
            cur.execute("CREATE TABLE IF NOT EXISTS books (`idbooks` INTEGER PRIMARY KEY AUTOINCREMENT,"
                        "`name` VARCHAR(45), `author` VARCHAR(45), `janr` VARCHAR(45));")
            con.commit()
            logging.warning(f"Успешное подключение к базе данных '{db_name}'!")
            return con
        elif choice == 1:
            try:
                con = pymysql.connect('localhost', f'{login}',
                                      f'{password}', f'{db_name}')
                logging.warning(f"Успешное подключение к базе данных '{db_name}'!")
                return con
            except pymysql.err.OperationalError or pymysql.err.InternalError:
                logging.warning("Ошибка подключения к базе данных!!!")
