## Task
- During the development of the golf store website (link), there was a need to migrate data from one SQLite database to another SQLite database due to changes in the database structure.
- Then there was a need to migrate the project to a PostgreSQL database

## Challenges in SQLite to PostgreSQL Migration

1. In the original database, there are dependencies between tables (one-to-many, many-to-many).
- Solution:
  - To retrieve all tables and create a list with the correct table order (e.g., users) to avoid errors during insertion:
      ```shell
      sqlite_cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
      get_tables = [table[0] for table in sqlite_cursor.fetchall()]

2. SQLite creates the 'sqlite_sequence' table, which does not exist in PostgreSQL.
- Solution:
  - Perform a check:
      ```shell
      if table_name[0] == 'sqlite_sequence':
          continue

3. The boolean type in SQLite is represented as 0 or 1, while in PostgreSQL it is represented as true, false, or '0', '1' (there are other variations, but let's consider these).
- Solution
  - First, determine the column type:
     ```shell
     # your_table - your table
     cursor.execute(f"SELECT column_name, data_type FROM information_schema.columns  WHERE table_name = 'your_table'")
     results = cursor.fetchall()
    
  - Then, when iterating over rows:
     ```shell
     for row in data_rows:
         row = list(row)
    
  - Perform the type check:
    ```shell
     for index, res in enumerate(results):
         # Check if the column type is "boolean"
         if res[1] == 'boolean':  
             # Convert the value to a string
             row[index] = str(row[index])  