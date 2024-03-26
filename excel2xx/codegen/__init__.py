# encoding: utf-8
import os
import logging
import glob
import traceback
import excel2xx.console as console
from mako.template import Template

log = logging.getLogger("codegen")

NOTE = "// DONT EDIT: generated by excel2xx/codegen.\n"


def generate(src: list, context={}, note=NOTE, encoding="utf-8", newline="\n"):
    """
    generate source code from mako template files
    """
    if isinstance(src, str):
        src = [src]
    elif isinstance(src, list):
        pass
    else:
        raise Exception("invalid params: src = " + str(src))

    fpaths = []
    for pattern in src:
        fpaths += glob.glob(pattern, recursive=True)
        pass
    print(f"\ttemplate files: {len(fpaths)}")

    for fpath in fpaths:
        fpath_new = fpath.replace(".mako", "")
        print(f"\t{fpath} -> ", end="")
        if not fpath.endswith(".mako"):
            print(console.Colors.yellow(fpath_new))
            continue

        ctx = dict(**context)
        ctx["__file__"] = fpath
        ctx["__dir__"] = os.path.dirname(fpath)

        tmpl = load_template(fpath)
        try:
            text = tmpl.render(**ctx)
            with open(fpath_new, "w", encoding=encoding, newline=newline) as fp:
                if note:
                    fp.write(note)
                fp.write(text)
                pass
            print(console.Colors.green(fpath_new))
            if fpath_new.endswith(".go"):
                os.system(f"go fmt {fpath_new} 2>&1 > /dev/null")
        except Exception:
            print(console.Colors.red(fpath_new))
            print("")
            print(console.Colors.red(f"something wrong with '{fpath}'"))
            stacks = traceback.format_exc()
            print(stacks)
            exit(101)
            pass
        pass
    print("\n")
    pass


def load_template(fpath) -> Template:
    with open(fpath, mode="r", encoding="utf-8") as fp:
        return Template(fp.read())
    pass
