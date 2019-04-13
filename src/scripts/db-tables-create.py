#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from __future__ import absolute_import

from core.database import con, get_session

import settings

def create_table():

    from domain import domains

    for table in con.metadata.tables:
        print ('创建{}表'.format(table))

    session = get_session(settings.DB_URL)

    con.metadata.create_all(bind=session.bind)

if __name__ == '__main__':

    create_table()

    print ('创建完成')
