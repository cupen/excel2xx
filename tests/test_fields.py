import os
from excel2xx import Excel, fields, fieldmeta

root_dir = os.path.dirname(os.path.dirname(__file__))


def test_fields():
    fpath = root_dir + "/example/test.xlsx"
    l = Excel(fpath)[0].toList()
    assert l
    assert l[0]["fieldJson"] == {"a": 1, "b": 2}
    assert l[0]["fieldJson"] != {"a": 1, "b": 2, "c": 3}
    d = Excel(fpath)[0].toDict()
    assert d


def test_IntArray():
    f = fieldmeta.DEFINE_FIELDS["array<int>"]
    assert f == fields.IntArray
    assert f.format(None, 1.0) == [1]
    assert f.format(None, "1,2, 6,   7,8") == [1, 2, 6, 7, 8]
    assert f.format(None, "1, 9 ,2,3") == [1, 9, 2, 3]
