import sqlite3


class DataBase:
    def __init__(self):
        self._db = sqlite3.connect("data.db")
        self._cursor = self._db.cursor()

        self._cursor.execute("""CREATE TABLE IF NOT EXISTS data (
            date TEXT,
            park INTEGER,
            habr INTEGER,
            che1 INTEGER,
            che2 INTEGER,
            izml INTEGER
        )""")
        self._db.commit()

    def execute(self, args: str):
        self._cursor.execute(args)
        fetch = self._cursor.fetchall()
        self._db.commit()
        return fetch

    def new_data(self, data: dict):
        self._cursor.execute(
            "INSERT INTO data VALUES(?, ?, ?, ?, ?, ?)",
            (data["date"], data["park"], data["habr"], data["che1"], data["che2"], data["izml"])
        )
        self._db.commit()

    def search_data(self, date0: dict, date1: dict):
        self._cursor.execute("SELECT * FROM data")
        fetch = self._cursor.fetchall()
        result = []
        for data in fetch:
            date = data[0].split(":")
            date = {"day": int(date[0]), "moonth": int(date[1])}
            if date["moonth"] >= date0["moonth"] and date["moonth"] <= date1["moonth"]:
                if date["day"] >= date0["day"] and date["day"] <= date1["day"]:
                    result.append(data)
        return result