#!/usr/bin/python3
# -*- coding:utf-8 -*-


import sys
import click
from . import config
from .news_monitor import NewsMonitor
from .__version__ import __version__


def run():
    news_monitor = NewsMonitor()
    news_monitor.start()
    input_text = None
    while input_text != '.exit':
        input_text = click.prompt('News monitor(s) are running. To exit, press ^C or type .exit')
        input_text = input_text.strip()
    news_monitor.stop()


@click.command()
@click.version_option(version=__version__)
@click.option('-s', '--sources', help='Set websites to monitor, e.g., news or "news other_sources" (news for news.com.au, more to be added)')
@click.option('-i', '--interval', default=5, type=int, help='Set interval of monitorings, in second(s)')
@click.option('-v', '--verbose', default=False, is_flag=True, help='Show more details.')
def main(
    sources,
    interval,
    verbose,
):
    config.init()
    if sources:
        config.set('news_sources', sources.split())
    else:
        click.secho('sources parameter is not set, use default source', bold=True)
    if interval:
        config.set('interval', interval)
    config.set('verbose', verbose)
    config.config_logging()

    try:
        run()
    except:
        sys.exit(0)


if __name__ == '__main__':
    main()