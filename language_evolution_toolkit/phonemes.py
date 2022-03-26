from typing import List, Union, Tuple

from ipapy import UNICODE_TO_IPA
from ipapy.ipachar import IPAChar, IPALetter, IPAVowel, IPADiacritic, IPASuprasegmental, IPAConsonant, IPATone

from language_evolution_toolkit.utils import LinguisticObject, ImmutableProperty, TrackingID


class Phoneme(LinguisticObject):
    """
    Phoneme is a dataclass that holds information about a given phoneme.

    Attributes
    ----------
    unicode_string: str
        The string of the phoneme in unicode (e.g. "pʰ")
    romanization: optional, str
        The romanization of the phoneme. If not give, it defaults to unicode_string.
    ipa_chars: List[Union[IPAChar, IPALetter, IPAConsonant, IPAVowel,
                          IPADiacritic, IPASuprasegmental, IPATone]]
        A list of the ipa characters defined by the given unicode_string.
    descriptors: Tuple[str]
        A list of descriptors (str) that define the phoneme. It is a list of all the descriptors of each character in
         the unicode_string.

    Example
    -------
    >>> example_phoneme = Phoneme("pʰ", "ph")
    >>> print(example_phoneme.descriptors)
    ('consonant', 'voiceless', 'bilabial', 'plosive', 'aspirated')
    >>> print(example_phoneme.__immutables_dict__)
    {'unicode_string': 'pʰ', 'romanization': 'ph', 'ipa_chars': [bilabial consonant plosive voiceless, aspirated diacritic], 'descriptors': ('consonant', 'voiceless', 'bilabial', 'plosive', 'aspirated')}

    """

    unicode_string = ImmutableProperty()
    romanization = ImmutableProperty()
    ipa_chars = ImmutableProperty()
    descriptors = ImmutableProperty()

    def __init__(self, unicode_string: str, romanization: str = '', tracking_id: TrackingID = None):
        """
        Parameters
        ----------
        unicode_string: str
             The string of the phoneme in unicode (e.g. "pʰ").
        romanization: optional, str
            The romanization of the phoneme. If not give, it defaults to unicode_string.
        tracking_id: TrackingID
            The tracking identification for linguistic evolution.
        """
        self._unicode_string: str = unicode_string
        self._romanization: str = romanization

        self._set_ipa_chars()
        self._set_romanization()
        self._set_descriptors()
        super().__init__(tracking_id)

    def _set_ipa_chars(self):
        """ Defines the ipa_chars from the unicode_string. """
        self._ipa_chars: List[Union[IPAChar, IPALetter, IPAConsonant,
                                    IPAVowel, IPADiacritic, IPASuprasegmental, IPATone]] = []
        for unicode_char in self.unicode_string:
            self._ipa_chars.append(UNICODE_TO_IPA[unicode_char])

    def _set_romanization(self):
        """ Defines romanization as unicode_string if the input romanization value is empty. """
        if self._romanization == '':
            self._romanization = self.unicode_string

    def _set_descriptors(self):
        """
        Defines the descriptors (str) as a list of all the descriptors of each character in the unicode_string.
        Ignores the descriptor 'diacritic'.
        """
        descriptors = []
        for i in range(len(self.ipa_chars)):
            descriptors = descriptors + self.ipa_chars[i].descriptors

        while 'diacritic' in descriptors:
            descriptors.remove('diacritic')

        self._descriptors: Tuple[str] = tuple(descriptors)

    def __hash__(self):
        return hash(self.descriptors)

    def __eq__(self, other: "Phoneme"):
        """ The Phonemes are the same if their descriptors are the same. Romanization does not play a part in this. """
        if not self.__class__.__name__ == other.__class__.__name__:
            return False
        else:
            return self.descriptors == other.descriptors
