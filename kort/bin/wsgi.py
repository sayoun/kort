# -*- coding: utf-8 -*-
"""
WSGI application that serve Kort API
with the /etc/kort.yaml configuration file.
"""

# XXX please don't remove me, I'm the wsgi *application*
from kort.api import app as application
from kort.conf import configure


def main():
    conf = configure()
    application.secret_key = conf.get('secret_key', 's3cr3t3c00k!3k0rt')

main()
