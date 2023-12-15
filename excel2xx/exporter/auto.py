# encoding: utf-8


def export(ex, ver=1):
    d = {}
    for sheet in ex:
        if str.startswith(sheet.name, "#"):
            continue
        name, _type = parse_sheet_name(sheet.name)
        if _type == "list":
            d[name] = sheet.toList()
        elif _type == "map":
            d[name] = sheet.toDict()
        elif _type == "kv":
            d[name] = sheet.toKV()
        else:
            raise Exception(f"invalid sheet {sheet.name} name={name} type={_type}")
    return d


def parse_sheet_name(name) -> (str, str):
    """
    >>> _parse_sheet_name("name") -> ("name", "list")
    """
    name = name.strip()
    if "=" not in name:
        return name, "list"
    arr = list(map(lambda x: x.strip(), name.split("=")))
    if len(arr) <= 1:
        return "", ""
    name = arr[1]
    return _parse_sheet_name(name)


def _parse_sheet_name(name) -> (str, str):
    realName = ""
    realType = ""
    state = 0  # 0-init, 1-type, 2-end
    for c in name:
        if c == "(":
            if state != 0:
                raise Exception(f"duplicated symbol '('")
            state = 1
        elif c == ")":
            if state != 1:
                raise Exception(f" ')' must behind of '('")
            if len(realType) <= 0:
                raise Exception(f" '()' must be one of list, map, kv")
            state = 2
            break  # end
        else:
            if state == 0:
                realName += c
            elif state == 1:
                realType += c
            else:
                raise Exception(f"BUG!")
            pass
        pass
    if realType == "":
        realType = "list"
    return realName, realType
