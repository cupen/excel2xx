# encoding: utf-8
from __future__ import unicode_literals, print_function
import excel2xx.main
import excel2xx.fields

__author__ = 'cupen'
__email__ = 'xcupen@gmail.com'

if __name__ == '__main__':
    excel2xx.setUnits("K,M,G,T,P", size=1024)
    exit(excel2xx.main.main_docopt())
    pass
