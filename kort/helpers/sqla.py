import re
import logging

import sys

from sqlalchemy import Column, Integer, DateTime, create_engine
from sqlalchemy.sql.expression import func
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.orm.attributes import QueryableAttribute
from sqlalchemy.ext.declarative import declared_attr, declarative_base

if sys.version_info[0] > 2:
    basestring = (str, bytes)

log = logging.getLogger(__name__)


class _Base(object):

    @declared_attr
    def __tablename__(cls):  # noqa
        # CamelCase to underscore cast
        s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', cls.__name__)
        return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()

    __table_args__ = {'mysql_engine': 'InnoDB',
                      'mysql_charset': 'utf8'
                      }

    @property
    def session(self):
        return DBSession().get_object_session(self)

    id = Column(Integer, primary_key=True)
    created_at = Column(DateTime, default=func.now())

    @classmethod
    def by_id(cls, id):
        return cls.first(where=(cls.id == id,))

    @classmethod
    def find(cls, join=None, where=None, order_by=None, limit=None,
             offset=None, count=False):
        if count:
            offset = limit = order_by = None  # XXX posgresql doesn't like it
        qry = cls.build_query(join, where, order_by, limit,
                              offset, count)
        return qry.scalar() if count else qry.all()

    @classmethod
    def first(cls, join=None, where=None, order_by=None):
        return cls.build_query(join, where, order_by).first()

    @classmethod
    def all(cls, page_size=1000, order_by=None):
        session = DBSession()
        offset = 0
        order_by = order_by or cls.id
        while True:
            page = cls.find(order_by=order_by,
                            limit=page_size, offset=offset)
            for m in page:
                yield m
            session.flush()
            if len(page) != page_size:
                raise StopIteration()
            offset += page_size

    @classmethod
    def build_order_by(cls, order_by):
        sa_order_by = []
        if not isinstance(order_by, (list, tuple)):
            order_by = [order_by]
        for field in order_by:
            if isinstance(field, basestring):
                desc_ = field.startswith('-')
                if desc_:
                    field = field[1:]

                # XXX Do we create own exception here ?
                attr = getattr(cls, field)  # raise AttributeError
                if not isinstance(attr, QueryableAttribute):
                    raise ValueError('%s is not a sortable field of %s' %
                                     (field, cls))
                field = attr.desc() if desc_ else attr
            sa_order_by.append(field)
        return sa_order_by

    @classmethod
    def build_query(cls, join=None, where=None, order_by=None,
                    limit=None, offset=None, count=False):
        session = DBSession()
        if count:
            query = session.query(func.count(count)).select_from(cls)
        else:
            query = session.query(cls)

        if join:
            if isinstance(join, (list, tuple)):
                for j in join:
                    if isinstance(j, (list, tuple)):
                        query = query.join(*j)
                    else:
                        query = query.join(j)
            else:
                query = query.join(join)

        if where:
            for filter in where:
                query = query.filter(filter)

        if order_by is not None:
            order_by = cls.build_order_by(order_by)
            if isinstance(order_by, (list, tuple)):
                query = query.order_by(*order_by)
            else:
                query = query.order_by(order_by)
        if limit:
            query = query.limit(limit)
        if offset:
            query = query.offset(offset)
        return query

    def validate(self, session):
        """
        return True or raise a :class:`ModelError` Exception
        """
        return True

    def delete(self):
        self.session.delete(self)

    def __repr__(self):
        """String representation of a model."""
        cls = self.__class__
        repr_ = '%s.%s' % (cls.__module__, cls.__name__)

        if hasattr(self, 'id'):
            repr_ += ' #%s' % self.id

        return '<%s>' % repr_

    __str__ = __repr__

    def __iter__(self):
        attrs = sorted(dir(self))
        for attr in attrs:
            if attr.startswith('_'):
                continue
            val = getattr(self, attr)
            if val is None:
                continue
            yield attr, val

    def pop(self, name, *args):
        """
        Trick colander dict validator (which is using dict.pop(),
        values aren't actually removed (because they can be properties)

        The pop is useless in our case (unknown key is always set to ignore)

        """

        return getattr(self, name, *args)

    def items(self):
        return dict(self).items()

    def __contains__(self, item):
        return hasattr(self, item)

    def __getitem__(self, item):
        return getattr(self, item)


class DBSession(object):
    """DBSession class singleton."""
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            raise RuntimeError('DBSession is not initialized')

        return cls._instance

    @classmethod
    def configure(cls, engine, scoped):
        if scoped:
            cls._instance = scoped_session(sessionmaker(bind=engine))
        else:
            cls._instance = sessionmaker(bind=engine)
        return cls._instance

    @classmethod
    def get_object_session(cls, object_):
        try:
            return cls._instance.object_session(object_)
        except KeyError:
            return None

    @classmethod
    def dispose(cls):
        try:
            return cls._instance.close()
        except:
            pass


class Database(object):
    """Database Base class."""
    _instance = None

    @classmethod
    def get(cls):
        if not cls._instance:
            cls._instance = declarative_base(cls=_Base)
        return cls._instance

    @classmethod
    def configure(cls, engine):
        instance = cls.get()
        instance.metadata.bind = engine
        # Create all tables in the engine. This is equivalent to "Create Table"
        # statements in raw SQL.
        from kort import models # noqa
        instance.metadata.create_all(engine)

    @classmethod
    def dispose(cls):
        try:
            instance = cls.get()
            instance.metadata.bind.dispose()
        except:
            pass


def init_engine(db_uri=None, scoped=False):
    engine = create_engine(db_uri or 'sqlite:///kort.db')
    DBSession.configure(engine, scoped)
    Database.configure(engine)
    return engine


def dispose_engine():
    DBSession.dispose()
    Database.dispose()
