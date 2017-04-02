"""The code powering `@eleanorrigbot`_.

.. _@eleanorrigbot: https://twitter.com/eleanorrigbot

"""
import logging

from tweepy import API, Stream

from .authenticate import get_authentication
from .classify import phrase_matches
from .extract import extract_phrase
from .listen import RetweetListener
from .parse_args import parse_args, __version__

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())

__author__ = 'Jonathan Sharpe'


def start_listening(location):
    """Start listening to the Twitter stream at the given location."""
    auth = get_authentication()

    listener = RetweetListener(
        api=API(auth),
        extractor=extract_phrase,
        filterer=phrase_matches
    )

    stream = Stream(auth=auth, listener=listener)

    logger.info('starting to listen to the stream at %r', location)
    stream.filter(locations=location)
