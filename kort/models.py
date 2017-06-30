# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import logging

from sqlalchemy import Column, Unicode

from kort.helpers.algo import encode
from kort.helpers.sqla import Database, DBSession

log = logging.getLogger(__name__)
Base = Database.get()


class Links(Base):
    """
    Describe a kort entry.

    This model handles all kort entries.
    """

    url = Column(Unicode(255), nullable=False)
    # token can be null until we generate the next id
    token = Column(Unicode(255), nullable=True)

    @classmethod
    def by_token(cls, token):
        """Get entry for a given token."""
        return cls.first(where=((cls.token == token),))

    @classmethod
    def by_url(cls, url):
        """Get entry for a given url."""
        return cls.first(where=((cls.url == url),))

    @classmethod
    def new(cls, url):
        """Create new entry.
        - check if url is not already shortened in database
        - if yes return found entry
        - if not generate token for next insert id and create entry url+token
        """
        link = Links.by_url(url)
        if not link:
            # create Link object and flush session to retrieve id
            session = DBSession()
            link = cls(url=url)
            session.add(link)
            session.flush()
            token = encode(link.id)
            link.token = token
            log.info('Creating entry for %s: %s' % (url, token))
        return link

    def __repr__(self):
        return "<Link #%d: %s (%s)" % (self.id, self.url, self.token)
