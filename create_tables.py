import sqlite3
import pandas as pd

connection = sqlite3.connect("data.db")
cursor = connection.cursor()

create_table = "CREATE TABLE IF NOT EXISTS items (gender int, age int, Category text, amount float, city text, Id INTEGER PRIMARY KEY AUTOINCREMENT)"
cursor.execute(create_table)


df = pd.read_excel('./Data.xlsx')
items = [tuple(v) for v in df.values]


insert_items = "INSERT INTO items (gender, age, Category, amount, city) VALUES (?, ?, ?, ?, ?)"
cursor.executemany(insert_items, items)


connection.commit()

connection.close()
