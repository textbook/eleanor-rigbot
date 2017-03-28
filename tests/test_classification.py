import pytest

from eleanorrigbot import phrase_matches


@pytest.mark.parametrize('input_, output', [
    ('hello world', False),

    # actual quotes from the song
    ('waits at the window wearing the face that she keeps in a jar by '
     'the door who is it for', True),
    ('eleanor rigby died in the church and was buried along with her '
     'name nobody came', True),
    ('father mckenzie wiping the dirt from his hands as he walks from '
     'the grave no one was saved', True),

    # the project slogan, with missing words tweaked
    ('eleanor rigby searching for tweet that will fit in the scheme of '
     'this rhyme what will it find', True),

    # the source of pronunciations doesn't know about "darning"
    ('look at him working darning his socks in the night when there\'s '
     'nobody there what does he care', False),

    # rhyming is difficult apparently - IH vs. IY
    ('eleanor rigby picks up the rice in the church where a wedding has '
     'been lives in a dream', False),
    ('father mckenzie writing the words of a sermon that no one will '
     'hear no one comes near', False),

    # 22 syllables, but across sub-phrase breaks
    ('concatenate banana terrible alpha bravo charlie delta echo '
     'foxtrot', False),

    # 22 syllables in correct pattern but doesn't rhyme
    ('eleanor rigby picks up the rice in the church where a wedding has '
     'been lives in a cart', False),
])
def test_phrase_classification(input_, output):
    assert phrase_matches(input_) == output
