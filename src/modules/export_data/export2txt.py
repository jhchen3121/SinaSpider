#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from __future__ import absolute_import

from core.database import get_session

import settings
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

"""
从本地数据库中导出数据
"""

def main():

    f = open('微博用户发表内容_jhchen.txt', 'w')

    session = get_session(settings.DB_URL)
    cursor = session.execute(""" select * from traning_collection """).cursor

    column = [c[0] for c in cursor.description]
    f.write('|'.join(column))
    f.write('\n')

    for res in cursor:
        cont = '{}|{}|{}|{}|{}|{}|{}\n'.format(*res)
        f.write(cont)

    f.close()

if __name__ == '__main__':
    main()
