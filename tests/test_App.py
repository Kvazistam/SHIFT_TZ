import sqlite3
import pytest
from fastapi.testclient import TestClient
from main import app
from Users.User import User
from App.App import authenticate_user




class TestUM:

    def setup_class(cls):
        print("aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAa")
        cls.database = './users.db'
        cls.table = 'test'
        cls.date = "01.01.2024"
        cls.salary = "1000"
        cls.password = "test_password"
        cls.username = "test_username"
        cls.client = TestClient(app)
        conn = sqlite3.connect(cls.database)
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name=?", ("test",))
        result = cursor.fetchone()
        if result is None:
            cursor.execute("CREATE TABLE test(id INTEGER PRIMARY KEY, "
                           "username TEXT NOT NULL,"
                           "password TEXT  NOT NULL,"
                           "salary REAL NOT NULL,"
                           "next_raise_date TEXT NOT NULL);")
        cursor.execute(
            "INSERT INTO test(username, password, salary, next_raise_date) VALUES(?, ?, "
            "?, ?);", (cls.username, cls.password, cls.salary, cls.date))
        conn.commit()
        conn.close()

    def teardown_class(cls):
        print("b")
        conn = sqlite3.connect(cls.database)
        cur = conn.cursor()
        try:
            cur.execute("DROP TABLE IF EXISTS test;")
            conn.commit()
            print("Таблица успешно удалена")
        except sqlite3.Error as e:
            print(f"Ошибка при удалении таблицы: {e}")
        finally:
            conn.close()

    def test_authenticate_user(self):
        user = authenticate_user(self.username, self.password, table=self.table)
        if not user:
            print("true user has not been authenticated")
        false_user = authenticate_user(self.username, "ayayayayaya", table=self.table)
        if false_user:
            print("false_user has been authenticated")
        assert isinstance(user, User)
        assert not false_user

    def test_get_token(self):
        response = self.client.post("/token", params={"table": "test"}, data={"username": self.username, "password": self.password})
        assert response.status_code == 200
        assert "access_token" in response.json()
        assert response.json()["token_type"] == "bearer"

    def test_get_token_fail(self):
        response = self.client.post("/token", params={"table": "test"}, data={"username": self.username, "password": "ayayayaya"})
        assert response.status_code == 401

    def test_read_salary_authenticated(self):
        login_response = self.client.post("/token", params={"table": "test"}, data={"username": "test_username", "password": "test_password"})
        token = login_response.json()["access_token"]
        response = self.client.get("/salary", headers={"Authorization": f"Bearer {token}"}, params={"table":self.table})
        assert response.status_code == 200
        assert "salary" in response.json() and "next_raise_date" in response.json()

    def test_read_salary_unauthenticated(self):
        response = self.client.get("/salary")
        assert response.status_code == 401
