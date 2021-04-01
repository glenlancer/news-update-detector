#!/usr/bin/python3
# -*- coding:utf-8 -*-


import sqlite3
import logging


class NewsComAuRecord:
    def __init__(self, record=None):
        self.heading = record[1] if record else ''
        self.url = record[2] if record else ''
        self.image = record[3] if record else ''
        self.standfirst = record[4] if record else ''
        self.update_time = record[5] if record else ''
        self.content = record[6] if record else ''


class NewsComAuDb:

    DB_FILE = 'news.db'
    
    # Assume headings are unique, which may not be true.
    SQL_CREATE_NEWS_TABLE = '''
        CREATE TABLE IF NOT EXISTS news_com_au (
            id          INTEGER PRIMARY KEY,
            heading     TEXT NOT NULL UNIQUE,
            url         TEXT,
            image       TEXT,
            standfirst  TEXT,
            update_time TEXT,
            content     TEXT
        );
    '''


    def __init__(self):
        self.conn = None
        self.logger = logging.getLogger(__name__)
        self.create_connection()
        self.create_table(self.SQL_CREATE_NEWS_TABLE)
    

    def create_connection(self):
        try:
            self.conn = sqlite3.connect(self.DB_FILE)
        except sqlite3.Error as e:
            self.logger.error(f'Db connection error: {e}')


    def create_table(self, create_table_sql):
        try:
            c = self.conn.cursor()
            c.execute(create_table_sql)
        except sqlite3.Error as e:
            self.logger.error(f'Db create table error: {e}')


    def select_news_via_heading(self, heading):
        sql = f'SELECT * FROM news_com_au WHERE heading = "{heading}"'
        record = self.db_fetchone(sql)
        if record:
            return NewsComAuRecord(record)
        return None


    def db_fetchone(self, sql):
        try:
            c = self.conn.cursor()
            c.execute(sql)
            res = c.fetchone()
            return res
        except Exception as e:
            self.logger.error(f'SQL failed: {sql}, {str(e)}')
            return None


    def insert_news(self, records):
        sql = '''
            INSERT OR IGNORE INTO news_com_au (heading,url,image,standfirst,update_time,content)
            VALUES (?,?,?,?,?,?)
        '''
        try:
            c = self.conn.cursor()
            for record in records:
                c.execute(sql,
                    (
                        record.heading,
                        record.url,
                        record.image,
                        record.standfirst,
                        record.update_time,
                        record.content,
                    ))
            self.conn.commit()
        except sqlite3.Error as e:
            self.logger.error(f'Db insertion error: {e}')
    
    
    def update_news(self, records):
        sql = '''
            UPDATE news_com_au
            SET url = ?,
                standfirst = ?,
                update_time = ?,
                content = ?
            WHERE heading = ?
        '''
        try:
            c = self.conn.cursor()
            for record in records:
                c.execute(sql,
                    (
                        record.url,
                        record.standfirst,
                        record.update_time,
                        record.content,
                        record.heading,
                    ))
            self.conn.commit()
        except sqlite3.Error as e:
            self.logger.error(f'Db update error: {e}')