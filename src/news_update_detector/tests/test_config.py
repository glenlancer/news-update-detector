# test cases for config.py


def test_get_set():
    from .. import config
    config.init()
    config.set('verbose', True)
    assert config.get('verbose') == True
