# coding:utf-8
from __future__ import unicode_literals, print_function

import sys

__author__ = 'cupen'

if sys.version_info[0] == 2:
    str = unicode


class Field:
    def __init__(self, name, colnum):
        self.name = name
        self.colum = colnum
        pass

    def format(self, v):
        raise NotImplementedError


class Int(Field):
    def format(self, v):
        return int(v)


class String(Field):
    def format(self, v):
        return str(v)


class Float(Field):
    def format(self, v):
        return float(v)


class Array(Field):
    def format(self, v):
        if isinstance(v, str):
            v = v.split(',')
        return list(v)


class Auto(Field):
    def format(self, v):
        return v


