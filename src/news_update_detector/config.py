#!/usr/bin/python3
# -*- coding:utf-8 -*-

import logging


def init():
    global opts
    opts = {
        'news_sources': ['news'],
        'news_sources_map': {
            'news': 'news_com_au',
        },
        'verbose': False,
        'fake_headers': {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Charset': 'UTF-8,*;q=0.5',
            'Accept-Encoding': 'gzip,deflate,sdch',
            'Accept-Language': 'en-US,en;q=0.8',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:60.0) Gecko/20100101 Firefox/60.0',
            'referer': 'https://www.google.com',
        },
        'stop_monitoring': False,
        'interval': 2,
    }


def config_logging():
    logging.basicConfig(
        format='[%(asctime)s] %(levelname)-8s | %(name)s: %(msg)s ',
        datefmt='%H:%M:%S',
    )


def get(key):
    return opts.get(key, '')


def set(key, value):
    opts[key] = value