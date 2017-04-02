from mock import patch
import pytest

from eleanorrigbot import phrase_matches


@pytest.mark.parametrize('input_, output', [
    ('hello world', False),

    # actual quotes from the song
    ('waits at the window wearing the face that she keeps in a jar by '
     'the door who is it for', True),
    ('eleanor rigby died in the church and was buried along with her '
     'name nobody came', True),

    # the source of pronunciations doesn't know about "darning"
    ('look at him working darning his socks in the night when there\'s '
     'nobody there what does he care', False),

    # rhyming is difficult apparently
    ('eleanor rigby picks up the rice in the church where a wedding has '
     'been lives in a dream', False),
    ('father mckenzie writing the words of a sermon that no one will '
     'hear no one comes near', False),
    ('father mckenzie wiping the dirt from his hands as he walks from '
     'the grave no one was saved', False),

    # 22 syllables, but across sub-phrase breaks
    ('concatenate banana terrible alpha bravo charlie delta echo '
     'foxtrot', False),

    # 22 syllables in correct pattern but doesn't rhyme
    ('eleanor rigby picks up the rice in the church where a wedding has '
     'been lives in a cart', False),
])
def test_phrase_classification(input_, output):
    assert phrase_matches(input_) == output


@patch('eleanorrigbot.classify.logger')
def test_logging(mock_logger):
    text = ('over wing exit leaving the plane as it falls like a stone from '
            'the sky final goodbye')
    phrase_matches(text)
    mock_logger.debug.assert_called_once_with(
        'processing %s-syllable tweet: %r',
        22,
        [
            ('over', 2), ('wing', 1), ('exit', 2), ('leaving', 2), ('the', 1),
            ('plane', 1), ('as', 1), ('it', 1), ('falls', 1), ('like', 1),
            ('a', 1), ('stone', 1), ('from', 1), ('the', 1), ('sky', 1),
            ('final', 2), ('goodbye', 2),
        ]
    )

    mock_logger.info.assert_called_once_with(
        'tweet matches syllable pattern: %r',
        [
            ['over', 'wing', 'exit'],
            ['leaving', 'the', 'plane'],
            ['as', 'it', 'falls', 'like', 'a', 'stone', 'from', 'the', 'sky'],
            ['final', 'goodbye'],
        ]
    )
