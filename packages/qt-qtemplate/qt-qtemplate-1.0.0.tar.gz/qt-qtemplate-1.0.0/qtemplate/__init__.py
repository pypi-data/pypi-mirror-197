# -*- coding: utf-8 -*-
import logging
import sys

VERSION = '1.0.0'


# Custom logging formatter
class MyFormatter(logging.Formatter):
    def format(self, record):
        if 'module' in record.__dict__.keys():
            record.module = record.module[:10]
        return super(MyFormatter, self).format(record)


# Logging configuration
log = logging.getLogger(__name__)
logformat = MyFormatter('%(asctime)s %(module)10s:%(lineno)-4s %(levelname)-7s %(message)s')
streamhandler = logging.StreamHandler(sys.stdout)
streamhandler.setFormatter(logformat)
log.addHandler(streamhandler)
log.setLevel(logging.INFO)


# Load classes here to make import paths easier
from qtemplate.qtemplate import QTemplateWidget  # noqa
from qtemplate.base import QTemplateTag  # noqa
from qtemplate.datastore import DataStore  # noqa
