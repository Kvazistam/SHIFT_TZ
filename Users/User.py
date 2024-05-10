import sqlite3
from passlib.context import CryptContext



class User:
    """Класс пользователя для более удобного представления данных из бд"""
    def __init__(self, username, password, salary, next_raise_date):
        self.username = username
        self.password = password
        self.salary = salary
        self.next_raise_date = next_raise_date

    def verify_password(self, password):
        return self.password == password

    def as_dict(self):
        return {
            "username": self.username,
            "salary": self.salary,
            "next_raise_date": self.next_raise_date
        }
