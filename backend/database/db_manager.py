import os
import sqlite3
from typing import Optional

from models.user import User

DATABASE = 'database_SkinAI.db'
IMAGE_STORAGE_PATH = "images/"


# ------------------ User related functions ------------------
def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


def insert_user(user):
    conn = get_db_connection()
    tables = conn.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='users';").fetchall()
    print(f"Tables: {tables}")
    cursor = conn.cursor()

    cursor.execute('''
    INSERT INTO users (username, email, password)
    VALUES (?, ?, ?)
    ''', (user.username, user.email, user.password))

    conn.commit()
    conn.close()


def get_user_by_username(username: str) -> Optional[User]:
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM users WHERE username = ?', (username,))
    user_row = cursor.fetchone()

    conn.close()

    if user_row:
        return User(
            id=user_row[0],
            username=user_row[1],
            email=user_row[2],
            password=user_row[3],
        )
    else:
        return None


def get_all_users():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    try:
        cursor.execute("SELECT * FROM users")
        return cursor.fetchall()
    except sqlite3.Error as e:
        print(f"Error fetching all users: {e}")
    finally:
        conn.close()


def update_user_in_db(updated_user):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    try:
        cursor.execute(
            "UPDATE users SET email = ?, password = ? WHERE username = ?",
            (updated_user.email, updated_user.password, updated_user.username)
        )
        conn.commit()
    except sqlite3.Error as e:
        print(f"Error updating user {updated_user.username}: {e}")
    finally:
        conn.close()


def delete_user_from_db(username):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    try:
        cursor.execute("DELETE FROM users WHERE username = ?", (username,))
        conn.commit()
    except sqlite3.Error as e:
        print(f"Error deleting user {username}: {e}")
    finally:
        conn.close()


# ------------------ Image related functions ------------------
def save_image_to_disk(image_data, filename):
    file_path = os.path.join(IMAGE_STORAGE_PATH, filename)
    with open(file_path, "wb") as f:
        f.write(image_data)
    return file_path


def insert_image(image_data: dict, user_id: int) -> None:
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute('''
    INSERT INTO images (user_id, image_path, description, malignancy_percentage)
    VALUES (?, ?, ?, ?)
    ''', (user_id, image_data['image_path'], image_data['description'], image_data['malignancy_percentage']))

    conn.commit()
    conn.close()
