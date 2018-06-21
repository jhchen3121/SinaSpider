#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from __future__ import absolute_import

from math import ceil
import datetime
from decimal import Decimal
from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm.session import sessionmaker
from sqlalchemy.orm import mapper, relationship, Query
from sqlalchemy import Table, Column, BigInteger, Integer, String, ForeignKey, Boolean, Date, DateTime,Text
from sqlalchemy.schema import Sequence
from sqlalchemy import func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.declarative import api 


import settings

Session=sessionmaker()
_session_pool = dict()

class connect(object):
    pass

con=connect()
con.metadata = MetaData()

def create_session(db_url, schema=None):
    if 'oracle' in db_url:
        engine = create_engine(db_url, coerce_to_unicode=True)
    elif 'mysql' in db_url:
        engine = create_engine(db_url, pool_recycle=600)
    else:
        engine = create_engine(db_url)
    metadata = MetaData(schema=schema)
    metadata.bind = engine
    connection = engine.connect()
    session=Session(bind=connection)
    return session


def get_session(db_url):
    '''
    相同的db_url只创建一个session
    '''
    if db_url not in _session_pool:
        session = create_session(db_url)
        _session_pool[db_url] = session
    return _session_pool[db_url]




class _QueryProperty(object):
    def __get__(self, instance, owner):
        session = owner.session()
        return BaseQuery(owner, session=session)

class DomainClass(object):

    query = _QueryProperty()

    def __init__(self, **kwargs):
        print kwargs

    @classmethod
    def is_session_exist(cls):
        session = cls.metadata.bind
        if session is None:
            raise NameError('数据库连接不存在')
        return session

    @classmethod
    def session(cls):
        return cls.is_session_exist()

    def get(self, idorcode=None):
        """ 按主键获取数据"""
        session = self.is_session_exist()
        if idorcode is not None:
            return session.query(self.__class__).get(idorcode)

        if hasattr(self, 'code'):
            return session.query(self.__class__).filter(self.__class__.code == self.code).one()
        else:
            return session.query(self.__class__).filter(self.__class__.id == self.id).one()

    def save(self):
        """ 保存当前数据"""
        session = self.is_session_exist()
        o =  session.add(self)
        session.flush()
        return self

    def update(self):
        """ 更新当前数据"""
        session = self.is_session_exist()
        o =  session.merge(self)
        session.flush()
        return self

    def refresh(self, attribute_names=None, lockmode=None):
        """ 刷新数据   """
        session = self.is_session_exist()
        session.refresh(self, attribute_names, lockmode)
        return self

    def to_dict(self, table = None, **kw):
        #继承时，自动加载父表的字段值
        d = dict()
        for cls in self.__class__.__bases__:
            if not hasattr(cls, '__table__'):
                break
            unmarshal = cls.__table__ 
            columns = kw.get('columns', map(lambda col:col.name, unmarshal.c))
            d.update(dict((col, _inner_convert(getattr(self, col))) for col in columns)  )

        unmarshal = table if table is not None else self.__table__ 
        columns = kw.get('columns', map(lambda col:col.name, unmarshal.c))
        d.update(dict((col, _inner_convert(getattr(self, col))) for col in columns)  )
        return d

    def marshal(self):
        columns = filter(lambda a:type(a) == unicode, [c for c in dir(self)])
        return dict((col, self._inner_convert(getattr(self, col))) for col in columns)  


    def _convert(self, d, k, func):
        if k in d and d[k] is not None:
            d[k] = func(d[k])

    def columns(self):
        '''
        返回表中的column name
        '''
        return [c.name for c in self.__table__.c]

    # 拷贝对象字段
    def dup(self, saved=False, deleted=True):
        data = self.to_dict()

        if hasattr(self, 'code'):
            del data['code']
        if hasattr(self, 'id'):
            del data['id']

        if hasattr(self, 'update_date'):
            del data['update_date']
        else:
            if hasattr(self, 'from_date'):
                del data['from_date']

        if hasattr(self, 'thru_date'):
            del data['thru_date']

        cls = self.__class__
        obj = cls(**data)
        if saved:
            obj.save()

        if deleted:
            self.logic_del()

        return obj

    # 逻辑删除记录
    def logic_del(self):
        if hasattr(self, 'thru_date'):
            self.thru_date = datetime.now()
            self.update()

class Pagination(object):
    def __init__(self, query, page, per_page, total, items):
        self.page = page
        self.per_page = per_page
        self.query = query
        self.total = total
        self.items = items

    @property
    def pages(self):
        """The total number of pages"""
        if self.per_page == 0:
            pages = 0
        else:
            pages = int(ceil(self.total / float(self.per_page)))
        return pages

    @property
    def has_prev(self):
        return self.page > 1

    @property
    def has_next(self):
        """True if a next page exists."""
        return self.page < self.pages

    def to_dict(self):
        d = dict()
        d['pages'] = self.pages
        d['items'] = [self.item_to_dict(item) for item in self.items]
        d['per_page'] = self.per_page
        d['total'] = self.total
        d['page'] = self.page
        d['has_prev'] = self.has_prev
        d['has_next'] = self.has_next
        return d

    @staticmethod
    def item_to_dict(item):
        if hasattr(item, 'to_dict'):
            return item.to_dict()
        elif hasattr(item, '_fields'):
            return  {f: _inner_convert(getattr(item, f)) for f in item._fields} 
        elif hasattr(item, '__table__'):
            return  {c.name: _inner_convert(getattr(item, c.name)) for c in item.__table__.columns} 

class BaseQuery(Query):
    def paginate(self, page=None, per_page=None):
        if page is None:
            page = 1
        if per_page is None:
            per_page = 20

        page = int(page)
        per_page = int(per_page)

        items = self.limit(per_page).offset((page - 1) * per_page).all()
        if page == 1 and len(items) < per_page:
            total = len(items)
        else:
            total = self.order_by(None).count()
            #total = self.with_entities(func.count()).scalar()
        return Pagination(self, page, per_page, total, items)


def _inner_convert(v):
    if type(v) == datetime.datetime:
        return v.isoformat()
    elif type(v) == datetime.date:
        return v.strftime('%Y-%m-%d')
    elif isinstance(v, Decimal):
        return str(v)
    else:
        return v

DomainBase = declarative_base(cls = DomainClass)
