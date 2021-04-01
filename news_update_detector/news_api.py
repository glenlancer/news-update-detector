#!/usr/bin/python3
# -*- coding:utf-8 -*-


import requests
from . import config
from .news_exceptions import RequestError, ResponseError


class NewsApi:

    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update(config.get('fake_headers'))


    def request(self, url, data=None):
        response = self.session.get(url, params=data, timeout=7)
        if response.status_code != requests.codes.ok:
            raise RequestError(response.text)
        if not response.text:
            raise ResponseError('Response content is empty.')
        return response.text