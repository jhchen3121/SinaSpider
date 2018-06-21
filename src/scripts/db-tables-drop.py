#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from __future__ import absolute_import

from core.database import con, get_session

import settings

def drop_table():

    from domain import domain

    for table in con.metadata.tables:
        print ('删除{}表'.format(table))

    session = get_session(settings.DB_URL)

    try:
        con.metadata.reflect(bind=session.bind)

        con.metadata.drop_all(bind=session.bind, tables=con.metadata.sorted_tables)
    except:
        print ('表不存在，删除失败！')

if __name__ == '__main__':

    drop_table()

    print ('删除完毕')
