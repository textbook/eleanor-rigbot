from unittest.mock import Mock, patch
import pytest
from tweepy import API, Status, User

from eleanorrigbot import RetweetListener


@pytest.fixture
def api():
    return Mock(autospec=API)


def create_tweet(id_, text, username):
    tweet = Mock(autospec=Status)
    tweet.id = id_
    tweet.text = text
    tweet.author = Mock(autospec=User)
    tweet.author.screen_name = username
    return tweet


def test_listener_match(api):
    filterer = Mock(return_value=True)
    extractor = Mock(return_value='hello world')

    listener = RetweetListener(api=api, extractor=extractor, filterer=filterer)

    listener.on_status(create_tweet(123, 'foo bar baz', 'ClaraCoventry'))
    filterer.assert_called_once_with('hello world')
    extractor.assert_called_once_with('foo bar baz')
    api.retweet.assert_called_once_with(123)


def test_listener_no_match(api):
    filterer = Mock(return_value=False)

    listener = RetweetListener(api, filterer=filterer)

    listener.on_status(create_tweet(123, 'hello world', 'BobBurnquist'))
    filterer.assert_called_once_with('hello world')
    api.retweet.assert_not_called()


@patch('eleanorrigbot.listen.logger')
def test_logging(mock_logger, api):
    listener = RetweetListener(api)

    listener.on_status(create_tweet(456, 'foo', 'AliceAnderson'))
    mock_logger.debug.assert_called_once_with(
        'received %r from @%s: %r',
        456,
        'AliceAnderson',
        'foo',
    )
    mock_logger.info.assert_called_once_with('retweeting %r %r', 456, 'foo')


@patch('eleanorrigbot.listen.logger')
def test_error_logging(mock_logger, api):
    listener = RetweetListener(api)

    listener.on_error(404)
    mock_logger.error.assert_called_once_with('streaming error %s', 404)


@patch('eleanorrigbot.listen.sleep')
@patch('eleanorrigbot.listen.logger')
def test_backoff(mock_logger, mock_sleep, api):
    listener = RetweetListener(api)
    listener.timeout = 4

    listener.on_error(420)
    mock_logger.info.assert_called_once_with('timing out for %s seconds', 240)
    mock_sleep.assert_called_once_with(240)

    assert listener.timeout == 8


def test_timeout_reset(api):
    listener = RetweetListener(api)
    listener.timeout = 8

    listener.on_connect()

    assert listener.timeout == 1
