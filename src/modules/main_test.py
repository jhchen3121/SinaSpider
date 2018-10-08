#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from __future__ import absolute_import

from sina_login import login
from user_msg_get import user_concern_msg_get
from user_msg_get import user_detail_msg_get
from user_msg_get import user_publish_msg_get

if __name__ == '__main__':

    session, user_id = login.user_login('xxx', 'xxx')

    #用户关注微博博主发表的内容
    #user_concern_msg_get.msg_get(session, user_id)

    #用户的详细信息
    #user_detail_msg_get.detail_msg_get(session, user_id)
    #user_detail_msg_get.user_concern_get(session, user_id)

    #用户自己发表的微博内容
    user_publish_msg_get.msg_get(session, user_id)

