from mock import patch
import pytest

from eleanorrigbot import get_authentication

ENV = dict(
    TWITTER_API_KEY='consumer_key',
    TWITTER_API_SECRET='consumer_secret',
    TWITTER_ACCESS_TOKEN='access_token',
    TWITTER_ACCESS_TOKEN_SECRET='access_token_secret',
)


@patch('eleanorrigbot.authenticate.getenv', side_effect=ENV.__getitem__)
@patch('eleanorrigbot.authenticate.OAuthHandler')
def test_oauth_creation(mock_oauth, _):
    assert get_authentication() is mock_oauth.return_value
    mock_oauth.assert_called_once_with(
        ENV['TWITTER_API_KEY'],
        ENV['TWITTER_API_SECRET']
    )
    mock_oauth.return_value.set_access_token.assert_called_once_with(
        ENV['TWITTER_ACCESS_TOKEN'],
        ENV['TWITTER_ACCESS_TOKEN_SECRET'],
    )


@patch('eleanorrigbot.authenticate.getenv', side_effect=KeyError)
@patch('eleanorrigbot.authenticate.logger')
def test_create_logging(mock_logger, _):
    with pytest.raises(KeyError):
        get_authentication()

    mock_logger.exception.assert_called_once()


@patch(
    'eleanorrigbot.authenticate.getenv',
    side_effect=dict(TWITTER_API_KEY='foo', TWITTER_API_SECRET='bar').__getitem__
)
@patch('eleanorrigbot.authenticate.logger')
def test_set_token_logging(mock_logger, _):
    with pytest.raises(KeyError):
        get_authentication()

    mock_logger.exception.assert_called_once()
