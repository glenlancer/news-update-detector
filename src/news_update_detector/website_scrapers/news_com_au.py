#!/usr/bin/python3
# -*- coding:utf-8 -*-


import threading
import traceback
import logging
import click
import timestring
import difflib
from rich.console import Console
from rich.table import Table
from bs4 import BeautifulSoup
from .. import config
from ..news_api import NewsApi
from ..dbs.newsComAuDb import *
from ..news_exceptions import *


class NewsComAuMonitor:

    NEWS_COM_AU_URL = 'https://www.news.com.au/'

    def __init__(self):
        self.news_api = NewsApi()
        self.logger = logging.getLogger(__name__)
        self.db = NewsComAuDb()
        self.console = Console()


    def _get_bs_obj(self, url):
        err = None
        try:
            page_text = self.news_api.request(url)
            page_bs = BeautifulSoup(page_text, 'html.parser')
        except (RequestError, ResponseError) as e:
            err = (self._get_bs_obj.__name__, e)
        except Exception as e:
            err_content = traceback.format_exc() if config.get('verbose') else str(e)
            err = (self._get_bs_obj.__name__, err_content)
        finally:
            if err:
                self.logger.error(err)
                return None
            return page_bs


    @staticmethod
    def _collect_all_story_blocks(page_bs):
        story_blocks_bs = page_bs.find_all('div', {'class': 'story-block'})
        all_story_blocks = []
        for story_block_bs in story_blocks_bs:
            if story_block_bs.find('h4', {'class': 'heading'}) and story_block_bs.find('span', {'class': 'standfirst-text'}):
                all_story_blocks.append(story_block_bs)
        return all_story_blocks


    @staticmethod
    def _parse_news_records(all_story_blocks):
        news_records = []
        for stroy_block in all_story_blocks:
            record = NewsComAuRecord()
            heading_bs = stroy_block.find('h4', {'class': 'heading'})
            if heading_bs:
                record.heading = heading_bs.get_text().strip()
            else:
                continue
            url_bs = heading_bs.find('a')
            if url_bs and 'href' in url_bs.attrs:
                record.url = url_bs.attrs['href']
            date_n_time_bs = stroy_block.find('span', {'class': 'date-and-time'})
            if date_n_time_bs and 'title' in date_n_time_bs.attrs:
                record.update_time = date_n_time_bs.attrs['title']
            image_bs = stroy_block.find('img')
            if image_bs and 'src' in image_bs.attrs:
                record.image = image_bs.attrs['src']
            standfirst_bs = stroy_block.find('span', {'class': 'standfirst-text'})
            if standfirst_bs:
                record.standfirst = standfirst_bs.get_text().strip()
            news_records.append(record)
        return news_records


    def get_news_content(self, url):
        if not url:
            return ''
        page_bs = self._get_bs_obj(url)
        if not page_bs:
            return ''
        headline_bs = page_bs.find('h1', {'class': 'story-headline'})
        intro_bs = page_bs.find('p', {'class': 'intro'})
        article_bs = page_bs.find('article', {'id': 'story'})
        if not article_bs:
            article_bs = page_bs.find('div', {'id': 'story'})
        content = ''
        if headline_bs:
            content += headline_bs.get_text().strip()
            content += '\n'
        if intro_bs:
            content += intro_bs.get_text().strip()
            content += '\n'
        if article_bs:
            children_p = article_bs.findChildren('p')
            for child_p in children_p:
                content += child_p.get_text().strip()
                content += '\n'
        return content


    def show_new_item(self, record):
        new_item_table = Table()
        new_item_table.add_column('Status', style='bold')
        new_item_table.add_column('Time')
        new_item_table.add_column('Heading')
        new_item_table.add_column('Standfirst')
        new_item_table.add_row(
            'New Item',
            record.update_time if record.update_time else 'N/A',
            record.heading,
            record.standfirst if len(record.standfirst) < 60 or config.get('verbose') else record.standfirst[:60] + '...',
        )
        self.console.print()
        self.console.print(new_item_table)


    def show_updated_item(self, ext_record, new_record):
        updated_item_table = Table()
        updated_item_table.add_column('Status', style='bold')
        updated_item_table.add_column('Prev Update Time')
        updated_item_table.add_column('Curr Update Time')
        updated_item_table.add_column('Heading')
        ext_content_lines = ext_record.content.splitlines()
        new_content_lines = new_record.content.splitlines()
        content_diff = difflib.Differ().compare(ext_content_lines, new_content_lines)
        updated_item_table.add_row(
            'Updated Item',
            ext_record.update_time if ext_record.update_time else 'N/A',
            new_record.update_time if new_record.update_time else 'N/A',
            new_record.heading,
        )
        self.console.print()
        self.console.print(updated_item_table)
        self.console.print()
        self.console.print('\n'.join(content_diff))


    def analyse_updated_record(self, ext_record, new_record):
        try:
            ext_update_time = timestring.Date(ext_record.update_time)
            new_update_time = timestring.Date(new_record.update_time)
        except:
            return None
        if ext_update_time < new_update_time:
            new_record.content = self.get_news_content(new_record.url)
            self.show_updated_item(ext_record, new_record)
            return new_record
        return None


    def analyse_news_records(self, all_news_records):
        added_news_records = []
        updated_news_records = []
        prev_record = None
        for record in all_news_records:
            if prev_record and (prev_record.heading == record.heading):
                continue
            else:
                prev_record = record
            ext_record = self.db.select_news_via_heading(record.heading)
            if ext_record is None:
                record.content = self.get_news_content(record.url)
                added_news_records.append(record)
                self.show_new_item(record)
            else:
                if not record.url.startswith(NewsComAuMonitor.NEWS_COM_AU_URL):
                    continue
                updated_record = self.analyse_updated_record(ext_record, record)
                if updated_record:
                    updated_news_records.append(updated_record)
        if added_news_records:
            self.db.insert_news(added_news_records)
        if updated_news_records:
            self.db.update_news(updated_news_records)


    def monitoring(self):
        page_bs = self._get_bs_obj(NewsComAuMonitor.NEWS_COM_AU_URL)
        if page_bs is None:
            return
        all_story_blocks = NewsComAuMonitor._collect_all_story_blocks(page_bs)
        all_news_records = NewsComAuMonitor._parse_news_records(all_story_blocks)
        self.analyse_news_records(all_news_records)


def start_monitoring():
    if config.get('stop_monitoring'):
        click.secho('Monitoring to news.com.au stopped', bold=True)
        return
    monitor = NewsComAuMonitor()
    monitor.monitoring()
    threading.Timer(config.get('interval'), start_monitoring).start()
