# test cases for news_api.py


import requests
import pytest
from news_update_detector.news_api import NewsApi
from news_update_detector.news_exceptions import *
from news_update_detector import config


def test_NewsApi_request(monkeypatch):
    NORMAL_TEXT = 'normal html text'
    FAKE_URL = 'fake url'
    config.init()
    news_api = NewsApi()
    class ResObj:
        status_code = None
        text = ''
    res_obj = ResObj()
    res_obj.status_code = requests.codes.ok
    res_obj.text = NORMAL_TEXT
    monkeypatch.setattr(
        news_api.session,
        'get',
        lambda _1, params, timeout: res_obj
    )

    # Return content text when it's normal
    assert NORMAL_TEXT == news_api.request(FAKE_URL)
    res_obj.text = ''
    # Throw exception when response content is empty
    with pytest.raises(ResponseError):
        news_api.request(FAKE_URL)
    # Throw exception when status code is not ok
    res_obj.status_code = requests.codes.none
    with pytest.raises(RequestError):
        news_api.request(FAKE_URL)