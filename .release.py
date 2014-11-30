__author__ = 'cupen'

import os
from zipfile import ZipFile


if __name__ == '__main__':
    zipName = 'excel2xx'
    zipFile = zipName + '.zip'
    if(os.path.exists(zipFile)):
        os.remove(zipFile)

    fileList = [
        'setup.py',
        'excel2json.py',
        'install.bat',
        'test.sh'
        'clear.sh'
    ]
    with ZipFile(zipFile, 'w') as zipfile:
        for tmpFileName in fileList:
            zipfile.write(tmpFileName, zipName + '/' + tmpFileName)
