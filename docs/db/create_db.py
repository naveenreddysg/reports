import sqlite3

connection = sqlite3.connect('data.db')
cursor = connection.cursor()

create_table =  """
    CREATE TABLE users(
        id varchar(30) primary key,
        name varchar(50),
        password varchar(50)
    )
"""
print(create_table)
cursor.execute(create_table)
connection.commit()
connection.close()