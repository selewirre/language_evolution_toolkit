from typing import List, Union, Tuple

from ipapy import UNICODE_TO_IPA
from ipapy.ipachar import IPAChar, IPALetter, IPAVowel, IPADiacritic, IPASuprasegmental, IPAConsonant, IPATone

from language_evolution_toolkit.utils import LinguisticObject, ImmutableProperty, TrackingID


class Phone(LinguisticObject):
    """
    Phone is a class that holds information about a single speech sound or gesture (phone).

    Attributes
    ----------
    transcription: str
        The string of the phone in unicode (e.g. "pʰ" for [pʰ])
    ipa_chars: List[Union[IPAChar, IPALetter, IPAConsonant, IPAVowel,
                          IPADiacritic, IPASuprasegmental, IPATone]]
        A list of the ipa characters defined by the given phone transcription.
    descriptors: Tuple[str]
        A list of descriptors (str) that define the phone. It is a list of all the descriptors of each character in
         the transcription.

    Example
    -------
    >>> example_phone = Phone("pʰ")
    >>> print(example_phone.descriptors)
    ('aspirated', 'bilabial', 'consonant', 'plosive', 'voiceless')
    >>> print(example_phone.__immutables_dict__)
    {'transcription': 'pʰ', 'ipa_chars': [bilabial consonant plosive voiceless, aspirated diacritic], 'descriptors': ('aspirated', 'bilabial', 'consonant', 'plosive', 'voiceless')}
    """

    transcription = ImmutableProperty()
    ipa_chars = ImmutableProperty()
    descriptors = ImmutableProperty()

    def __init__(self, transcription: str, tracking_id: TrackingID = None):
        """
        Parameters
        ----------
        transcription: str
             The string of the phone in unicode (e.g. "pʰ" for [pʰ])
        tracking_id: optional, TrackingID
            The tracking identification for linguistic evolution.
        """
        self._transcription: str = transcription

        self._set_ipa_chars()
        self._set_descriptors()
        super().__init__(tracking_id)

    def _set_ipa_chars(self):
        """ Defines the ipa_chars from the transcription. """
        self._ipa_chars: List[Union[IPAChar, IPALetter, IPAConsonant,
                                    IPAVowel, IPADiacritic, IPASuprasegmental, IPATone]] = []
        for unicode_char in self.transcription:
            self._ipa_chars.append(UNICODE_TO_IPA[unicode_char])

    def _set_descriptors(self):
        """
        Defines the descriptors (str) as a list of all the descriptors of each character in the transcription.
        Ignores the descriptor 'diacritic'.
        """
        descriptors: List[str] = []
        for i in range(len(self.ipa_chars)):
            descriptors = descriptors + self.ipa_chars[i].descriptors

        while 'diacritic' in descriptors:
            descriptors.remove('diacritic')

        self._descriptors: Tuple[str] = tuple(sorted(descriptors))

    def __hash__(self):
        return hash(self.descriptors)

    def __eq__(self, other: "Phone"):
        """ The Sounds are the same if their descriptors are the same. Transcription does not play a part in this. """
        if not self.__class__.__name__ == other.__class__.__name__:
            return False
        else:
            return self.descriptors == other.descriptors

    def __repr__(self):
        return f"[{self.transcription}]"
