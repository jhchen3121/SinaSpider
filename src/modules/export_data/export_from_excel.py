#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from __future__ import absolute_import

"""
从excel中读取文件
"""

import settings
import xlrd
import os
import sys

reload(sys)
sys.setdefaultencoding('utf-8')

def main():

    f1 = open('negitive.txt', 'w')
    f2 = open('positive.txt', 'w')

    excel_path = os.path.join(settings.DATA_DIR, '原始词库/大连理工大学情感词汇本体库.xlsx')

    workbook = xlrd.open_workbook(excel_path)
    # 获取所有sheet
    sheet = workbook.sheet_by_index(0)

    for i in range(sheet.nrows-1):
        word = sheet.cell(i+1, 0).value
        rate = int(sheet.cell(i+1, 6).value)


        if rate == 2:
            f1.write('-1###{}\n'.format(word))
        elif rate == 1:
            f2.write('1###{}\n'.format(word))

    f1.close()
    f2.close()

if __name__ == '__main__':
    main()
