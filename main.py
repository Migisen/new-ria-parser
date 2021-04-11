import sqlite3
import parser


con = sqlite3.connect('ria_news.db')

# Сделать в ф-цию
for i in range(1):
    with con:
        con.execute('create table if not exists news_table(news_id integer primary key, date text, url text, '
                    'title text, tags text, article_text text, last_url text)')
        try:
            url = con.execute('select last_url from news_table order by news_id desc limit 1').fetchone()[0]
        except TypeError:
            print('БД пустая')
            url = 'https://ria.ru/economy/'
        result = parser.simple_parser(url, iteration=1)
        for article in result:
            con.execute('insert into news_table (url, date, title, tags, article_text, last_url) '
                        'values(:url, :date, :title, :tags, :text, :last_url)                      ', article)

    print(f'Цикл {i} завершен')


# TODO: Сделай обратную выгрузку в Python тоже ф-цией
# with con:
#     urls = con.execute('select url from news_table').fetchall()
#     urls = [url[0] for url in urls]


# result = {'url': [url_1, ..., url_n],
#           'date': [date_1, ..., date_n],
#           ...}

#test = pd.read_sql('select * from news_table', con=con)
