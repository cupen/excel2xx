# encoding:UTF-8
"""Export excel to json.

Usage:
    excel2json.py INPUT [--output=<output>] [--type=list] [--debug=0]
    excel2json.py [options]

Arguments:
    INPUT    Excel file.

Options:
    --help show this help message and exit
    --version show version and exit
    --debug=1 show debug infomation
    -o --output=FILE output file
    -t --type=TYPE output json object type was 'list' or 'dict'. [default: list]

"""
import os
from docopt import docopt

__author__ = 'cupen'
__email__ = 'cupen@foxmail.com'

from excel2xx import Excel

def main(args):
    if args['--help']:
        print(__doc__)
        exit(0)

    excelFile = args.get('INPUT')
    jsonFile = args.get('--output')
    jsonType = args.get('--type')
    if not excelFile:
        print("Unexist 'INPUT'.")
        exit(1)

    if excelFile: excelFile = os.path.realpath(excelFile)
    if jsonFile: jsonFile = os.path.realpath(jsonFile)

    # print("Export '%s' to '%s'" % (excelFile, jsonFile))

    excel = Excel(excelFile)
    jsonText = None
    if jsonType and jsonType == 'dict':
        jsonText = excel.toJson(Excel.XX_TYPE_DICT, jsonFile)
    else:
        jsonText = excel.toJson(Excel.XX_TYPE_LIST, jsonFile)

    if not jsonFile:
        print(jsonText)
    pass

if __name__ == '__main__':
    # import sys
    # sys.argv += "example/test.xls --type dict --debug 1".split(' ')
    args = docopt(__doc__)
    if args['--debug']: print(args)
    main(args)
    pass
