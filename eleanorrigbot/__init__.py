"""The code powering `@eleanorrigbot`_.

.. _@eleanorrigbot: https://twitter.com/eleanorrigbot

"""
import logging

from .authenticate import get_authentication
from .classify import phrase_matches
from .listen import RetweetListener

logging.getLogger(__name__).addHandler(logging.NullHandler())

__author__ = 'Jonathan Sharpe'
__version__ = '0.0.1'
