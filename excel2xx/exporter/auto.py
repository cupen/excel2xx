# encoding: utf-8


def export(ex, ver=1):
    d = {}
    for sheet in ex:
        if str.startswith(sheet.name, "#"):
            continue
        name, _type = parse_sheet_name(sheet.name)
        if not name:
            raise Exception(f"invalid sheet {sheet.name}")
        if _type == "list":
            d[name] = sheet.toList()
        elif _type == "map":
            d[name] = sheet.toDict()
        elif _type == "kv":
            d[name] = sheet.toKV()
        else:
            raise Exception(f"invalid sheet {sheet.name} name={name} type={_type}")
    return d


def parse_sheet_name(name: str) -> tuple[str, str]:
    """
    >>> _parse_sheet_name("name")
    ('name', 'list')
    >>> _parse_sheet_name("name(list)")
    ('name', 'list')
    >>> _parse_sheet_name("name123(map)")
    ('name123', 'map')
    >>> _parse_sheet_name("name123((map)")
    Traceback (most recent call last):
    Exception: duplicated symbol '('
    >>> _parse_sheet_name("sheet-map(map)")
    ('sheet-map', 'map')
    """
    name = name.strip()
    if "=" in name:
        arr = list(map(lambda x: x.strip(), name.split("=")))
        name = arr[1]
    return _parse_sheet_name(name)


def _parse_sheet_name(name) -> tuple[str, str]:
    realName = ""
    realType = ""
    state = 0  # 0-start, 1-name, 2-type, 3-end
    for c in name:
        if c == "(":
            if state != 1:
                raise Exception(f"duplicated symbol '('")
            state = 2
        elif c == ")":
            if state != 2:
                raise Exception(f" ')' must behind of '('")
            if len(realType) <= 0:
                raise Exception(f" '()' must be one of list, map, kv")
            state = 3
            break  # end
        else:
            if not str.isalnum(c) and c not in ["-", "_"]:
                raise Exception(f"invalid char '{c}'")
            if state == 0:
                realName = c
                state = 1
            elif state == 1:
                realName += c
            elif state == 2:
                realType += c
            else:
                raise Exception(f"BUG!")
            pass
        pass
    if realType == "":
        realType = "list"
    return realName, realType
