import sqlite3


def initiate_db():
    connection = sqlite3.connect('telegram.db')
    cursor = connection.cursor()
    cursor.execute(
        '''
        CREATE TABLE IF NOT EXISTS Products(
        id INTEGER PRIMARY KEY,
        title TEXT NOT NULL,
        description TEXT,
        price INTEGER NOT NULL
        )
        ''')
    cursor.execute(
        '''
        CREATE TABLE IF NOT EXISTS Users(
        id INTEGER PRIMARY KEY,
        username TEXT NOT NULL,
        email TEXT NOT NULL,
        age INTEGER NOT NULL,
        balance INTEGER NOT NULL
        )
        ''')
    connection.commit()
    connection.close()


def add_user(username, email, age):
    connection = sqlite3.connect('telegram.db')
    cursor = connection.cursor()
    cursor.execute(f'INSERT INTO Users (username, email, age, balance) VALUES(?, ?, ?, ?)',
                   (username, email, age, '1000'))
    connection.commit()
    connection.close()


def is_included(username):
    connection = sqlite3.connect('telegram.db')
    cursor = connection.cursor()
    check = cursor.execute(
        f'SELECT username FROM Users WHERE username = ?', (username, )).fetchone()
    connection.commit()
    connection.close()
    print(check)
    return check


def get_all_products():
    connection = sqlite3.connect('telegram.db')
    cursor = connection.cursor()
    result = cursor.execute('SELECT * FROM Products').fetchall()
    connection.commit()
    connection.close()
    return result


initiate_db()