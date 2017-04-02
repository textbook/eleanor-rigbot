"""Functionality for classifying phrases extracted from tweets."""
import logging

from collections import defaultdict
from itertools import combinations

from pronouncing import phones_for_word, rhymes, syllable_count

logger = logging.getLogger(__name__)


class PhraseMatcher(object):  # pylint: disable=too-few-public-methods
    """Class to match phrases found in tweets.

    Arguments:
      syllable_pattern (:py:class:`tuple`): The syllable pattern, as a
        sequence of the syllables in each line.
      rhyming_scheme (:py:class:`tuple`, optional): The rhyming scheme,
        as a sequence of rhyming groups (or ``None`` for lines not in a
        rhyming group). The groups are used as dictionary keys, so must
        be hashable (e.g. :py:class:`int` or :py:class:`str`). Note
        that the length of the ``rhyming_scheme`` must be the same as
        the ``syllable_pattern``.

    Attributes:
      total_syllables (:py:class:`int`): The total number of syllables
        in the phrase.
      rhyming_lines (:py:class:`dict`): The map of rhyming groups to
        line numbers.

    """

    def __init__(self, syllable_pattern, rhyming_scheme=None):
        if (rhyming_scheme is not None
                and len(syllable_pattern) != len(rhyming_scheme)):
            error = 'syllable pattern and rhyming scheme must have same length'
            raise ValueError(error)
        self.syllable_pattern = syllable_pattern
        self.total_syllables = sum(syllable_pattern)
        self.rhyming_lines = self._create_rhyming_lines(rhyming_scheme)

    def __call__(self, phrase):
        """Whether a phrase matches the scheme.

        Arguments:
          phrase (:py:class:`str`): The phrase to test.

        Returns:
          :py:class:`bool`: Whether it matches the scheme.

        """
        words_and_syllables = [(word, self._syllables_in_word(word))
                               for word in phrase.split()]
        total_syllables = self._calculate_total_syllables(words_and_syllables)
        if total_syllables is None:
            return False
        logger.debug(
            'processing %s-syllable tweet: %r',
            total_syllables,
            words_and_syllables
        )
        if total_syllables != self.total_syllables:
            return False
        lines = self._greedy_match_syllable_pattern(words_and_syllables)
        if lines is None:
            return False
        logger.info('tweet matches syllable pattern: %r', lines)
        return self._match_rhyming_scheme(lines)

    def _match_rhyming_scheme(self, lines):
        """Whether the lines fit the rhyming scheme.

        Arguments:
          lines (:py:class:`list`): The lines, as a list of lists of
            strings.

        Returns:
          :py:class:`bool`: Whether the lines match the rhyming scheme.

        """
        if self.rhyming_lines is not None:
            for indices in self.rhyming_lines.values():
                if not self._lines_rhyme(*[lines[index] for index in indices]):
                    return False
        return True

    def _greedy_match_syllable_pattern(self, words_and_syllables):
        """Whether the words_and_syllables fit into the pattern.

        Arguments:
          words_and_syllables (:py:class:`list`): The words in the
            phrase and their syllable counts.

        Returns:
          :py:class:`list`: The words in the phrase split into the
            pattern or ``None`` if the phrase didn't fit the pattern.

        """
        words_and_syllables = words_and_syllables[:]
        phrase = [[]]
        for count in self.syllable_pattern:
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

    @staticmethod
    def _calculate_total_syllables(words_and_syllables):
        """Calculate the total syllable count.

        Arguments:
          words_and_syllables (:py:class:`list`): The words in the
            phrase and their syllable counts.

        Returns:
          :py:class:`int`: The total syllable count, or ``None`` if
            any words had no syllable count.

        """
        try:
            return sum(syllables for _, syllables in words_and_syllables)
        except TypeError:
            pass

    @staticmethod
    def _create_rhyming_lines(rhyming_scheme):
        """Create the map of line numbers to rhyme groups."""
        if rhyming_scheme is None:
            return None
        rhyming_lines = defaultdict(list)
        for index, group in enumerate(rhyming_scheme):
            if group is not None:
                rhyming_lines[group].append(index)
        return rhyming_lines

    @staticmethod
    def _lines_rhyme(*lines):
        """Whether the supplied lines rhyme.

        Arguments:
          *lines (:py:class:`tuple`): The lines to check as lists of
            lists of words.

        Returns:
          :py:class:`bool`: Whether all of the lines rhyme.

        """
        words = [line[-1] for line in lines]
        for first_word, second_word in combinations(words, 2):
            if (first_word not in rhymes(second_word)
                    and second_word not in rhymes(first_word)):
                return False
        return True

    @staticmethod
    def _syllables_in_word(word):
        """Returns the number of syllables in the word.

        Arguments:
          word (:py:class:`str`): The word to calculate the syllable
            count for.

        Returns:
          :py:class:`int`: The number of syllables in the word (or
            ``None`` if the count could not be calculated).

        """
        phones = phones_for_word(word)
        if phones:
            return syllable_count(phones[0])
