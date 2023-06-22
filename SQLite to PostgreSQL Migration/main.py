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
                # print('results', results)
                # [print('boolean') for res in results if res[1] == 'boolean']

                for row in data_rows:
                    row = list(row)
                    # print('row', row)

                    for index, res in enumerate(results):
                        if res[1] == 'boolean':  # Проверка типа столбца на "boolean"
                            row[index] = str(row[index])  # Преобразование значения в строку

                    # print('row str', row)

                    # print('columns', columns)
                    # print('results', results)
                    # print('.join(columns)', ', '.join(columns))
                    # print('.join(results[1])', ', '.join(results[1]))
                    print(
                        f"INSERT INTO {table_name} ({', '.join(columns)}) VALUES ({'%s, ' * (len(columns) - 1) + '%s'})",
                        row)
                    query = f"INSERT INTO {table_name} ({', '.join(columns)}) VALUES ({'%s, ' * (len(columns) - 1) + '%s'})"
                    cursor.execute(query, row)

    finally:
        sqlite_cursor.close()
        sqlite_connection.close()
        print("DataBase disconnect")


except Exception as ex:
    # в случае сбоя подключения будет выведено сообщение в STDOUT
    print('Can`t establish connection to database')
    print(ex)

# ------------------------------------------------------------------------------------------------------------------
# Проблемы

# в исходной базе есть зависимости одной таблицы к другой (one to many, many to many)
# то сперва нодо достать все таблицы и сформировть список с корректным расположением таблиц (напр. users)
# чтобы не возникало ошибок при добавлении
# решение -
# Запрос для получения списка таблиц
# sqlite_cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
# get_tables = [table[0] for table in sqlite_cursor.fetchall()]

# так же у sqlite создается таблица - sqlite_sequence, которой в postgresql нету
# решение -
# Проверка
# if table_name[0] == 'sqlite_sequence':
#     continue

# тип boolean в sqlite (0 или 1), а в postgresql (true, false или '0', '1') (есть еще варианты, но расмотрим только эти)
# сперва нужно узнать тип столбца
# your_table - ваша таблица
# cursor.execute(f"SELECT column_name, data_type FROM information_schema.columns  WHERE table_name = 'your_table'")
# results = cursor.fetchall()
# print('results', results)
# ------------------------------------------------------------------------------------------------------------------

