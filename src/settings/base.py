# -*- coding: utf-8 -*-
import os

###############################################################################
# 接口测试开关
DEBUG = True

# 项目目录
PROJ_DIR = os.environ['PROJ_DIR']
# HOME目录
HOME_DIR = os.environ['HOME']

# 页面目录
STATIC_DIR = os.path.join(PROJ_DIR, 'web')

# 日志格式
LOG_FMT = '%(levelname) -6s %(asctime)s  %(filename)-20s %(lineno) -5d: %(message)s'

#DB_URL = "oracle+cx_oracle://epark:epark@192.168.100.40:1521/dbutf"
#DB_URL = 'mysql+mysqldb://epark_user:epark_pwd@localhost/epark_db?charset=utf8'
DB_URL = 'mysql+mysqldb://sinaspider:sinaspider@localhost/sinaspiderdb?charset=utf8'

MONGO_URL = "'mongodb://localhost:27017/'"

EXPIRES_IN = 60 * 100   # 60s * 100
MQ_URL = "amqp://guest:guest@127.0.0.1:5672/%2F"

ATTACHMENT_DIR = os.path.join(PROJ_DIR, 'attachments')

PLUGINS = 'plugins'
SAMPLES = 'services'
MODELS = 'domain'
MODELSOBJ = 'domain/model'
FRONT_SRV_PORT = 8900

EXCHANGE = 'sinaspider.service.topic'
EXCHANGE_TYPE = 'topic'
QUEUE = 'sinaspider.service.queue'
ROUTING_KEY = 'sinaspider.service.#'
ROUTING_PREFIX = 'sinaspider.service.'


def logConfig():
    import logging
    import sys
    logging.basicConfig(format=LOG_FMT, level=logging.INFO, stream=sys.stdout)
