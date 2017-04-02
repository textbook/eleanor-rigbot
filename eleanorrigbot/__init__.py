"""The code powering `@eleanorrigbot`_.

.. _@eleanorrigbot: https://twitter.com/eleanorrigbot

"""
import logging

from tweepy import API, Stream

from .authenticate import get_authentication
from .classify import PhraseMatcher
from .extract import extract_phrase
from .listen import RetweetListener
from .parse_args import parse_args, __version__

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())

__author__ = 'Jonathan Sharpe'

ELEANOR_RIGBY = PhraseMatcher(
    syllable_pattern=(5, 4, 9, 4),
    rhyming_scheme=(None, None, 0, 0),
)
"""Whether the phrase matches the Eleanor Rigby scheme.

The rules for the scheme are as follows:

 1. Must contain exactly 22 syllables

 2. Must divide into 5, 4, 9 and 4 syllables on word breaks

 3. Last two lines (9 syllables and 4 syllables) must rhyme

"""


def start_listening(location, filterer=ELEANOR_RIGBY):
    """Start listening to the Twitter stream at the given location."""
    auth = get_authentication()

    listener = RetweetListener(
        api=API(auth),
        extractor=extract_phrase,
        filterer=filterer
    )

    stream = Stream(auth=auth, listener=listener)

    logger.info('starting to listen to the stream at %r', location)
    stream.filter(locations=location)
