"""Functionality for listening to the Twitter stream."""
import logging
from time import sleep

from tweepy import StreamListener

logger = logging.getLogger(__name__)


def _match_all(_):
    return True


def _all_text(text):
    return text


class RetweetListener(StreamListener):
    """Listens to the Twitter stream and retweets matching statuses."""

    def __init__(self, api=None, extractor=_all_text, filterer=_match_all):
        super().__init__(api)
        self.extractor = extractor
        self.filterer = filterer
        self.timeout = 1

    def on_connect(self):
        """Called when a connection is made."""
        self.timeout = 1
        return super().on_connect()

    def on_status(self, status):
        """Called when a new status is streamed."""
        text = self._get_text(status)
        logger.debug(
            'received %r from @%s: %r',
            status.id,
            status.author.screen_name,
            text,
        )
        if self.filterer(self.extractor(text)):
            logger.info('retweeting %r %r', status.id, text)
            self.api.retweet(status.id)
        return super().on_status(status)

    def on_error(self, status_code):
        """Called when an error occurs."""
        logger.error('streaming error %s', status_code)
        if status_code == 420:
            timeout = self.timeout * 60
            logger.info('timing out for %s seconds', timeout)
            sleep(self.timeout * 60)
            self.timeout *= 2  # exponential back-off
        return super().on_error(status_code)

    @staticmethod
    def _get_text(status):
        try:
            return status.extended_tweet['full_text']
        except (AttributeError, KeyError):
            return status.text
