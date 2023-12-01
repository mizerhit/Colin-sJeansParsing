import sqlite3
import requests
from bs4 import BeautifulSoup
import json

class DataAccessObject:
    __instance = None

    def __init__(self):
        self.__instance = sqlite3.connect('db.sqlite3')
        self.__cursor = self.__instance.cursor()
        self.__create_tables()
    
    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
            cls.__instance.__instance = sqlite3.connect('db.sqlite3', check_same_thread=False)
            cls.__instance.__cursor = cls.__instance.__instance.cursor()
            cls.__instance.__create_tables()
        return cls.__instance

    def __del__(self):
        self.__instance.close()
        self.__instance = None

    def __create_tables(self):
        self.__cursor.execute('''
            CREATE TABLE IF NOT EXISTS Things (
                thing TEXT NOT NULL,
                color TEXT NOT NULL,          
                price INTEGER,
                discount INTEGER
            )
        ''')
        self.__instance.commit()

    def save_thing(self, name, colour, price, discount):
        self.__cursor.execute('INSERT OR REPLACE INTO Things (thing, color, price, discount) VALUES (?, ?, ?, ?)',
                              (name, colour, price, discount))
        self.__instance.commit()

    def get_things(self):
        self.__cursor.execute('SELECT thing FROM Things')
        return self.__cursor.fetchall()

    def get_thing(self, name):
        self.__cursor.execute('SELECT * FROM Things WHERE thing = ?', (name,))
        return self.__cursor.fetchall()

    def get_discount(self):
        self.__cursor.execute('SELECT * FROM Things ORDER BY discount DESC')
        return self.__cursor.fetchall()
    
    def DataUpdate(self):
        url = "https://www.colins.ru/c/muzh-2?specs=7"
        response = requests.get(url)

        if response.status_code == 200:

            soup = BeautifulSoup(response.text, 'lxml')

            all_data = soup.findAll('div', class_='productCartMain')

            for data in all_data:
                div = data.div
                thing_data = json.loads(div.attrs["data-ga"])
                name = thing_data.get("name", "")
                discount = thing_data.get("discount", "")
                price = thing_data.get("price", "")
                colour = thing_data.get("variant", "")
                self.save_thing(name, colour, price, discount)

db = DataAccessObject()
db.DataUpdate()
print(db.get_discount())
print()
print()
print()
print(db.get_things())