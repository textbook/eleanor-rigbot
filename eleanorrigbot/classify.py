"""Functionality for classifying phrases extracted from tweets."""
import logging

from pronouncing import phones_for_word, rhymes, syllable_count

logger = logging.getLogger(__name__)


def phrase_matches(phrase):
    """Whether the phrase matches the scheme.

    The rules for the scheme are as follows:

     1. Must contain exactly 22 syllables

     2. Must divide into 5, 4, 9 and 4 syllables on word breaks

     3. Last two lines (9 syllables and 4 syllables) must rhyme

    Arguments:
      phrase (:py:class:`str`): The phrase to test.

    Returns:
      :py:class:`bool`: Whether it matches the scheme.

    """
    words = phrase.split()
    words_and_syllables = [(word, _syllables_in_word(word)) for word in words]
    total_syllables = _calculate_total_syllables(words_and_syllables)
    if total_syllables is None:
        return False
    logger.debug(
        'processing %s-syllable tweet: %r',
        total_syllables,
        words_and_syllables
    )
    if total_syllables != 22:
        return False
    sub_phrases = _greedy_match_syllable_pattern(words_and_syllables)
    if sub_phrases is None:
        return False
    logger.info('tweet matches syllable pattern: %r', sub_phrases)
    return _lines_rhyme(*sub_phrases[-2:])


def _lines_rhyme(first, second):
    """Whether the two supplied lines rhyme.

    Arguments:
      first (:py:class:`list`): The first line as a list of words.
      second (:py:class:`list`): The second line as a list of words.

    Returns:
      :py:class:`bool`: Whether the lines rhyme.

    """
    first_line_last_word = first[-1]
    second_line_last_word = second[-1]
    return (first_line_last_word in rhymes(second_line_last_word)
            or second_line_last_word in rhymes(first_line_last_word))


def _calculate_total_syllables(words_and_syllables):
    """Calculate the total syllable count.

    Arguments:
      words_and_syllables (:py:class:`list`): The words in the phrase
        and their syllable counts.

    Returns:
      :py:class:`int`: The total syllable count, or ``None`` if any
        words had no syllable count.

    """
    try:
        return sum(syllables for _, syllables in words_and_syllables)
    except TypeError:
        pass


def _greedy_match_syllable_pattern(words_and_syllables, pattern=(5, 4, 9, 4)):
    """Whether the words_and_syllables fit into the appropriate pattern.

    Arguments:
      words_and_syllables (:py:class:`list`): The words in the phrase
        and their syllable counts.

    Returns:
      :py:class:`list`: The words in the phrase split into the pattern
        or ``None`` if the phrase didn't fit the pattern.

    """
    words_and_syllables = words_and_syllables[:]
    phrase = [[]]
    for count in pattern:
        while True:
            word, syllables = words_and_syllables.pop(0)
            count -= syllables
            if count < 0:
                return
            phrase[-1].append(word)
            if count == 0:
                phrase.append([])
                break
    return phrase[:-1] if len(words_and_syllables) == 0 else None


def _syllables_in_word(word):
    """Returns the number of syllables in the word.

    Arguments:
      word (:py:class:`str`): The word to calculate the syllable count
        for.

    Returns:
      :py:class:`int`: The number of syllables in the word (or ``None``
        if the count could not be calculated).

    """
    phones = phones_for_word(word)
    if phones:
        return syllable_count(phones[0])
