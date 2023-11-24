import requests
from bs4 import BeautifulSoup

url = "https://www.colins.ru/c/muzh-2?specs=7"

response = requests.get(url)

if response.status_code == 200:

    soup = BeautifulSoup(response.text, 'lxml')
    title = soup.title.text

    all_data = soup.findAll('div', class_='productCartMain')

    for data in all_data:
        div = data.div
        thing = div.attrs["data-ga"]
        str(thing)

        name_pos = thing.find('"name"')
        discount_pos = thing.find('"discount"')
        price_pos = thing.find('"price"')
        category_pos = thing.find('"category"')
        variant_pos = thing.find('"variant"')
        quantity_pos = thing.find('"quantity"')

        name = thing[(name_pos + 7):(discount_pos - 1)]
        discount = thing[(discount_pos + 11):(price_pos - 1)]
        price = thing[(price_pos + 8):(category_pos - 1)]
        variant = thing[(variant_pos + 10):(quantity_pos - 1)]

        print("________________________________________________________________________________________________________________________________")
        print(name)
        print(discount)
        print(price)
        print(variant)
else:
    print(f"Faile, status code: {response.status_code}")
