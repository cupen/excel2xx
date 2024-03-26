# encoding: utf-8
import os
import importlib
import importlib.util
from excel2xx import console


def import_validator(name, fpath):
    spec = importlib.util.spec_from_file_location(name, fpath)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    # sys.modules[name] = module
    return module


def run(data, data_dir: str, validator_name="_validator"):
    validator_dir = os.path.join(data_dir, validator_name)
    for fpath in list_files(validator_dir):
        show = fpath[len(data_dir) :].strip("/")
        # fpathx = console.Colors.blue(show)
        print(f"\t{show} -> ", end="")
        # mpath = fpath.replace("/", ".").replace(".py", "")
        pkgname = os.path.basename(fpath).split(".")[0]
        mod = import_validator(pkgname, fpath)
        try:
            mod.validate(data)
            console.success("OK")
        except Exception as ex:
            console.fail("FALIED")
            console.error("\t\t" + str(ex))
            return 1
        pass
    print("\n")
    return 0


def list_files(_dir: str):
    import bisect

    rs = []  # type: list[str]
    for base, dirs, files in os.walk(_dir):
        for fname in files:
            if not fname.endswith(".py"):
                continue
            if fname.endswith("__.py"):
                continue
            fpath = os.path.join(base, fname)
            # rs.append(fpath)
            bisect.insort(rs, fpath)
            pass
        pass
    return rs
