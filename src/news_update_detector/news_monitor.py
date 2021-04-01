#!/usr/bin/python3
# -*- coding:utf-8 -*-


import click
import importlib
import threading
import signal

from . import config


class NewsMonitor:

    def __init__(self):
        self.scraper_thread_pool = []
        self._setup_signal_hook()


    @staticmethod
    def _get_website_scrapers():
        return [v for k, v in config.get('news_sources_map').items() if k in config.get('news_sources')]


    def _spawn_scraper_thread(self, scraper):
        scraper_module = importlib.import_module('.website_scrapers.' + scraper, __package__)
        scraper_module.start_monitoring()


    def start(self):
        website_scrapers = NewsMonitor._get_website_scrapers()

        for scraper in website_scrapers:
            t = threading.Thread(
                target=self._spawn_scraper_thread,
                args=(scraper,)
            )
            t.setDaemon(False)
            t.start()
            self.scraper_thread_pool.append(t)


    def stop(self, signum=None, frame=None):
        config.set('stop_monitoring', True)
        click.echo()
        click.echo('Stop monitoring. Please wait for the thread to finish.')
        for t in self.scraper_thread_pool:
            t.join()


    def _setup_signal_hook(self):
        signal.signal(signal.SIGINT, self.stop)
        signal.signal(signal.SIGTERM, self.stop)