import requests
import time
import csv
from bs4 import BeautifulSoup


url = 'http://www.mojgorod.ru/cities/listcity.html'


def start(html):
    soup = BeautifulSoup(html, 'lxml')
    list_cities_href = soup.find('body').find_next(
        'table').find_next('table').find_next('td').find_next('td')

    for index, url in enumerate(list_cities_href.find_all('a')):
        col1, col2, col3, col4 = [], [], [], []

        r_card_city = requests.get(url['href'])
        soup_card = BeautifulSoup(r_card_city.content, 'lxml')

        card_table = soup_card.find('table').find_next('table').find('tr')
        card_table_count_people = card_table.find_all('table')[-1]

        name_city = card_table.find('h2').text
        name_region = card_table.find('h3').find('a').text

        print('Обработка ' + name_city)

        for idx, t in enumerate(card_table_count_people.find_all('tr')):
            if idx == 0:
                continue

            all_td = t.find_all('td')

            col1.append([all_td[0].text, all_td[1].text])
            col2.append([all_td[2].text, all_td[3].text])
            col3.append([all_td[4].text, all_td[5].text])
            col4.append([all_td[6].text, all_td[7].text])

        with open('cities.csv', 'a', newline='') as csvfile:
            csvwriter = csv.writer(csvfile, delimiter=';')

            for col in col1:
                csvwriter.writerow([name_city, name_region, col[0], col[1]])

            for col in col2:
                csvwriter.writerow([name_city, name_region, col[0], col[1]])

            for col in col3:
                csvwriter.writerow([name_city, name_region, col[0], col[1]])

            for col in col4:
                csvwriter.writerow([name_city, name_region, col[0], col[1]])

        time.sleep(0.05)


def get_html():
    return requests.get(url).content


if __name__ == '__main__':
    start(get_html())
