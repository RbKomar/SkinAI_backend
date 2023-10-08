import sqlite3


def initialize_db():
    with sqlite3.connect('../../database_SkinAI.db') as conn:
        c = conn.cursor()

        c.execute('''
        CREATE TABLE users (
            id INTEGER PRIMARY KEY,
            username TEXT UNIQUE NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )''')

        c.execute('''
        CREATE TABLE images (
            id INTEGER PRIMARY KEY,
            user_id INTEGER NOT NULL,
            image_data TEXT NOT NULL,
            description TEXT,
            malignancy_percentage INTEGER,
            FOREIGN KEY(user_id) REFERENCES users(id)
        )''')

        print("Database initialized successfully.")


if __name__ == "__main__":
    initialize_db()
