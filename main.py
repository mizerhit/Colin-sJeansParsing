import requests
from bs4 import BeautifulSoup
import DataBase as db
import json

database = db.DataAccessObject()

url = "https://www.colins.ru/c/muzh-2?specs=7"

response = requests.get(url)
def UpdateData():
    if response.status_code == 200:

        soup = BeautifulSoup(response.text, 'lxml')
        title = soup.title.text

        all_data = soup.findAll('div', class_='productCartMain')

        for data in all_data:
            div = data.div
            thing_data = json.loads(div.attrs["data-ga"])
            name = thing_data.get("name", "")
            discount = thing_data.get("discount", "")
            price = thing_data.get("price", "")
            colour = thing_data.get("variant", "")
            database.save_thing(name, colour, price, discount)
    else:
        print(f"Faile, status code: {response.status_code}")