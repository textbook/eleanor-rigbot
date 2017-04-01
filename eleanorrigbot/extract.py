"""Functionality to clean tweet content for processing."""
import re

VALID_PUNCTUATION = r'.,;:?!\''

CLEAN_TEXT = re.compile(r'(?:^|\s)[a-z{}\s]+(?:$|\s)'.format(VALID_PUNCTUATION))


def extract_phrase(text):
    """Extract the text of the tweet for phrase testing.

    Here the phrase to test is defined as the longest substring of
    clean text, with any punctuation between the words removed.

    """
    return _rejoin(_clean_text(text.lower()))


def _clean_text(text):
    """Find the longest substring of 'clean' characters in the text."""
    clean_strings = CLEAN_TEXT.findall(text)
    if clean_strings:
        return max(clean_strings, key=len)
    return ''


def _rejoin(phrase):
    """Rejoin phrase with any punctuation stripped."""
    return ' '.join([word.strip(VALID_PUNCTUATION) for word in phrase.split()])
