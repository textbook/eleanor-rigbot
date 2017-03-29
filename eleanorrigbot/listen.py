"""Functionality for listening to the Twitter stream."""
import logging

from tweepy import StreamListener

logger = logging.getLogger(__name__)


def _match_all(_):
    return True


class RetweetListener(StreamListener):
    """Listens to the Twitter stream and retweets matching statuses."""

    def __init__(self, api=None, filterer=_match_all):
        super(RetweetListener, self).__init__(api)
        self.filterer = filterer

    def on_status(self, status):
        """Called when a new status is streamed."""
        logger.debug('received %r %r', status.id, status.text)
        if self.filterer(status.text.lower()):
            logger.info('retweeting %r %r', status.id, status.text)
            self.api.retweet(status.id)

    def on_error(self, status_code):
        """Called when an error occurs."""
        logger.error('streaming error %s', status_code)
        return super().on_error(status_code)
