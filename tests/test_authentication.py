from unittest.mock import call, patch

from eleanorrigbot import get_authentication

ENV = dict(
    TWITTER_API_KEY='consumer_key',
    TWITTER_API_SECRET='consumer_secret',
    TWITTER_ACCESS_TOKEN='access_token',
    TWITTER_ACCESS_TOKEN_SECRET='access_token_secret',
)


@patch('eleanorrigbot.authenticate.getenv', side_effect=ENV.get)
@patch('eleanorrigbot.authenticate.OAuthHandler')
def test_oauth_creation(mock_oauth, mock_getenv):
    assert get_authentication() is mock_oauth.return_value
    mock_oauth.assert_called_once_with(
        ENV['TWITTER_API_KEY'],
        ENV['TWITTER_API_SECRET']
    )
    mock_oauth.return_value.set_access_token.assert_called_once_with(
        ENV['TWITTER_ACCESS_TOKEN'],
        ENV['TWITTER_ACCESS_TOKEN_SECRET'],
    )
    mock_getenv.assert_has_calls([call(key) for key in ENV], any_order=True)
