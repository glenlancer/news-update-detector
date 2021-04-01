#!/usr/bin/python3
# -*- coding:utf-8 -*-


class RequestError(RuntimeError):
    def __init__(self, *args, **kwargs):
        pass


class ResponseError(RuntimeError):
    def __init__(self, *args, **kwargs):
        pass