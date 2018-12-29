import os
from datetime import datetime

from excel2xx import Excel
from unittest import TestCase
import tempfile
from openpyxl import Workbook

class TestDateTime(TestCase):
    def setUp(self):
        now = datetime.now()
        self.now = now

        wb = Workbook()
        sheet = wb.active
        sheet['A1'] = "test"
        sheet['A2'] = "string"
        sheet['A3'] = "测试下时间导出"
        sheet['A4'] = now
        sheet['A5'] = now.strftime("%d/%m/%Y %H:%M")

        dpath = tempfile.mkdtemp(prefix="excel2xx-testcase")
        fpath = f"{dpath}/sample.xlsx"
        wb.save(fpath)
        self.excel = Excel(fpath)
        pass


    def test_read(self):
        rows = list(self.excel[0])
        # self.assertEqual(1, rows[0]["test"])
        self.assertEqual(self.now.strftime("%d/%m/%Y %H:%M"), rows[1]["test"])
        pass


    def test_unixstamp(self):
        # text = "12/29/2018 7:15"
        dt = datetime.strptime("29/12/2018 15:15", "%d/%m/%Y %H:%M")
        print(dt)
        print(dt.astimezone())
        print(dt.timestamp())
        pass
