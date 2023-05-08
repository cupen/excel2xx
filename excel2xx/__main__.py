# encoding: utf-8
import os, sys

debug = os.environ.get("EXCEL2XX_DEBUG", 0)
if debug:
    print("sys.path:")
    for path in sys.path:
        print("\t" + path)

import excel2xx.main
import excel2xx.fields

if __name__ == "__main__":
    excel2xx.setUnits("K,M,G,T,P", size=1024)
    exit(excel2xx.main.main_docopt())
    pass
