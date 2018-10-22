#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from __future__ import absolute_import

from domain.models import SinaUserDetail
from domain.models import TraningCollection
from domain.models import SinaUserConcern

from core.helpers import with_session

'''
数据库操作
'''

@with_session(tx=True)
def insert_user_detail(session, data):
    ''' 插入用户详细信息 '''

    SinaUserDetail.Create(data)

@with_session(tx=True)
def insert_user_publish(session, data, user_detail):
    ''' 
    插入用户发表的内容 
    :param data(type([{},{},...]))
    '''
    
    user_id = user_detail.get('user_id')
    user_name = user_detail.get('user_name')

    for each_res in data:
        each_res.update(user_id=user_id, user_name=user_name)
        TraningCollection.Create(each_res)

@with_session(tx=True)
def insert_user_concern(session, data, user_detail):
    '''
    插入用户关注人列表
    '''

    SinaUserConcern.Create(data, user_detail)
