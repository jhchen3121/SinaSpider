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

#traning set
traning_collection = Table('traning_collection', con.metadata,
    Column('id', BigInteger, Sequence('traning_collection_seq'), primary_key=True),

    Column('user_id', String(128), doc="用户id"),
    Column('user_name', String(256), doc="用户名"),
    Column('content', String(2048), doc="发表内容"),
    Column('publish_date', String(60), doc='发表时间'),

    Column('from_time', DateTime, doc="创建时间"),
    Column('thru_time', DateTime, doc="删除时间"),
)

# 用户基本信息
ss_sina_user_detail = Table('ss_sina_user_detail', con.metadata,
    
    Column('id', BigInteger, Sequence('ss_sina_user_detail_seq'), primary_key=True),

    Column('user_id', String(128), doc="用户id"),
    Column('user_name', String(256), doc="用户名"),
    Column('sex', String(16), doc="性别"),
    Column('user_address', String(128), doc="地址"),
    Column('constellation', String(64), doc="星座"),
    Column('sexual_orientation', String(32), doc="性取向"),
    Column('relationship', String(32), doc="情感状况"),
    Column('fans_count', BigInteger, doc="粉丝数目"),
    Column('weibo_publish_count', BigInteger, doc="微博发表数目"),
    Column('concern_count', BigInteger, doc="关注数"),
    
    Column('from_time', DateTime, doc="创建时间"),
    Column('thru_time', DateTime, doc="删除时间"),
)

# 用户关注人列表
ss_sina_user_concern = Table('ss_sina_user_concern', con.metadata,

    Column('id', BigInteger, Sequence('ss_sina_user_concern_seq'), primary_key=True),

    Column('user_id', String(128), doc="用户id"),
    Column('concern_id', String(128), doc="关注人id"),

    Column('from_time', DateTime, doc="创建时间"),
    Column('thru_time', DateTime, doc="删除时间"),
)

# 情感分析结果
ss_analyse_result = Table('ss_analyse_result', con.metadata,

    Column('id', BigInteger, Sequence('ss_analyse_result_seq'), primary_key=True),

    Column('user_id', String(128), doc="用户id"),
    Column('user_name', String(256), doc="用户名"),
    Column('rate', BigInteger, doc="情感分析结果"),
    Column('content', String(2048), doc="发表内容"),

    Column('from_time', DateTime, doc="创建时间"),
    Column('thru_time', DateTime, doc="删除时间"),
)

