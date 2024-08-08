import os
import sqlite3


def init_db(db_file_name):
    connection = sqlite3.connect(db_file_name)
    cursor = connection.cursor()

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS Products(
        id INTEGER PRIMARY KEY,
        title TEXT NOT NULL,
        description TEXT NOT NULL,
        price INTEGER
        );
        """
    )

    cursor.execute(
        """
        CREATE INDEX IF NOT EXISTS idx_title ON Products (title);
        """
    )

    for i in range(1, 5):
        cursor.execute(
            "INSERT INTO Products (title, description, price) VALUES (?, ?, ?);",
            (f"Product {i}", f"описание {i}", f"{i * 100}"),
        )

    connection.commit()
    connection.close()


def get_data(db_file_name):
    connection = sqlite3.connect(db_file_name)
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT * FROM Products;
        """
    )
    products = cursor.fetchall()
    connection.close()
    return products


def get_all_products():
    db_file_name = "../../../Downloads/product_telegram.db"
    if not os.path.exists(db_file_name):
        init_db(db_file_name)
    return get_data(db_file_name)
