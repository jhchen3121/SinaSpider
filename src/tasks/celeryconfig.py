#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from __future__ import absolute_import

from kombu import Exchange, Queue

"""
celery 配置信息
"""

# 指定 Broker
BROKER_URL = 'redis://127.0.0.1:6379'

# 指定 Backend
CELERY_RESULT_BACKEND = 'redis://127.0.0.1:6379/0'

# 指定时区
CELERY_TIMEZONE = 'Asia/Shanghai'

# 异步任务
CELERY_IMPORTS = ( 
    'tasks.weibo_spider',
    'tasks.analysis'
)

#队列配置
default_exchange = Exchange('default', type='direct')
spider_exchange = Exchange('spider', type='direct')
analysis_exchange = Exchange('analysis', type='direct')

#队列定义
CELERY_QUEUES = (
    Queue('default', default_exchange, routing_key='default'),
    Queue('weibo_spider', spider_exchange, routing_key='tasks.weibo_spider'),
    Queue('analysis', analysis_exchange, routing_key='tasks.analysis'),
)

CELERY_DEFAULT_QUEUE = 'default'
CELERY_DEFAULT_EXCHANGE = 'default'
CELERY_DEFAULT_ROUTTING_KEY = 'default'

#配置路由，把不同任务分发至不同的队列
CELERY_ROUTES = {
    'tasks.weibo_spider.spider_msg_get': {
        'queue': 'weibo_spider',
        'routing_key': 'tasks.weibo_spider'
    },
    'tasks.analysis.analysis_test': {
        'queue': 'analysis',
        'routing_key': 'tasks.analysis'
    }
}

#任务过期时间
CELERY_TASK_RESULT_EXPIRES = 60 * 60 * 24

#防止死锁
CELERYD_FORCE_EXECV = True

#每个worker最多执行100各任务被销毁，防止内存泄漏
CELERYD_MAX_TASKS_PER_CHILD = 100

