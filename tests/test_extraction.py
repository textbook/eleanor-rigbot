import pytest

from eleanorrigbot import extract_phrase


@pytest.mark.parametrize('input_, output', [
    (
        'have you seen our baking bags for easter, filled with all the dry '
        'ingredients to make the most delicious easter roc\u2026 '
        'https://t.co/md75ifzqw6',
        'have you seen our baking bags for easter filled with all the dry '
        'ingredients to make the most delicious easter'
    ),
    (
        '@KarenDanczuk good morning KD, how are you this wet morning '
        '\U0001f48b\U0001f48b',
        'good morning kd how are you this wet morning'
    ),
    (
        'your merciful overlords would like you to talk about mental health. '
        'or anything, really; except the democratic election of a head of '
        'state.',
        'your merciful overlords would like you to talk about mental health or '
        'anything really except the democratic election of a head of state'
    ),
    (
        'This is the best thing i\'ve ever seen https://t.co/vLGv1abHu8',
        'this is the best thing i\'ve ever seen'
    )
])
def test_extract_phrase(input_, output):
    assert extract_phrase(input_) == output
