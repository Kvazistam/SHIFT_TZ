import sqlite3

from Users.User import User

# В файле находятся функции для взаимодействия с базой данных, в основном используются для отладки и юнит тестов


def get_user(username, table="users"):
    """Находит пользователя в users.db и возвращает объект класса User"""
    conn = sqlite3.connect('users.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM {table} WHERE username = ?", (username,))
    user_record = cursor.fetchone()
    conn.close()
    if user_record:
        return User(user_record['username'], user_record['password'], user_record['salary'],
                    user_record['next_raise_date'])
    return None


def create_user(username, password, salary, next_raise_date, table="users"):
    """Создает пользователя в users.db с переданными параметрами"""
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute(f"INSERT INTO {table} (username, password, salary, next_raise_date) VALUES (?, ?, ?, ?)",
                   (username, password, salary, next_raise_date))
    conn.commit()
    conn.close()


def delete_user(username, table="users" ):
    """Удаляет пользователя в users.db"""
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute(f"DELETE FROM {table} WHERE username = ?", (username))
    conn.commit()
    conn.close()


def update_user(username, password=None, salary=None, next_raise_date=None,  table="users"):
    """Обновляет данные пользователя в users.db"""
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()

    cursor.execute(f"UPDATE {table} SET password = ? WHERE username = ?", (table, password, username))
    if salary:
        cursor.execute(f"UPDATE {table} SET salary = ? WHERE username = ?", (table, salary, username))
    if next_raise_date:
        cursor.execute(f"UPDATE {table} SET next_raise_date = ? WHERE username = ?", (table, next_raise_date, username))
    conn.commit()
    conn.close()
