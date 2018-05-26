# -*- coding: utf-8 -*-
import os

###############################################################################
# 腾讯云的配置
QCLOUD_APP_ID = "1255979880"
QCLOUD_SECRET_ID = "AKIDJXaUDOuF8wZ1KaFtulQuDScgigaObNG4"
QCLOUD_SECRET_KEY = "rcHl4CXlphS2RozylNo493qUxJdpqfL7"
QCLOUD_BUCKET = "hzyhepark"

# 微信小程序相关配置
WECHAT_APP_ID = 'wx732c2cc252ccd7a8'
WECHAT_SECRET_KEY = "c9dc0d1bd7527654cc030ad259d85740"

# 微信模版消息配置项
WECHAT_PAY_TEMPLATE_ID = '1FgGEW7mQekymvn1-rQKeZ-ND1JXfaIcr2fja7nbUxg'      # 微信支付
CARD_PAY_TEMPLATE_ID = '1FgGEW7mQekymvn1-rQKeQC-MO_eRYTTRJq-I_EwQiA'        # 百合卡支付
SIGN_TEMPLATE_ID = '1FgGEW7mQekymvn1-rQKeUrAKwmFz1ZYuvh3Cz90tUE'            # 签约

CARD_PAY_TEMPLATE_TIPS = '感谢使用湖州银行百合卡'
CARD_PAY_TEMPLATE_PAGE = 'pages/index/index'

WECHAT_PAY_TEMPLATE_TIPS = '感谢使用湖州银行百合易停车'
WECHAT_PAY_TEMPLATE_PAGE = 'pages/index/index'

SIGN_TEMPLATE_TIPS = '欢迎使用湖州银行百合卡'
SIGN_TEMPLATE_PAGE = 'pages/index/index'

# 接口测试开关
DEBUG = True

# 银行卡与车牌最大绑定数
EPARK_BANKCARD_CAR_MAX_BIND_COUNT = 3
EPARK_CAR_BANKCARD_MAX_BIND_COUNT = -1  # -1 不限制

# 银行卡存放目录
base_dir = os.path.dirname(os.path.abspath(__file__))
BANKCARD_DIR= os.path.join(base_dir, '../images')
if not os.path.exists(BANKCARD_DIR):
    os.mkdir(BANKCARD_DIR)
###############################################################################

# 项目目录
PROJ_DIR = os.environ['PROJ_DIR']
# HOME目录
HOME_DIR = os.environ['HOME']

# 获取帆软报表地址
FINEREPORT_URL = ''

# 页面目录
STATIC_DIR = os.path.join(PROJ_DIR, 'web')

# 日志格式
LOG_FMT = '%(levelname) -6s %(asctime)s  %(filename)-20s %(lineno) -5d: %(message)s'

DB_URL = "oracle+cx_oracle://epark:epark@192.168.100.40:1521/dbutf"
# DB_URL = 'mysql+mysqldb://epark_user:epark_pwd@localhost/epark_db?charset=utf8'

MONGO_URL = "'mongodb://localhost:27017/'"

SECRET_KEY = '\xff\xc2+\xb2@T\x1c\n\x8b\xd7\x93\xf7\xaf\xf2R\x9b\xf0\xd2W\xba\xaa\xbe\xa6\x8b\xb8\xa2uQ\xe8E\x92\x8e\x8f\xdb\x95o!\x92\xe0\x02\xbf\xa9\x1fi\x87\xfe\x97F'
EXPIRES_IN = 60 * 100   # 60s * 100
MQ_URL = "amqp://guest:guest@127.0.0.1:5672/%2F"

ATTACHMENT_DIR = os.path.join(PROJ_DIR, 'attachments')

PLUGINS = 'plugins'
SAMPLES = 'services'
MODELS = 'domain'
MODELSOBJ = 'domain/model'
FRONT_SRV_PORT = 8900

EXCHANGE = 'hzyhpark.service.topic'
EXCHANGE_TYPE = 'topic'
QUEUE = 'hzyhpark.service.queue'
ROUTING_KEY = 'hzyhpark.service.#'
ROUTING_PREFIX = 'hzyhpark.service.'


def logConfig():
    import logging
    import sys
    logging.basicConfig(format=LOG_FMT, level=logging.INFO, stream=sys.stdout)
