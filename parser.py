import requests
import dateparser
import json
import re

from datetime import date, timedelta, datetime
from bs4 import BeautifulSoup as bs


# Качаем сайт

# news = {'title': --,
#         'url': --
#         'date': --,
#         'text': --}



def simple_parser(url: str, iteration: int = 5):
    one_day = timedelta(days=1)

    if re.search(r'\d+', url) is not None:
        last_date = re.search(r'\d+', url).group(0)
        news_day = datetime.strptime(last_date, '%Y%m%d') - one_day
        url = 'https://ria.ru/economy/'
    else:
        news_day = date.today()

    formatted_date = news_day.strftime('%Y%m%d')
    news_list = []
    for i in range(iteration):

        result = requests.get(url + formatted_date)

        try:
            if result.status_code != 200:
                raise Exception('Не удалось получить страницу')
        except Exception:
            print(f'Такой даты нет {formatted_date}')
            news_day = news_day - one_day
            formatted_date = news_day.strftime('%Y%m%d')
            continue

        page_text = result.text
        page_soup = bs(page_text, features='lxml')
        articles_list = page_soup.find_all('div', class_='list-item')
        # TODO: Сделать, чтобы парсило со всех страниц (разбей на ф-ции)
        for article_block in articles_list:
            article_href = article_block.find('a', class_='list-item__title')
            # Название статьи
            article_title = article_href.text
            # Сслыка
            article_url = article_href.get('href')
            # Дата
            article_date = article_block.find(class_="list-item__date")
            article_date = dateparser.parse(article_date.text, languages=['ru'])
            # Теги
            article_tags = article_block.find_all("a", class_="list-tag__text")
            article_tags = json.dumps([tag.text for tag in article_tags]).encode('utf8')
            # Текст
            article_text = parse_page(article_url)

            news_list.append({'title': article_title, 'url': article_url, "tags": article_tags, "date": article_date,
                              "text": article_text, 'last_url': url + formatted_date})
        print(news_list)
        news_day = news_day - one_day
        formatted_date = news_day.strftime('%Y%m%d')

    return news_list


def parse_page(url):
    page_response = requests.get(url)
    page_text = page_response.text
    page_soup = bs(page_text, features='lxml')
    article_text_blocks = page_soup.find_all("div", class_="article__text")
    article_text = ''.join([text_block.text for text_block in article_text_blocks])
    return article_text

if __name__ == '__main__':
    simple_parser('https://ria.ru/economy/')