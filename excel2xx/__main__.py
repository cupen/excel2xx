# encoding: utf-8
from __future__ import unicode_literals, print_function
import excel2xx.main
import excel2xx.fields

__author__ = 'cupen'
__email__ = 'xcupen@gmail.com'

if __name__ == '__main__':
    excel2xx.fields.BigNumber.setUnits(",K,M,G")
    exit(excel2xx.main.main_docopt())
    pass
