import sqlite3

from faker import Faker

from app.config import DATABASE


def generate_mock_users(cursor, num_users=10):
    fake = Faker()

    for _ in range(num_users):
        username = fake.user_name()
        email = fake.email()
        password = fake.password(length=12)  # Adjust length as needed
        cursor.execute(
            "INSERT INTO users (username, email, password) VALUES (?, ?, ?)",
            (username, email, password),
        )


def initialize_db(mock_users_count=None):
    with sqlite3.connect(DATABASE) as conn:
        c = conn.cursor()

        c.execute(
            """
        CREATE TABLE users (
            id INTEGER PRIMARY KEY,
            username TEXT UNIQUE NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )"""
        )

        c.execute(
            """
        CREATE TABLE images (
            id INTEGER PRIMARY KEY,
            user_id INTEGER NOT NULL,
            image_path TEXT NOT NULL,
            description TEXT,
            malignancy_percentage INTEGER,
            FOREIGN KEY(user_id) REFERENCES users(id)
        )"""
        )

        if mock_users_count:
            generate_mock_users(c, mock_users_count)

        conn.commit()

        print("Database initialized successfully.")


if __name__ == "__main__":
    # For example, to initialize the database with 20 mock users:
    initialize_db(mock_users_count=20)
