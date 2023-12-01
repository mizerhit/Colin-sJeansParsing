import sqlite3

class DataAccessObject:
    __instance = None

    def __init__(self):
        self.__instance = sqlite3.connect('db.sqlite3')
        self.__cursor = self.__instance.cursor()
        self.__create_tables()
    
    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
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
        self.__cursor.execute('''
            SELECT thing FROM Things
        ''')
        return self.__cursor.fetchall()
    
    def get_thing(self, name):
        self.__cursor.execute('SELECT * FROM Things WHERE thing = ?', (name,))
        return self.__cursor.fetchall()
    
    def get_discount(self):
        self.__cursor.execute('SELECT * FROM Things ORDER BY discount DESC')
        return self.__cursor.fetchall()
