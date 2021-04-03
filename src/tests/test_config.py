# test cases for config.py


from news_update_detector import config


def test_get_set():
    config.init()
    config.set('verbose', True)
    assert config.get('verbose') == True