#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from __future__ import absolute_import

from tasks import app
from datetime import datetime

'''
用于通联支付交互

'''


@app.task
def send_pay_result():
    """
    告知通联支付结果
    """
    pass
#    pay_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

#    data = dict(orderNo=order_no, transeState=transe_state,
#                payType=pay_type, payTime=pay_time)

#    allinpay.send_pay_result(**data)


@app.task
def handle_pushed_order():
    """
    处理通联推送的订单
    """

    pass
    # 参数转换

    # 存入核心
#    res = core.pay_parking_fee(**data)
#    if res.code != 0:
#        return

    # 核心代扣成功，返回代扣卡号
#    card_no = res.pay_account

    # 存入前置数据库
#    db.pay_parking_fee_by_card_dk(card_no, **data)

 #   order_no = data.get('order_no') # 订单号
#    transe_state = 0                # 代扣成功
#    pay_type = 'DF'                 # 代付

    # 支付结果告知通联
#    pay_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
#    data = dict(orderNo=order_no, transeState=transe_state,
#                payType=pay_type, payTime=pay_time)

#    allinpay.send_pay_result(**data)
