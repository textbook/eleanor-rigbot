"""The code powering `@eleanorrigbot`_.

.. _@eleanorrigbot: https://twitter.com/eleanorrigbot

"""

from .authenticate import get_authentication
from .classify import phrase_matches
from .listen import RetweetListener

__author__ = 'Jonathan Sharpe'
__version__ = '0.0.1'
