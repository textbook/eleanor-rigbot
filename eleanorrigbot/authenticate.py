"""Authenticate application from environment variables."""
import logging
from os import getenv

from tweepy import OAuthHandler

logger = logging.getLogger(__name__)


def get_authentication():
    """Create the Tweepy authentication object."""
    auth = _create_handler()
    _set_token(auth)
    return auth


def _create_handler():
    """Create an OAuth handler."""
    try:
        consumer_key = getenv('TWITTER_API_KEY')
        consumer_secret = getenv('TWITTER_API_SECRET')
    except KeyError:
        logger.exception('missing consumer authentication parameter')
        raise
    return OAuthHandler(consumer_key, consumer_secret)


def _set_token(auth):
    """Set the access token."""
    try:
        key = getenv('TWITTER_ACCESS_TOKEN')
        secret = getenv('TWITTER_ACCESS_TOKEN_SECRET')
    except KeyError:
        logger.exception('missing access token authentication parameter')
        raise
    auth.set_access_token(key, secret)
