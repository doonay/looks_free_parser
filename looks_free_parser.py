import requests
from bs4 import BeautifulSoup
import json
import sys

session = requests.Session()
headers = {
    'authority': 'hub.virtamate.com',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-language': 'ru,en;q=0.9,en-GB;q=0.8,en-US;q=0.7',
    'cache-control': 'max-age=0',
    'cookie': 'vamhubconsent=yes',
    'referer': 'https://hub.virtamate.com/resources/categories/scenes.6/',
    'sec-ch-ua': '"Microsoft Edge";v="119", "Chromium";v="119", "Not?A_Brand";v="24"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'same-origin',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36 Edg/119.0.0.0',
}
    
def get_pagination(url):
    session = requests.Session()
    r = session.get(url, headers=headers)
    soup = BeautifulSoup(r.text, 'lxml')
    navs = soup.find('ul', {'class': 'pageNav-main'}).find_all('li')
    pages = int(navs[-1].get_text())
    return pages

def main(url, pages):
    links = []
    for page in range(1, pages+1, 1):
        url = f'https://hub.virtamate.com/resources/categories/looks.7/?order=rating_weighted&direction=desc&page={page}'
        print(f'Parse page {page}/{pages}')

        headers = {
        'cookie': 'vamhubconsent=yes' #добавил укороченные хэдеры! проверить!
        }

        try:
            r = session.get(url, headers=headers) #хэдэры не убирать!!! даже с сессией требуется кук доступа 18+
            soup = BeautifulSoup(r.text, 'lxml')
            items = soup.find('div', {'class': ['structItemContainer']}).find_all('div', {'class': ['structItem', 'structItem--resource', 'is-prefix3', 'js-inlineModContainer']})
            for item in items:
                link = f'https://hub.virtamate.com{item.find("a", {"data-tp-primary": "on"}).get("href")}'
                links.append(link)
        except:
            print('Какая то ошибка запроса. Обработать!')
        '''
        with open('links_temp.txt', 'a', encoding='utf-8') as file:
            file.write(f"{item.get('data-author')}\n")
        '''

    """
    ТУТ ВЫЗЫВАЕМ МЕТОДЫ ОРМ ВМЕСТО ЗАПИСИ В ФАЙЛ
    """
    with open('links.txt', 'a', encoding='utf-8') as file:
        for link in links:
            file.write(f"{link}\n")

def get_file_links():
    headers = {
        'cookie': 'vamhubconsent=yes'
        }
    page_links = []
    with open('links.txt', 'r', encoding='utf-8') as file:
        for line in file:
            page_links.append(line.strip())
    download_links = []
    for page_url in page_links:
        r = session.get(page_url, headers=headers)
        soup = BeautifulSoup(r.text, 'lxml')
        a = soup.find('div', {'class': ['p-title-pageAction']}).find('a')

        '''важный момент!!!
        есть три типа ссылок

        <a class="button--cta button button--icon button--icon--download" href=".*" target="_blank">
            <span class="button-text">Download</span>
        </a>
        <a class="button--cta button button--icon button--icon--download" data-xf-click="overlay" href=".*" target="_blank">
            <span class="button-text">Download</span>
        </a>
        <a class="button--cta button button--icon button--icon--redirect" data-xf-init="tooltip" href=".*" rel="noopener" target="_blank" title="mega.nz">
            <span class="button-text">Go to download</span>
        </a>

        итоговая ссылка выглядит одинаково, однако она либо прямая, либо на доп страницу, либо редиректная, для дальнейшей обработки это нужно указывать
        '''

        if a.get('data-xf-click') == "overlay":
            overlay = 'overlay'
            href_string = f'{overlay} {a.get('href')}'
        elif a.get('data-xf-init') == "tooltip":
            site = a.get('title')
            href_string = f'{site} {a.get('href')}'
        else:
            print(f'https://hub.virtamate.com{href}')
            download_links.append(f'https://hub.virtamate.com{href}')

    with open('download_links.txt', 'a', encoding='utf-8') as file:
        for download_link in download_links:
            file.write(f"{download_link}\n")
    
    

if __name__ == '__main__':
    url = 'https://hub.virtamate.com/resources/categories/looks.7/'
    #url = 'https://hub.virtamate.com/resources/categories/scenes.3/'
    pages = get_pagination(url)
    print('pages:', pages)
    #main(url, pages)
    #print('links.txt is done!')
    #---
    print('далее достаём все ссылки на скачку')
    get_file_links()