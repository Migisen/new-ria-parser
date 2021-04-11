import requests
from datetime import date, timedelta
from bs4 import BeautifulSoup as bs


# Качаем сайт

# TODO: Переделать в ф-цию, на вход основная ссылка и кол-во итераций на выход список статей


def simple_parser(url, iteration):
    news_list = []
    news_day = date.today()
    formated_day = news_day.strftime('%Y%m%d')
    one_day = timedelta(days=1)

    for i in range(iteration):

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
            article_date = article_block.find(class_="list-item__date")
            article_time = article_date.text
            article_date = news_day.strftime('%Y%m%d') + " " + article_time[-5:]  # извлекаем время
            article_tags = article_block.find_all("a", class_="list-tag__text")
            article_tag = []
            for article_tag_block in article_tags:
                article_tag.append(article_tag_block.text)

            result = requests.get(article_url)
            page_text = result.text
            page_soup = bs(page_text, features='lxml')
            article_text_blocks = page_soup.find_all("div", class_="article__text")
            article_text = str()
            for article_text_block in article_text_blocks:
                article_text += article_text_block.text + ""

            news_list.append({'title': article_title, 'url': article_url, "tags": article_tag, "date": article_date,
                              "text": article_text})
        print(news_list)
        news_day = news_day - one_day
        formated_day = news_day.strftime('%Y%m%d')

    return news_list


simple_parser('https://ria.ru/economy/', 10)
