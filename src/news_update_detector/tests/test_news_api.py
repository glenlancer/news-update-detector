# test cases for news_api.py


import requests
import pytest
from ..news_exceptions import *


def test_NewsApi_request(monkeypatch):
    from ..news_api import NewsApi

    NORMAL_TEXT = 'normal html text'
    FAKE_URL = 'fake url'

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
        lambda url, params, timeout: res_obj
    )

    assert NORMAL_TEXT == news_api.request(FAKE_URL)
    res_obj.text = ''
    with pytest.raises(ResponseError):
        news_api.request(FAKE_URL)
    res_obj.status_code = requests.codes.none
    with pytest.raises(RequestError):
        news_api.request(FAKE_URL)
