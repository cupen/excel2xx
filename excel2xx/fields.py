__author__ = 'cupen'


class Field:

    def __init__(self, name, colnum: int):
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
        return list(v)


class Auto(Field):
    def format(self, v):
        return v


