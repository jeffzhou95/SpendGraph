import sqlite3
import pandas as pd

connection = sqlite3.connect("data.db")
cursor = connection.cursor()

# create_table = "CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username text, password text)"
# cursor.execute(create_table)

create_table = "CREATE TABLE IF NOT EXISTS items (email text, firstName text, lastName text, institution text, department text, street text, city text, state text, zipCode text, country text, officePhone text, mobilePhone text, website text, topic text, twitter text, facebook text, requirements text, needs text, M text, D text, Y text, Id INTEGER PRIMARY KEY AUTOINCREMENT)"
cursor.execute(create_table)


df = pd.read_excel('./temp.xlsx')
items = [tuple(v) for v in df.values]
insert_items = "INSERT INTO items (email, firstName, lastName, institution, department, street, city, state, zipCode, country, officePhone, mobilePhone, website, topic, twitter, facebook, requirements, needs, M, D, Y) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"
cursor.executemany(insert_items, items)

make_notnull = "UPDATE items SET firstName=COALESCE(firstName,''), lastName=COALESCE(lastName, ''), email=COALESCE(email, ''), topic=COALESCE(topic, ''), institution=COALESCE(institution, '')"
cursor.execute(make_notnull)

connection.commit()

connection.close()
