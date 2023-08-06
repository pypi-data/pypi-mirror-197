# -*- coding: utf-8 -*-
import unittest.mock
import logging
import json
import sys
import random

try:
    import xmlrunner  # noqa
except ImportError:
    pass

try:
    from StringIO import StringIO  # noqa
except ImportError:
    # Python 3 Support
    from io import StringIO

sys.path.append('pysdl')
from src.pysdl import StackdriverJsonFormatter


class TestStackDriverFormatter(unittest.TestCase):
    def setUp(self):
        self.logger = logging.getLogger("logging-test-{}".format(random.randint(1, 101)))
        self.logger.setLevel(logging.DEBUG)
        self.buffer = StringIO()

        self.logHandler = logging.StreamHandler(self.buffer)
        self.logger.addHandler(self.logHandler)

    def testFormatKeys(self):
        supported_keys = [
            'asctime',
            'created',
            'filename',
            'funcName',
            'levelname',
            'levelno',
            # Only addition key added is severity
            'severity',
            'lineno',
            'module',
            'msecs',
            'message',
            'name',
            'pathname',
            'process',
            'processName',
            'relativeCreated',
            'thread',
            'threadName'
        ]

        log_format = lambda x: ['%({0:s})s'.format(i) for i in x]
        custom_format = ' '.join(log_format(supported_keys))

        fr = StackdriverJsonFormatter(custom_format)
        self.logHandler.setFormatter(fr)

        msg = "testing logging format"
        self.logger.info(msg)
        log_msg = self.buffer.getvalue()
        log_json = json.loads(log_msg)

        for supported_key in supported_keys:
            if supported_key in log_json:
                self.assertTrue(True)
