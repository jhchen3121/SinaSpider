#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from __future__ import absolute_import

import logging
import traceback
import inspect
import settings

from functools import wraps, partial, update_wrapper
from core.database import get_session, DomainBase

logger = logging.getLogger(__name__)

def build_args(session, args, kw, func):
    arg_key_list = inspect.getargspec(func)[0]

    assert len(kw) + len(args) + 1 == len(arg_key_list), b'参数个数不正确，期望:{}, 实际:{}'.format(len(arg_key_list), len(kw) + len(args) + 1)

    new_args = []
    i = 0
    for key in arg_key_list:
        if key == "session":
            new_args.append(session)
            continue
        if key in kw:
            new_args.append(kw.get(key))
        new_args.append(args[i])
        i = i + 1
    return new_args, kw

def with_session(db_url=None, tx=False):
    def session_decoder(func):
        def _get_session(*args, **kw):
            url = db_url or settings.DB_URL
            arg_key_list = inspect.getargspec(func)[0]
            if arg_key_list and arg_key_list[0] == 'self':
                self = args[0]
                url = getattr(self, 'db_url', url)

            session = get_session(url)
            DomainBase.metadata.bind = session
            return session

        def wrapper(*args, **kw):
            result = None
            session = _get_session(*args, **kw)

            try:
                args, kw = build_args(session, args, kw, func)
                result = func(*args)
                if tx:
                    session.commit()
                else:
                    session.rollback()
            except Exception, ex:
                session.rollback()
                logger.error(traceback.format_exc())
                raise ex 
            return result

        update_wrapper(wrapper, func)

        return wrapper
    return session_decoder

