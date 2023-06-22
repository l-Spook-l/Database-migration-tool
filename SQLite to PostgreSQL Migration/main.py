import psycopg2
import sqlite3

from config import db_name, user, password, host, port

try:
    # Подключение к БД postgreSQL
    postgresql_connection = psycopg2.connect(
        dbname=db_name,
        user=user,
        password=password,
        host=host,
        port=port
    )
    # Автокомит для postgresql
    postgresql_connection.autocommit = True

    # Подключение к БД Sqlite
    sqlite_connection = sqlite3.connect('db.sqlite3')
    # Получаем объект курсора
    sqlite_cursor = sqlite_connection.cursor()

    print("DataBase connect")

    tables = ['store_user', 'store_typeproduct', 'store_brandproduct', 'store_categoryproduct', 'store_productphotos',
              'store_gender', 'store_product', 'store_infoproduct', 'store_basket', 'store_basketproduct',
              'store_wishlist', 'store_wishlistproduct', 'store_review', 'django_migrations', 'django_content_type',
              'auth_group_permissions', 'auth_permission', 'auth_group', 'store_user_groups',
              'store_user_user_permissions', 'store_brandproduct_categories', 'store_brandproduct_type',
              'store_categoryproduct_brand', 'store_categoryproduct_type', 'store_product_photos', 'django_admin_log',
              'authtoken_token', 'django_session']

    try:

        # Запрос для получения списка таблиц
        # sqlite_cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        # get_tables = [table[0] for table in sqlite_cursor.fetchall()]
        # print(tables)

        with postgresql_connection.cursor() as cursor:
            for table_name in tables:
                print('#' * 50)
                print(table_name)
                print('*' * 50)

                # Извлечение всех строк данных из SQLite
                sqlite_cursor.execute(f"SELECT * FROM {table_name}")
                data_rows = sqlite_cursor.fetchall()
                print('data_rows', data_rows)

                # Запрос для получения списка столбцов выбранной таблицы
                sqlite_cursor.execute(f"PRAGMA table_info ({table_name})")
                columns = [column[1] for column in sqlite_cursor.fetchall()]
                print('columns', columns)

                # Получаем типы столбцов
                cursor.execute(
                    f"SELECT column_name, data_type FROM information_schema.columns  WHERE table_name = '{table_name}'")
                results = cursor.fetchall()

                for row in data_rows:
                    row = list(row)

                    for index, res in enumerate(results):
                        # Проверка типа столбца на "boolean"
                        if res[1] == 'boolean':
                            # Преобразование значения в строку
                            row[index] = str(row[index])

                    print(
                        f"INSERT INTO {table_name} ({', '.join(columns)}) VALUES ({'%s, ' * (len(columns) - 1) + '%s'})",
                        row)

                    # Формируем SQL-запрос для вставки данных в таблицу БД
                    query = f"INSERT INTO {table_name} ({', '.join(columns)}) VALUES ({'%s, ' * (len(columns) - 1) + '%s'})"
                    # Выполняем запрос к БД с нужными параметрами
                    cursor.execute(query, row)

    finally:
        sqlite_cursor.close()
        sqlite_connection.close()
        print("DataBase disconnect")


except Exception as ex:
    # В случае сбоя подключения будет выведено сообщение
    print('Can`t establish connection to database')
    print(ex)
