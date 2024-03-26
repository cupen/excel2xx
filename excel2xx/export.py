# coding: utf-8
from __future__ import unicode_literals, print_function
import json
from pprint import pformat
from mako.template import Template
from io import open
from datetime import datetime, date
from excel2xx.exporter import auto


def _defaultSerialize(obj):
    if isinstance(obj, (datetime, date)):
        return obj.isoformat()
    raise TypeError("Type %s not serializable" % type(obj))


def toJson(excel, output, encoding="utf-8"):
    data = auto.export(excel)
    with open(output, "w", encoding=encoding) as fp:
        json.dump(data, fp, ensure_ascii=False, indent=4, default=_defaultSerialize)
    pass


def toMako(excel, output, template, encoding="utf-8"):
    data = auto.export(excel)
    with open(output, "w", encoding=encoding) as fp:
        text = ""
        with open(template, "r", encoding=encoding) as f:
            text = Template(f.read()).render(excel=data, format=pformat)
        fp.write(text)
    pass


def toMsgPack(excel, output, encoding="utf-8"):
    import msgpack

    data = auto.export(excel)
    with open(output, mode="wb") as fp:
        fp.write(msgpack.packb(data, default=_defaultSerialize))
    pass


def toCSV(excel, output, encoding="utf-8"):
    # data = auto.export(excel)
    raise NotImplementedError("toCSV")
    pass
