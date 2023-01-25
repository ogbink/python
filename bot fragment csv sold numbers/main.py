from bs4 import BeautifulSoup
import requests
import os.path

if os.path.exists('phones.csv') == False:
    with open('phones_2.csv','w') as file:
        file.write('Номер телефона,Цена\n')


## делаем первый запрос чтобы получить список номеров которые будем пропускать
old_numbers = []
response = requests.get('https://fragment.com/numbers?sort=ending&filter=sold') # можно изменить url на другой фильтр
soup = BeautifulSoup(response.text, 'html.parser')
numbers = soup.select('tr.tm-row-selectable')
for number in numbers:
    phone = number.select_one('div.table-cell-value.tm-value').text.replace(' ','')
    price = number.select_one('div.table-cell-value.tm-value.icon-before.icon-ton').text
    with open('phones_2.csv','a') as file:
        file.write(f'{phone},{price} TON\n')
###