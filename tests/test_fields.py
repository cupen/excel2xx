import os
from excel2xx import Excel

root_dir = os.path.dirname(os.path.dirname(__file__))


def test_fields():
    fpath = root_dir + "/example/test.xlsx"
    l = Excel(fpath)[0].toList()
    assert l
    assert l[0]["fieldJson"] == {"a": 1, "b": 2}
    assert l[0]["fieldJson"] != {"a": 1, "b": 2, "c": 3}
    d = Excel(fpath)[0].toDict()
    assert d
