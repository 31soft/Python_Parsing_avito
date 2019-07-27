#go!
import requests
from bs4 import BeautifulSoup
import csv

def get_html(url):
    r = requests.get(url)
    return r.text

def get_total_pages(html):
    soup = BeautifulSoup(html, 'lxml')
    soup.encode("utf-8")
    pages = soup.find('div', class_='pagination-pages').find_all('a', class_='pagination-page')[-1].get('href')
    total_pages = pages.split('=')[1].split('&')[0]
    return int(total_pages)

def write_csv(data):
    with open('avito.csv', 'a', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow((data['title'],
                         data['address'],
                         data['price'],
                         data['url']
                         ))

def get_page_data(html):
    soup = BeautifulSoup(html, 'lxml')
    ads = soup.find('div', class_='catalog-list').find_all('div', class_='item_table')
    for ad in ads:
        try:
            title = ad.find('div', class_='description').find_all('h3')[0].text.strip()
        except:
            title = ''
        try:
            address = ad.find('div', class_='description').find_all('address').text.strip()
        except:
            address = ''
        try:
            price = ad.find('div', class_='about').text.strip();
        except:
            price = ''
        try:
            url = 'https://avito.ru' + ad.find('div', class_='description').find('h3').find('a').get('href')
        except:
            url = ''
        data = {'title': title,
                'address': address,
                'price': price,
                'url': url}
        write_csv(data)



def main():
    url = 'https://www.avito.ru/belgorod/doma_dachi_kottedzhi?q=Северный'

    base_url = 'https://www.avito.ru/belgorod/doma_dachi_kottedzhi?'
    page_part = 'p='
    query_part = 'q=Северный'

    total_pages = get_total_pages(get_html(url))
    for i in range(1, total_pages):
        url_gen = base_url + page_part + str(i) + query_part
        html = get_html(url_gen)
        get_page_data(html)

if __name__ == '__main__':
    main()
