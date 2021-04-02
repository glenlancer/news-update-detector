# test cases for newsComAuDb.py

import os
from ..dbs.newsComAuDb import *


def test_NewsComAuDb():
    TEST_DB_FILE = 'test_news.db'
    NewsComAuDb.DB_FILE = TEST_DB_FILE
    
    news_com_au_db = NewsComAuDb()
    assert os.path.isfile('test_news.db') == True

    news_com_au_db.create_table(NewsComAuDb.SQL_CREATE_NEWS_TABLE)
    news_record = NewsComAuRecord()
    TEST_HEADING = 'test heading'
    TEST_TIME = '2021-01-01T00:00:00.000+00:00'
    TEST_CONTENT = 'updated content'
    news_record.heading = TEST_HEADING
    news_record.update_time = TEST_TIME

    news_com_au_db.insert_news([news_record])
    selected_record = news_com_au_db.select_news_via_heading(TEST_HEADING)
    assert selected_record.heading == TEST_HEADING
    assert selected_record.update_time == TEST_TIME
    assert None == news_com_au_db.select_news_via_heading('none record')

    selected_record.content = TEST_CONTENT
    news_com_au_db.update_news([selected_record])
    selected_record = news_com_au_db.select_news_via_heading(TEST_HEADING)
    assert selected_record.content == TEST_CONTENT

    if os.path.exists(TEST_DB_FILE):
        os.remove(TEST_DB_FILE)