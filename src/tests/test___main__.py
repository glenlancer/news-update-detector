# test cases for __main__.py


from click.testing import CliRunner
from news_update_detector import __main__
from news_update_detector import config


def test_main(monkeypatch):
    monkeypatch.setattr(__main__, 'run', lambda: None)
    runner = CliRunner()
    result = runner.invoke(__main__.main, [])
    assert result.exit_code == 0
    assert result.output == 'sources parameter is not set, use default source\n'
    assert config.get('interval') == 5
    assert config.get('verbose') == False