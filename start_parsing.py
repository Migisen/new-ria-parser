from src.RiaParser import RiaParser
import sqlite3
import warnings

warnings.filterwarnings(
    "ignore",
    message="The localize method is no longer necessary, as this time zone supports the fold attribute",
)

params = {
    'db_name': 'beautiful_news.db'
}

# russian_economy_url = r'https://ria.ru/economy+location_rossiyskaya-federatsiya/'
economy_url = r'https://ria.ru/economy/'
parser = RiaParser(target_url=economy_url, db_name=params['db_name'])

with sqlite3.connect(params['db_name']) as db_connection:
    db_connection.execute(
        '''CREATE TABLE IF NOT EXISTS ria_news (
            url TEXT PRIMARY KEY,
            title TEXT,
            date TEXT,
            text TEXT
        )
        '''
        )


if __name__=='__main__':
    parser.start_parsing()

