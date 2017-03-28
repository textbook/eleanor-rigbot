"""Authenticate application from environment variables."""

from os import getenv

from tweepy import OAuthHandler


def get_authentication():
    """Create the Tweepy authentication object."""
    consumer_key = getenv('TWITTER_API_KEY')
    consumer_secret = getenv('TWITTER_API_SECRET')
    auth = OAuthHandler(consumer_key, consumer_secret)

    key = getenv('TWITTER_ACCESS_TOKEN')
    secret = getenv('TWITTER_ACCESS_TOKEN_SECRET')
    auth.set_access_token(key, secret)

    return auth
