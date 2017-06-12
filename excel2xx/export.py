# coding: utf-8
from __future__ import unicode_literals, print_function
import json
from collections import OrderedDict
from pprint import pformat
from mako.template import Template
import sys
if sys.version_info[0] == 2:
    from io import open

__author__ = 'cupen'
__email__ = 'cupen@foxmail.com'


def toJson(excel, output, encoding='utf-8'):
    _dict = OrderedDict()
    for sheet in excel:
        _dict[sheet.name] = list(sheet)

    with open(output, mode='w', encoding=encoding) as f:
        json.dump(_dict, f)
    pass


def toMako(excel, output, template, encoding='utf-8'):
    with open(output, mode='w', encoding=encoding) as ouputfile:
        text = ''
        with open(template, mode='r', encoding=encoding) as f:
            text = Template(f.read()).render(excel=excel, format=pformat)
        ouputfile.write(text)
    pass


def toMsgPack(excel, output, encoding='utf-8'):
    import msgpack

    _dict = OrderedDict()
    for sheet in excel:
        _dict[sheet.name] = list(sheet)

    with open(output, mode='wb') as f:
        f.write(msgpack.packb(_dict))
    pass