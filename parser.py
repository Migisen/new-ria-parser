import requests
from datetime import date, timedelta
from bs4 import BeautifulSoup as bs

# Качаем сайт
url = 'https://ria.ru/economy/'
news_list = []
# news = {'title': --,
#         'url': --
#         'date': --,
#         'text': --}
# TODO: Переделать в ф-цию, на вход основная ссылка и кол-во итераций на выход список статей
news_day = date.today()
formated_day = news_day.strftime('%Y%m%d')
one_day = timedelta(days=1)

for i in range(10):

    result = requests.get(url + formated_day)

    try:
        if result.status_code != 200:
            raise Exception('Не удалось получить страницу')
    except Exception:
        print(f'Такой даты нет {formated_day}')
        news_day = news_day - one_day
        formated_day = news_day.strftime('%Y%m%d')
        continue

    page_text = result.text
    page_soup = bs(page_text, features='lxml')
    articles_list = page_soup.find_all('div', class_='list-item')
    for article_block in articles_list:
        # TODO: добавить время статьи и теги
        article_href = article_block.find('a', class_='list-item__title')
        article_title = article_href.text
        article_url = article_href.get('href')
        news_list.append({'title': article_title, 'url': article_url})
    print(news_list)
    news_day = news_day - one_day
    formated_day = news_day.strftime('%Y%m%d')

print(news_list)

print("Arigato")