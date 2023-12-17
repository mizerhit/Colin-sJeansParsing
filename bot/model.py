import psycopg2
import requests
from bs4 import BeautifulSoup
import json

class DataAccessObject:
    __instance = None
    
    def __init__(self):
        if DataAccessObject.__instance is not None:
            raise Exception("This class is a singleton!")
        else:
            DataAccessObject.__instance = self
            self.__instance = psycopg2.connect(
                host="db",
                user="root", 
                password="root",
                port="5432",
                dbname="things"
            )
            self.__cursor = self.__instance.cursor()
            self.__create_tables()

    def __enter__(self):
        return self

    def __exit__(self):
        self.__instance.close()
        
    def __del__(self):
        self.__instance.close()

    def __create_tables(self):
        
        self.__cursor.execute('''
            CREATE TABLE IF NOT EXISTS Things (
                thing TEXT NOT NULL,
                color TEXT NOT NULL,
                price INTEGER,
                discount INTEGER,
                ref_photo TEXT NOT NULL PRIMARY KEY
            )
        ''')
        self.__instance.commit()

    def save_thing(self, name, colour, price, discount, ref_photo):
        sql = 'INSERT INTO Things (thing, color, price, discount, ref_photo) VALUES (%s, %s, %s, %s, %s) ON CONFLICT (ref_photo) DO UPDATE SET thing = EXCLUDED.thing'
        thing = (name, colour, price, discount, ref_photo)
        self.__cursor.execute(sql, thing)
        self.__instance.commit()

    def get_things(self):
        self.__cursor.execute('SELECT thing FROM Things')
        return self.__cursor.fetchall()

    def get_thing(self, name):
        self.__cursor.execute('SELECT * FROM Things WHERE thing = %s', (name,))
        return self.__cursor.fetchall()

    def get_discount(self):
        self.__cursor.execute('SELECT thing, color, price, discount FROM Things ORDER BY discount DESC')
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
                discount = int(discount)
                price = thing_data.get("price", "")
                dot_pos = price.find('.')
                price = int(price[0: dot_pos])
                colour = thing_data.get("variant", "")
                ref_photo = data.find('img')['data-original']
                self.save_thing(name, colour, price, discount, ref_photo)