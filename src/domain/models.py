#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from __future__ import absolute_import

from core.database import DomainBase

from domain import domains

class SinaUser(DomainBase):
    __table__ = domains.ss_sina_user

class TraningCollection(DomainBase):
    __table__ = domains.traning_collection

class Sina_user_detail(DomainBase):
    __table__ = domains.ss_sina_user_detail

class Analyse_result(DomainBase):
    __table__ = domains.ss_analyse_result
