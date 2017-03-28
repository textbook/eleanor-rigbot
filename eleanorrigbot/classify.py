"""Functionality for classifying phrases extracted from tweets."""

from nltk.corpus import cmudict

_PRONUNCIATIONS = cmudict.dict()


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
    if _calculate_total_syllables(words_and_syllables) != 22:
        return False
    sub_phrases = _greedy_match_syllable_pattern(words_and_syllables)
    if sub_phrases is None:
        return False
    return _lines_rhyme(*sub_phrases[-2:])


def _lines_rhyme(first, second):
    """Whether the two supplied lines rhyme.

    Rhyming is defined here as the last word of each line containing
    the same final syllable.

    Arguments:
      first (:py:class:`list`): The first line as a list of words.
      second (:py:class:`list`): The second line as a list of words.

    Returns:
      :py:class:`bool`: Whether the lines rhyme.

    """
    first_phonemes = _phonemes_in_word(first[-1])
    second_phonemes = _phonemes_in_word(second[-1])
    first_syllable = _syllables(first_phonemes)[-1]
    second_syllable = _syllables(second_phonemes)[-1]
    return first_syllable[:-1] == second_syllable[:-1]


def _calculate_total_syllables(words_and_syllables):
    """Calculate the total syllable count.

    Arguments:
      words_and_syllables (:py:class:`list`): The words in the phrase
        and their syllable counts.

    Returns:
      :py:class:`int`: The total syllable count, or ``0`` if any words
        had no syllable count.

    """
    try:
        return sum(syllables for _, syllables in words_and_syllables)
    except TypeError:
        return 0


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
    try:
        phonemes = _phonemes_in_word(word)
    except KeyError:
        return
    return len(_syllables(phonemes))


def _phonemes_in_word(word):
    """Returns the phonemes in the word from the first pronunciation.

    Arguments:
      word (:py:class:`str`): The word to calculate the syllable count
        for.

    Returns:
      :py:class:`list`: The phonemes in the word.

    Raises:
      :py:class:`KeyError`: If the word has no pronunciations in the
        corpus.

    """
    return _PRONUNCIATIONS[word][0]


def _syllables(phonemes):
    """Extract the syllables from the phonemes.

    See http://stackoverflow.com/a/4103234/3001761

    Arguments:
      phonemes (:py:class:`list`): The phonemes in the word.

    Returns:
      :py:class:`list`: The syllables in those phonemes.

    """
    return [phoneme for phoneme in phonemes if phoneme[-1].isdigit()]
