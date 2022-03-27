import warnings
from typing import List, Union, Tuple, Iterator

from ipapy import UNICODE_TO_IPA
from ipapy.ipachar import IPAChar, IPALetter, IPAVowel, IPADiacritic, IPASuprasegmental, IPAConsonant, IPATone
from multipledispatch import dispatch

from language_evolution_toolkit.utils import LinguisticObject, ImmutableProperty, TrackingID


class Phoneme(LinguisticObject):
    """
    Phoneme is a class that holds information about a given phoneme.

    Attributes
    ----------
    unicode_string: str
        The string of the phoneme in unicode (e.g. "pʰ")
    romanization: str
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
        tracking_id: optional, TrackingID
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


class PhonemeCatalog(LinguisticObject):
    """
    PhonemeCatalog is a class that holds information about an assortment of phonemes.

    Attributes
    ----------
    phonemes: List[Phoneme]
        A list of all the phonemes in the catalog.
    unicode_string_list: List[str]
        List of all the unicode_strings in the phonemes.
    romanization_list: List[str]
        List of all the romanizations in the phonemes.
    ipa_chars_list: List[List[Union[IPAChar, IPALetter, IPAConsonant, IPAVowel,
                                    IPADiacritic, IPASuprasegmental, IPATone]]]
        A list of ipa characters of each phoneme.
    descriptors_list: List[Tuple[str]]
        A list of all the descriptors in the phonemes.

    Example
    -------
    >>> a = Phoneme('a')
    >>> p = Phoneme('p')
    >>> e = Phoneme('e')
    >>> pc = PhonemeCatalog([a, p, e])
    >>> print(pc)  # returns the list of all the phonemes
    [Phoneme(unicode_string='a', romanization='a', ipa_chars=[front open unrounded vowel], descriptors=('vowel', 'open', 'front', 'unrounded')), Phoneme(unicode_string='p', romanization='p', ipa_chars=[bilabial consonant plosive voiceless], descriptors=('consonant', 'voiceless', 'bilabial', 'plosive')), Phoneme(unicode_string='e', romanization='e', ipa_chars=[close-mid front unrounded vowel], descriptors=('vowel', 'close-mid', 'front', 'unrounded'))]
    >>> print(pc.with_descriptors('unrounded'))  # returns all phonemes that are unrounded
    [Phoneme(unicode_string='a', romanization='a', ipa_chars=[front open unrounded vowel], descriptors=('vowel', 'open', 'front', 'unrounded')), Phoneme(unicode_string='e', romanization='e', ipa_chars=[close-mid front unrounded vowel], descriptors=('vowel', 'close-mid', 'front', 'unrounded'))]
    """

    phonemes = ImmutableProperty()
    unicode_string_list = ImmutableProperty()
    romanization_list = ImmutableProperty()
    ipa_chars_list = ImmutableProperty()
    descriptors_list = ImmutableProperty()

    def __init__(self, phonemes: List[Phoneme], tracking_id: TrackingID = None):
        """
        Parameters
        ----------
        phonemes: List[Phoneme]
            A list of all the Phonemes that will constitute the PhonemeCatalog.
        tracking_id: optional, TrackingID
            The tracking identification for linguistic evolution.
        """
        self._phonemes = phonemes
        self.__post_init__()
        super().__init__(tracking_id)

    def __post_init__(self):
        self._unicode_string_list: List[str] = [phoneme.unicode_string for phoneme in self.phonemes]
        self._romanization_list: List[str] = [phoneme.romanization for phoneme in self.phonemes]
        self._ipa_chars_list: List[List[Union[
            IPAChar, IPALetter, IPAConsonant, IPAVowel,
            IPADiacritic, IPASuprasegmental, IPATone]]] = [phoneme.ipa_chars for phoneme in self.phonemes]
        self._descriptors_list: List[Tuple[str]] = [phoneme.descriptors for phoneme in self.phonemes]

    def with_descriptors(self, descriptors: Union[str, List[str]], exact_match: bool = True) -> List[Phoneme]:
        """
        Parameter
        ---------
        descriptors: Union[str, List[str]]
            A specific descriptor (e.g. 'vowel', 'bilabial', or 'aspired'), or a list of descriptors
            (e.g. ['bilabial', 'aspired']).
        exact_math: optional, bool
            A variable that determined if all the descriptors must describe the phoneme, or only one is good enough.

        Returns
        -------
        List[Phonemes]
            A list of all the phonemes that have all or any of the descriptors in the given list.
        """
        if isinstance(descriptors, str):
            descriptors = [descriptors]

        if exact_match:
            matching_method = all
        else:
            matching_method = any

        phonemes = []
        for phoneme in self.phonemes:
            add_to_list = matching_method([bool(descriptor in phoneme.descriptors) for descriptor in descriptors])
            if add_to_list:
                phonemes.append(phoneme)

        return phonemes

    @dispatch(int)
    def __getitem__(self, item: int) -> Phoneme:
        """
        Returns
        -------
        Phoneme
            Retrieving item by the phoneme list index number.
        """
        try:
            return self.phonemes[item]
        except IndexError:
            raise IndexError('Phoneme Catalog index is out of range')

    @dispatch(str)
    def __getitem__(self, item: str) -> Phoneme:
        """
        Returns
        -------
        Phoneme
            Retrieving item by the unicode string or romanization of the phoneme list .
        """
        try:
            return self.phonemes[self.unicode_string_list.index(item)]
        except ValueError:
            pass

        try:
            return self.phonemes[self.romanization_list.index(item)]
        except ValueError:
            raise KeyError(f'{item} is neither in unicode_string_list nor'
                           f' in the romanization_list of the phoneme catalog.')

    def __iter__(self) -> Iterator:
        """
        Return
        ------
        Iterator
            Phoneme list.
        """
        return iter(self.phonemes)

    def __hash__(self):
        return hash(self.phonemes)

    def __eq__(self, other: "PhonemeCatalog"):
        """ The PhonemeCatalogs are the same if their phonemes are the same. """
        if not self.__class__.__name__ == other.__class__.__name__:
            return False
        else:
            return self.phonemes == other.phonemes

    def __repr__(self):
        return repr(self.phonemes)

    @classmethod
    def from_lists(cls, unicode_strings: List[str], romanizations: List[str] = None,
                   phoneme_tracking_ids: List[TrackingID] = None,
                   catalog_tracking_id: TrackingID = None) -> "PhonemeCatalog":
        """
        Implementing a PhonemeCatalog from lists of phoneme components instead of a list of phonemes.
        Parameters
        ----------
        unicode_strings: List[str]
            List of unicode strings for each phoneme.
        romanizations: optional, List[str]
            List of romanizations for each phoneme.
        phoneme_tracking_ids: List[TrackingID]
            List of tracking IDs for each phoneme.
        catalog_tracking_id: TrackingID
            Tracking identification for linguistic evolution.

        Return
        ------
        PhonemeCatalog
            PhonemeCatalog object defined by the given lists and tracking ID.
        """
        if not romanizations:
            romanizations = len(unicode_strings)*['']
        if len(unicode_strings) != len(romanizations):
            raise ValueError("The length of 'unicode_strings' and 'romanizations' lists are not the same.")

        if not phoneme_tracking_ids:
            phoneme_tracking_ids = [TrackingID() for _ in unicode_strings]
        if len(unicode_strings) != len(phoneme_tracking_ids):
            raise ValueError("The length of 'unicode_strings' and 'phoneme_tracking_ids' lists are not the same.")

        phonemes = [Phoneme(us, rms, tids) for (us, rms, tids)
                    in zip(unicode_strings, romanizations, phoneme_tracking_ids)]

        return cls(phonemes, catalog_tracking_id)


class UniquePhonemeCatalog(PhonemeCatalog):
    """
    UniquePhonemeCatalog is a class that holds information about an assortment of unique phonemes. If a phoneme in the
    input list is a duplicate, it will be ignored. Only the first occurrence will remain.
    """

    def __post_init__(self):
        self.uniquefy_phonemes()
        super().__post_init__()

    def uniquefy_phonemes(self):
        new_phonemes = []
        for phoneme in self.phonemes:
            if phoneme not in new_phonemes:
                new_phonemes.append(phoneme)
            else:
                warnings.warn(f'{phoneme} has a duplicate in the Phoneme list. It will be ignored.')
        self._phonemes = new_phonemes
