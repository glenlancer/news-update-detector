# test cases for news_com_au.py


from news_update_detector.news_api import NewsApi
from news_update_detector import config
from news_update_detector.website_scrapers.news_com_au import *
from news_update_detector.dbs.newsComAuDb import NewsComAuRecord


config.init()
news_api = NewsApi()
# Use real content each time, if this fails, the program needs to be updated anyway.
page_content = news_api.request(NewsComAuMonitor.NEWS_COM_AU_URL)
page_bs = BeautifulSoup(page_content, 'html.parser')


def test__get_bs_obj(monkeypatch):
    monkeypatch.setattr(NewsComAuMonitor, '__init__', lambda x: None)
    news_com_au_monitor = NewsComAuMonitor()
    news_com_au_monitor.news_api = NewsApi()
    monkeypatch.setattr(news_com_au_monitor.news_api, 'request', lambda x: page_content)
    import bs4
    assert isinstance(news_com_au_monitor._get_bs_obj(NewsComAuMonitor.NEWS_COM_AU_URL), bs4.BeautifulSoup) == True


def test__collect_all_story_blocks(monkeypatch):
    monkeypatch.setattr(NewsComAuMonitor, '__init__', lambda x: None)
    news_com_au_monitor = NewsComAuMonitor()
    assert len(news_com_au_monitor._collect_all_story_blocks(page_bs)) == 68


def test__parse_news_record(monkeypatch):
    monkeypatch.setattr(NewsComAuMonitor, '__init__', lambda x: None)
    news_com_au_monitor = NewsComAuMonitor()
    all_story_blocks = news_com_au_monitor._collect_all_story_blocks(page_bs)
    all_news_records = news_com_au_monitor._parse_news_records(all_story_blocks)
    assert len(all_news_records) == 68
    assert isinstance(all_news_records[0], NewsComAuRecord) == True


def test__get_news_content(monkeypatch):
    article_content = '''
        <h1 class="story-headline">Story Headline</h1>
        <p class="intro">Story Introduction</p>
        <div id="story">
            <p>Story text 1</p>
            <p>Story text 2</p>
            <p>Story text 3</p>
        </div>
    '''
    monkeypatch.setattr(NewsComAuMonitor, '__init__', lambda x: None)
    news_com_au_monitor = NewsComAuMonitor()
    news_com_au_monitor.news_api = NewsApi()
    monkeypatch.setattr(news_com_au_monitor.news_api, 'request', lambda x: article_content)
    assert news_com_au_monitor._get_news_content('Fake Url') == (
        'Story Headline\n'
        'Story Introduction\n'
        'Story text 1\n'
        'Story text 2\n'
        'Story text 3\n'
    )


def test_analyse_updated_record(mocker, monkeypatch):
    monkeypatch.setattr(NewsComAuMonitor, '__init__', lambda x: None)
    news_com_au_monitor = NewsComAuMonitor()
    ext_record = NewsComAuRecord()
    new_record = NewsComAuRecord()
    assert news_com_au_monitor._analyse_updated_record(ext_record, new_record) == None
    EXT_TIME = '2021-04-03T03:55:00.000+00:00'
    NEW_TIME = '2021-04-03T04:55:00.000+00:00'
    ext_record.update_time, new_record.update_time = EXT_TIME, NEW_TIME
    monkeypatch.setattr(NewsComAuMonitor, '_get_news_content', lambda x, y: None)
    monkeypatch.setattr(NewsComAuMonitor, 'show_updated_item', lambda x, y, z: None)
    spy__get_news_content = mocker.spy(news_com_au_monitor, '_get_news_content')
    spy_show_updated_item = mocker.spy(news_com_au_monitor, 'show_updated_item')
    news_com_au_monitor._analyse_updated_record(ext_record, new_record)
    assert spy__get_news_content.call_count == 1
    assert spy_show_updated_item.call_count == 1
    ext_record.update_time, new_record.update_time = NEW_TIME, EXT_TIME
    assert news_com_au_monitor._analyse_updated_record(ext_record, new_record) == None


def test_analyse_news_records(mocker, monkeypatch):
    monkeypatch.setattr(NewsComAuMonitor, '__init__', lambda x: None)
    news_com_au_monitor = NewsComAuMonitor()
    class DbStub:
        def insert_news(x):
            pass
        def update_news(x):
            pass
        def select_news_via_heading(x):
            pass
    news_com_au_monitor.db = DbStub()
    ext_record = NewsComAuRecord()
    new_record = NewsComAuRecord()
    ext_record.heading = 'same heading'
    new_record.heading = 'same heading'
    monkeypatch.setattr(news_com_au_monitor.db, 'insert_news', lambda x: None)
    monkeypatch.setattr(news_com_au_monitor.db, 'update_news', lambda x: None)
    monkeypatch.setattr(news_com_au_monitor.db, 'select_news_via_heading', lambda x: None)
    monkeypatch.setattr(NewsComAuMonitor, '_get_news_content', lambda x, y: '')
    monkeypatch.setattr(NewsComAuMonitor, 'show_new_item', lambda x, y: None)
    spy_db_insert_news = mocker.spy(news_com_au_monitor.db, 'insert_news')
    spy_db_update_news = mocker.spy(news_com_au_monitor.db, 'update_news')
    spy_db_select_news_via_heading = mocker.spy(news_com_au_monitor.db, 'select_news_via_heading')

    news_com_au_monitor.analyse_news_records([ext_record, new_record])
    assert spy_db_select_news_via_heading.call_count == 1
    assert spy_db_insert_news.call_count == 1
    assert spy_db_update_news.call_count == 0

    ext_record.url = NewsComAuMonitor.NEWS_COM_AU_URL
    monkeypatch.setattr(NewsComAuMonitor, 'show_new_item', lambda x, y: ext_record)
    monkeypatch.setattr(NewsComAuMonitor, '_analyse_updated_record', lambda x, y, z: ext_record)
    monkeypatch.setattr(news_com_au_monitor.db, 'select_news_via_heading', lambda x: ext_record)
    news_com_au_monitor.analyse_news_records([ext_record])
    assert spy_db_select_news_via_heading.call_count == 1
    assert spy_db_update_news.call_count == 1