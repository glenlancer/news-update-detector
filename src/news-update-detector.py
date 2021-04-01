#!/usr/bin/python3
# -*- coding:utf-8 -*-


import os
import sys


def start():
    sys.path.insert(1, os.getcwd())
    if sys.version_info[0] == 3:
        import news_update_detector
        news_update_detector.main()
    else:
        print('This program uses Python3.')


if __name__ == '__main__':
    start()