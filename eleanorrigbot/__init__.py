"""The code powering `@eleanorrigbot`_.

.. _@eleanorrigbot: https://twitter.com/eleanorrigbot

"""
import logging

from tweepy import API, Stream

from .authenticate import get_authentication
from .classify import phrase_matches
from .listen import RetweetListener

# https://www.flickr.com/places/info/12695850
LIVERPOOL = [-3.0087, 53.3261, -2.8180, 53.4751]

logging.getLogger(__name__).addHandler(logging.NullHandler())

__author__ = 'Jonathan Sharpe'
__version__ = '0.0.1'


def start_listening():
    """Start listening to the Twitter stream in Liverpool."""
    api = API(get_authentication())

    listener = RetweetListener(api, phrase_matches)

    stream = Stream(auth=api.auth, listener=listener)
    stream.filter(locations=LIVERPOOL)
