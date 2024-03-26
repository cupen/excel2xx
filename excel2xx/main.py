# encoding: utf-8
"""Export data from Excel file.

Usage:
    excel2xx.py json    <excel> [options]
    excel2xx.py msgpack <excel> [options]
    excel2xx.py mako    <excel> --template=FILE [options]
    excel2xx.py --version

Arguments:
    <excel>                        Excel file path.

Options:
    -h --help                      show this help message and exit.
    --version                      show version and exit.
    -o --output=FILE               output to file.
    --name-row=NAME_ROW            name row number. [default: 1]
    --type-row=TYPE_ROW            type row number. [default: 2]
    --desc-row=DESC_ROW            desc row number. [default: 3]
    --data-row=DATA_ROW            data row number. [default: 4]
    -v --verbose                   show debug infomation.
    -vv --verbose2                 show more debug infomation.
"""
import os
import traceback
from docopt import docopt
from excel2xx import Excel, export, FieldMeta


def main(args):
    excelFile = args["<excel>"]
    outputFile = args["--output"]

    if excelFile:
        excelFile = os.path.realpath(excelFile)
    if outputFile:
        outputFile = os.path.realpath(outputFile)

    if not os.path.isfile(excelFile):
        print("Unexist file:" + excelFile)
        return 1

    meta = FieldMeta(
        name=int(args["--name-row"]) - 1,
        type=int(args["--type-row"]) - 1,
        desc=int(args["--desc-row"]) - 1,
        data=int(args["--data-row"]) - 1,
    )
    excel = Excel(excelFile, fieldMeta=meta)
    if args["json"]:
        export.toJson(excel, args["--output"] or "%(excelFile)s.json" % locals())
    elif args["msgpack"]:
        export.toMsgPack(excel, args["--output"] or "%(excelFile)s.json" % locals())
    elif args["mako"]:
        export.toMako(
            excel, args["--output"] or "%(--template)s.mako" % args, args["--template"]
        )
    else:
        print("Invalid subcmd.")
        return 2
    return 0


def main_docopt(argv=None):
    args = docopt(__doc__, argv)
    if args["--verbose2"]:
        print(args)
    try:
        return main(args)
    except Exception as e:
        errorMsg = traceback.format_exc() if args["--verbose"] else e
        print(errorMsg)
        return 2
    pass


if __name__ == "__main__":
    import sys

    exit(main_docopt(sys.argv))
