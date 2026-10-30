import sqlite3

from database import DATABASE_FILE


with sqlite3.connect(DATABASE_FILE) as connection:

    connection.row_factory = sqlite3.Row

    results = connection.execute("""
        SELECT * FROM check_history
        ORDER BY id DESC
    """).fetchall()

    for result in results:
        print(dict(result))