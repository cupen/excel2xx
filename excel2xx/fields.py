# coding:utf-8
from __future__ import unicode_literals, print_function

import xlrd
from xlrd.xldate import xldate_as_datetime

__author__ = 'cupen'


class Field:

    def __init__(self, name, colnum, wb=None):
        self.name = name
        self.colum = colnum
        self.wb = wb
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
        return list(v)


class Auto(Field):
    def format(self, v):
        return v

class Date(Field):
    def format(self, v):
        try:
            return xldate_as_datetime(v, self.wb.datemode).date()
        except:
            return None


class DateTime(Field):
    def format(self, v):
        try:
            return xldate_as_datetime(v, self.wb.datemode)
        except:
            return None
