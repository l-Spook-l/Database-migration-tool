## Задача
- При разработке веб сайта golf store (ссылка), возникла необходимость перенести данные из одной БД SQLite в другую SQLite, так как в ходе разработки была изменена структура БД. 
- Затем возникла необходимость переноса проекта на БД PostgreSLQ



## Проблемы в работе с переносом SQLite to PostgreSQL

1. В исходной базе есть зависимости одной таблицы к другой (one to many, many to many).
Сперва нодо достать все таблицы и сформировть список с корректным расположением таблиц (напр. users),
чтобы не возникало ошибок при добавлении
- Решение:
  - Запрос для получения списка таблиц
      ```shell
      sqlite_cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
      get_tables = [table[0] for table in sqlite_cursor.fetchall()]

2. В sqlite создается таблица - sqlite_sequence, которой в postgresql нету
- Решение:
  - Надо сделать проверку
      ```shell
      if table_name[0] == 'sqlite_sequence':
          continue

3. Тип boolean в sqlite (0 или 1), а в postgresql (true, false или '0', '1') (есть еще варианты, но расмотрим только эти)
- Решение
  - Сперва нужно узнать тип столбца
     ```shell
     # your_table - ваша таблица
     cursor.execute(f"SELECT column_name, data_type FROM information_schema.columns  WHERE table_name = 'your_table'")
     results = cursor.fetchall()
    
  - Затем при переборе столбцов
     ```shell
     for row in data_rows:
         row = list(row)
    
  - Делать проверку
    ```shell
     for index, res in enumerate(results):
         # Проверка типа столбца на "boolean"
         if res[1] == 'boolean':  
             # Преобразование значения в строку
             row[index] = str(row[index])  