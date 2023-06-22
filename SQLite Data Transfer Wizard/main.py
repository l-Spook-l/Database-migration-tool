# Перенос нужных таблиц из одно БД в другую SQLIte
import sqlite3


def data_transfer():
    try:
        # Открываем подключение к исходной базе данных
        source_conn = sqlite3.connect('db.sqlite3')
        source_cursor = source_conn.cursor()

        # Открываем подключение к целевой базе данных
        target_conn = sqlite3.connect(
            'C:\Disk_D\Python_project\Django\Django_React_Golf_store\server\golf_home\db.sqlite3')
        target_cursor = target_conn.cursor()
        print("DataBase connect")
        try:
            # source_cursor.execute("SELECT * FROM store_brandproduct")
            # rows = source_cursor.fetchall()
            # for row in rows:
            #     target_cursor.execute("INSERT INTO store_brandproduct VALUES (?, ?, ?, ?, ?)", row)

            # source_cursor.execute("SELECT * FROM store_typeproduct")
            # rows = source_cursor.fetchall()
            # for row in rows:
            #     target_cursor.execute("INSERT INTO store_typeproduct VALUES (?, ?, ?)", row)

            # source_cursor.execute("SELECT * FROM store_categoryproduct")
            # rows = source_cursor.fetchall()
            # for row in rows:
            #     target_cursor.execute("INSERT INTO store_categoryproduct VALUES (?, ?, ?)", row)

            # source_cursor.execute("SELECT * FROM store_productphotos")
            # rows = source_cursor.fetchall()
            # for row in rows:
            #     target_cursor.execute("INSERT INTO store_productphotos VALUES (?, ?)", row)

            # source_cursor.execute("SELECT * FROM store_product")
            # rows = source_cursor.fetchall()
            # for row in rows:
            #     target_cursor.execute("INSERT INTO store_product VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)", row)

            source_cursor.execute("SELECT * FROM store_product_photos")
            rows = source_cursor.fetchall()
            for row in rows:
                target_cursor.execute("INSERT INTO store_product_photos VALUES (?, ?, ?)", row)

            # Сохраняем изменения и закрываем подключения к базам данных
            target_conn.commit()

        finally:
            source_conn.close()
            target_conn.close()
            print("DataBase disconnect")

    except Exception as ex:  # Если не удалось подключится вывести сообшение
        print("Connection refused...")
        print(ex)


def main():
    data_transfer()


if __name__ == "__main__":
    main()
