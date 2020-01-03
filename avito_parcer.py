import requests
from bs4 import BeautifulSoup
import csv

headers = {'accept': '*/*',
           'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 '
                         '(KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36 OPR/64.0.3417.92'}

base_url = f'https://www.avito.ru/moskva?q=bmw&p=1'


def avito_parcer(base_url, headers):
    session = requests.Session()
    request = session.get(base_url, headers=headers)
    cars = []
    soup = BeautifulSoup(request.content, 'lxml')
    divs = soup.find_all('div', attrs={'class': 'description item_table-description'})
    for div in divs:
        title = div.find('h3', attrs={'class': 'snippet-title'}).text.strip()
        price = div.find('span', attrs={'data-marker': 'item-price'}).text.strip()
        description = div.find('div', attrs={'data-marker': 'item-specific-params'}).text.strip()
        time = div.find('div', attrs={'data-marker': 'item-date'}).text.strip()
        absolute_time1 = div.find('div', attrs={'class': 'item-date'}).div['data-absolute-date'].split()[0]
        absolute_time2 = div.find('div', attrs={'class': 'item-date'}).div['data-absolute-date'].split()[1].split(':')[0][1]
        absolute_time = absolute_time1 + ' в ' + absolute_time2 + ' часов'
        if absolute_time1 == 'Сегодня' and absolute_time2 == '9':
            cars.append({
                'title': title,
                'price': price,
                'description': description,
                'time': absolute_time
            })
    return cars


def csv_writer(cars):
    with open('parced_bmw_avito.csv', 'w') as file:
        writer = csv.writer(file)
        writer.writerow(('Машина', 'Цена', 'Описание', 'Время'))
        for car in cars:
            writer.writerow((car['title'], car['price'], car['description'], car['time']))


cars = avito_parcer(base_url, headers)
csv_writer(cars)

