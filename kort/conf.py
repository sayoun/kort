# -*- coding: utf-8 -*-
import os
from logging.config import dictConfig

import yaml
try:
    from yaml import CSafeLoader as YAMLLoader
except ImportError:
    from yaml import SafeLoader as YAMLLoader

from kort.helpers.sqla import init_engine


def configure(filename=None):
    conf = {}
    if not filename:
        configuration_file = '/etc/kort.yaml'
        if os.path.isfile(configuration_file):
            filename = configuration_file
    if filename:
        try:
            with open(filename) as fdesc:
                conf = yaml.load(fdesc, YAMLLoader)
        except IOError:
            print('Cannot load configuration file %s' % filename)

    if conf.get('logging'):
        dictConfig(conf.get('logging'))

    db_uri = conf.get('databases', {}).get('kort', {}).get('sqlalchemy.url')
    init_engine(db_uri, scoped=True)

    return conf
