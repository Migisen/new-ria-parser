import sqlite3
import multiprocessing
import os

from bs4 import BeautifulSoup as bs
import requests
import dateparser

class RiaParser:
    def __init__(self, target_url: str, db_name: str) -> None:
        self.__temp_path = './last_url.tmp'
        self._headers = {
            'User-Agent': r'Mozilla/5.0 (X11; Linux aarch64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.188 Safari/537.36 CrKey/1.54.250320'
        }
        self._ria_url = 'https://ria.ru'
        self._session = RiaParser.create_session(self._headers)
        self._db_name = db_name
        self.target_url = target_url
        if os.path.exists(self.__temp_path):
            with open(self.__temp_path, 'r') as f:
                self.next_url = f.read()
        else:
            self.next_url = target_url


    def start_parsing(self):
        while True:
            try:
                page = self.parse_page(self.next_url)
                news_data = self.get_labels(page)
                self.commit_to_db(news_data)
            except Exception:
                print('Press F, retrying')
                with open('last_url.tmp', 'w') as f:
                    f.write(self.next_url)

    def parse_page(self, url: str) -> str:
        page = self._session.get(url)
        page.raise_for_status()
        return page.text

    def get_labels(self, page: str):
        page_soup = bs(page, features='lxml')
        try:
            self.next_url = self._ria_url + page_soup.find('div',{'class': 'list-items-loaded'})['data-next-url']
        except TypeError:
            self.next_url = self._ria_url + page_soup.find('div', {'class': 'list-more'})['data-url']
        news_items = page_soup.find_all('div', {'class': 'list-item'})
        news_strings = [(str(news_item)) for news_item in news_items]
        # articles_results = []
        with multiprocessing.Pool(4) as pool:
            # for article in news_items:
                # article_information = self.extract_information(article)
                # articles_results.append(article_information)
            articles_results = pool.map(self.extract_information, news_strings)    
        return articles_results

    def extract_text(self, article_url: str) -> str:
        article_response = self._session.get(article_url)
        article_response.raise_for_status()
        article_soup = bs(article_response.text, features='lxml')
        text_blocks = article_soup.find_all('div', {'class': 'article__text'})
        article_text = ''
        for paragraph in text_blocks:
            article_text += paragraph.text
        return article_text

    def commit_to_db(self, news_data: dict):
        # news_tuples = [news_dict.values() for news_dict in news_data]
        with sqlite3.connect(self._db_name) as db_connection:
            db_connection.executemany(
                """
                INSERT INTO ria_news
                VALUES(:url, :title, :date, :text)
                """, news_data # TODO: Нужно передавать тюплы
            )

    
    def extract_information(self, news_string: str) -> dict:
        news_soup = bs(news_string, features='lxml')
        article_info =  news_soup.find('a', {'class': 'list-item__title'})
        article_url = article_info['href']
        article_title = news_soup.find('a', {'class': 'list-item__title'}).text
        article_date = news_soup.find('div', {'class': 'list-item__date'}).text
        article_text = self.extract_text(article_url=article_url)

        information = {
            'url': article_url,
            'title': article_title,
            'date': dateparser.parse(article_date, languages=['ru']),
            'text': article_text
        }

        print(f'{information["title"]} | {information["date"]}')

        return information

    @staticmethod
    def create_session(headers: dict) -> requests.Session:
        session = requests.Session()
        session.headers = headers
        return session

