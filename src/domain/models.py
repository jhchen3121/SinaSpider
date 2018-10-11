#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from __future__ import absolute_import

from core.database import DomainBase

from domain import domain

class SinaUser(DomainBase):
    __table__ = domain.ss_sina_user

class TraningCollection(DomainBase):
    __table__ == domain.traning_collection

class Sina_user_detail(DomainBase):
    __table__ == domain.ss_sina_user_detail
