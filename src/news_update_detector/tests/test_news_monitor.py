# test cases for news_monitor.py

from news_update_detector.website_scrapers import news_com_au
import pytest
from ..news_monitor import NewsMonitor
from .. import config


@pytest.fixture
def check_args():
    class CheckArgs:
        def __call__(self, *args):
            self.args = list(args)
    return CheckArgs()


def test__get_website_scrapers():
    config.init()
    config.set('news_sources', ['other', 'qq', 'news'])
    config.set('news_sources_map', {
        'news': 'news_com_au',
        'qq': 'news_qq_com',
        'other': 'other_com',
    })
    news_monitor = NewsMonitor()
    assert sorted(news_monitor._get_website_scrapers()) == sorted(['other_com', 'news_qq_com', 'news_com_au'])


def test__spawn_scraper_thread(mocker, monkeypatch):
    from ..website_scrapers import news_com_au
    monkeypatch.setattr(news_com_au, 'start_monitoring', lambda: None)
    spy_start_monitoring = mocker.spy(news_com_au, 'start_monitoring')
    news_monitor = NewsMonitor()
    news_monitor._spawn_scraper_thread('news_com_au')
    assert spy_start_monitoring.call_count == 1


def test_start(mocker, monkeypatch, check_args):
    news_monitor = NewsMonitor()
    monkeypatch.setattr(NewsMonitor, '_get_website_scrapers', lambda: ['news_com_au'])
    monkeypatch.setattr(NewsMonitor, '_spawn_scraper_thread', check_args)
    news_monitor.start()
    news_monitor.stop()
    assert check_args.args == ['news_com_au']

