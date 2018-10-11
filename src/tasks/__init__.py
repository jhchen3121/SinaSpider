# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from __future__ import absolute_import

from celery import Celery

# 创建 Celery 实例
app = Celery('tasks')

# 通过 Celery 实例加载配置模块
app.config_from_object('tasks.celeryconfig')
