#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from __future__ import absolute_import

from datetime import timedelta
from celery.schedules import crontab


# 指定 Broker
BROKER_URL = 'redis://127.0.0.1:6379'

# 指定 Backend
CELERY_RESULT_BACKEND = 'redis://127.0.0.1:6379/0'

# 指定时区
CELERY_TIMEZONE = 'Asia/Shanghai'

# 异步任务
CELERY_IMPORTS = (
#    'tasks.wechat_tmpl',
    'tasks.allinpay_tips',
#    'tasks.wechat_tokens'
)

# 定时任务
#CELERYBEAT_SCHEDULE = {
#    'refresh-token-every-1-hours': {
#        'task': 'tasks.wechat_tokens.refresh_token',
#        'schedule': timedelta(seconds=60*60)
#    }
#}
