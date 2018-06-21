#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from __future__ import absolute_import

from core.database import *
from datetime import datetime

ss_sina_user = Table('ss_sina_user', con.metadata,

    Column('id', BigInteger, Sequence('sina_user_seq'), primary_key=True),
    Column('username', String(128), doc='新浪用户用户名'),
    Column('passwd', String(128), doc='新浪用户密码（哈希处理）'),

    Column('from_time', DateTime, default=datetime.now, doc="创建时间"),
    Column('thru_time', DateTime, doc="删除时间"),

)
