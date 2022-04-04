import warnings
from typing import List, Union, Tuple, Iterator, Set, Iterable

from ipapy.ipachar import IPAChar, IPALetter, IPAVowel, IPADiacritic, IPASuprasegmental, IPAConsonant, IPATone
from multipledispatch import dispatch

from language_evolution_toolkit.phones import Phone
from language_evolution_toolkit.utils import LinguisticObject, ImmutableProperty, TrackingID, sort_by_element_attribute, check_descriptors


# TODO: Think about using an attribute to define the conditions for which each phone is used in.
#  Maybe put it in the phones? -> No
class Phoneme(LinguisticObject):
    """
    Phoneme is a class that holds information about a given phoneme.

    Attributes
    ----------
    transcription: str
        The string of the phoneme in unicode (e.g. "p" for /p/).
    allophones: Tuple[Phone]
        A list of all the allophones that comprise the phoneme.
    allophone_transcriptions: List[str]
        A list of all the allophone transcriptions.
    allophone_ipa_chars: List[List[Union[IPAChar, IPALetter, IPAConsonant, IPAVowel,
                                         IPADiacritic, IPASuprasegmental, IPATone]]]
        A list of the ipa characters of all allophones.
    allophone_descriptors: List[Tuple[str]]
        A list of all tuples of allophone descriptors.
    common_descriptors: Tuple[str]
        A tuple of common descriptors (str) that define the phoneme. It is a list of all the common descriptors  between
        the phones.
    all_descriptors: Tuple[str]
        A tuple of all descriptors (str) that define the phoneme. It is a list of any descriptors that appear in any of
        the allophones.

    Example
    -------
    >>> phone_p1 = Phone('p')
    >>> phone_p2 = Phone('pʰ')
    >>> phone_p3 = Phone('p̚')
    >>> phoneme_p = Phoneme('p', [phone_p1, phone_p2, phone_p3])
    >>> print(phoneme_p.all_descriptors)
    ('aspirated', 'bilabial', 'consonant', 'no-audible-release', 'plosive', 'voiceless')
    >>> print(phoneme_p.common_descriptors)
    ('bilabial', 'consonant', 'plosive', 'voiceless')
    """

    transcription: str = ImmutableProperty()
    allophones: Tuple[Phone] = ImmutableProperty()
    common_descriptors: Tuple[str] = ImmutableProperty()
    all_descriptors: Tuple[str] = ImmutableProperty()

    def __init__(self, transcription: str, allophones: Iterable[Union[Phone, str]] = None,
                 tracking_id: TrackingID = None, assure_uniqueness: bool = True):
        """
        Parameters
        ----------
        transcription: str
             The string of the phoneme in unicode (e.g. "p" for /p/).
        allophones: optional, Iterable[Union[Phone, str]]
            A list of all the allophones (as Phone or str) that comprise the phoneme. Defaults to a single phone same as
            the phoneme transcription.
        tracking_id: optional, TrackingID
            The tracking identification for linguistic evolution.
        """
        self._transcription: str = transcription

        if not allophones:
            allophones = [Phone(self.transcription)]
        else:
            allophones: List[Phone] = [allophone if isinstance(allophone, Phone) else Phone(allophone)
                                       for allophone in allophones]

        self._allophones: Tuple[Phone] = tuple(sort_by_element_attribute(allophones, 'transcription'))

        if assure_uniqueness:
            self._assure_allophone_uniqueness()

        self.__post_init__()

        super().__init__(tracking_id)

    def __post_init__(self):
        self._set_common_descriptors()
        self._set_all_descriptors()

    def _assure_allophone_uniqueness(self):
        new_allophones: List[Phone] = []
        for allophone in self.allophones:
            if allophone not in new_allophones:
                new_allophones.append(allophone)
            else:
                warnings.warn(f'{allophone} is a duplicate in the allophone list. It will be ignored.')
        self._allophones: Tuple[Phone] = tuple(new_allophones)

    @property
    def allophone_transcriptions(self) -> List[str]:
        """ A list of transcriptions of each allophone. """
        return [allophone.transcription for allophone in self.allophones]

    @property
    def allophone_ipa_chars(self) -> List[List[Union[
            IPAChar, IPALetter, IPAConsonant, IPAVowel, IPADiacritic, IPASuprasegmental, IPATone]]]:
        """ A list of ipa_chars of each allophone. """
        return [allophone.ipa_chars for allophone in self.allophones]

    @property
    def allophone_descriptors(self) -> List[Tuple[str]]:
        """ A list of descriptors of each allophone. """
        return [allophone.descriptors for allophone in self.allophones]

    def _set_all_descriptors(self):
        """ Setting the all_descriptors as a tuple of all descriptors appearing in allophones. """
        all_descriptors: Set[str] = set.union(*[set(ad) for ad in self.allophone_descriptors])
        self._all_descriptors: Tuple[str] = tuple(sorted(all_descriptors))

    def _set_common_descriptors(self):
        """ Setting the common_descriptors as a tuple of common descriptors between allophones. """
        common_descriptors: Set[str] = set.intersection(*[set(ad) for ad in self.allophone_descriptors])
        self._common_descriptors: Tuple[str] = tuple(sorted(common_descriptors))

    def has_common_descriptors(self, descriptors: Union[str, List[str]], exact_match: bool = True) -> bool:
        """
        Parameter
        ---------
        descriptors: Union[str, List[str]]
            A specific descriptor (e.g. 'vowel', 'bilabial', or 'aspired'), or a list of descriptors
            (e.g. ['bilabial', 'aspired']). If a descriptor starts with "!", it means that the descriptor is NOT wanted.
        exact_math: optional, bool
            A variable that determined if all the descriptors must describe the phoneme, or if only one is good enough.

        Returns
        -------
        bool
            A value True or False if all or any of the given descriptors describe the phone.
        """
        if isinstance(descriptors, str):  # to work with a list of strings either way
            descriptors = [descriptors]

        if exact_match:
            matching_method = all
        else:
            matching_method = any

        return matching_method(check_descriptors(descriptors, self.common_descriptors))

    def find_allophones_with_descriptors(self, descriptors: Union[str, List[str]],
                                         exact_match: bool = True) -> List[Phone]:
        """
        Parameter
        ---------
        descriptors: Union[str, List[str]]
            A specific descriptor (e.g. 'vowel', 'bilabial', or 'aspired'), or a list of descriptors
            (e.g. ['bilabial', 'aspired']). If a descriptor starts with "!", it means that the descriptor is NOT wanted.
        exact_math: optional, bool
            A variable that determined if all the descriptors must describe the phoneme, or if only one is good enough.

        Returns
        -------
        List[Phonemes]
            A list of all the allophones that have all or any of the descriptors in the given list.
        """
        if isinstance(descriptors, str):  # to work with a list of strings either way
            descriptors = [descriptors]

        phones = [phone for phone in self.allophones if phone.has_descriptors(descriptors, exact_match)]
        return phones

    @dispatch(int)
    def __getitem__(self, item: int) -> Phone:
        """
        Returns
        -------
        Phoneme
            Retrieving allophone by the allophone list index number.
        """
        try:
            return self.allophones[item]
        except IndexError:
            raise IndexError('Allophone list index is out of range')

    @dispatch(str)
    def __getitem__(self, item: str) -> Phone:
        """
        Returns
        -------
        Phoneme
            Retrieving allophone by the transcription.
        """
        try:
            return self.allophones[self.allophone_transcriptions.index(item)]
        except ValueError:
            raise KeyError(f'{item} is not a phone transcription in the allophone list.')

    def __iter__(self) -> Iterator:
        """
        Return
        ------
        Iterator
            Allophone list.
        """
        return iter(self.allophones)

    def __hash__(self):
        return hash(self.allophones)

    def __eq__(self, other: "Phoneme"):
        """ The Phonemes are the same if their allophones are the same. Transcription does not play a part in this. """
        if not self.__class__.__name__ == other.__class__.__name__:
            return False
        else:
            return self.allophones == other.allophones

    def __repr__(self):
        return f"/{self.transcription}/: {self.allophones}"


class PhonemeCatalog(LinguisticObject):
    """
    PhonemeCatalog is a class that holds information about an assortment of phonemes.

    Attributes
    ----------
    phonemes: List[Phoneme]
        A list of all the phonemes in the catalog.
    phoneme_transcriptions: List[str]
        A list of all the transcriptions of the given phonemes.
    all_descriptors: Tuple[str]
        A list of all the descriptors of the given phonemes.

    Example
    -------
    >>> phoneme_p = Phoneme('p', ['p', 'pʰ', 'p̚'])
    >>> phoneme_t = Phoneme('t', ['t', 'tʰ', 't̚'])
    >>> pc = PhonemeCatalog([phoneme_p, phoneme_t])
    >>> print(pc.find_phonemes_with_descriptors('bilabial'))
    [/p/: ([p], [pʰ], [p̚])]
    >>> print(pc.find_phones_with_descriptors('aspirated'))
    [[pʰ], [tʰ]]
    >>> print(pc.all_descriptors)
    ('alveolar', 'aspirated', 'bilabial', 'consonant', 'no-audible-release', 'plosive', 'voiceless')
    """

    phonemes: Tuple[Phoneme] = ImmutableProperty()
    phones: List[Phone] = ImmutableProperty()
    all_descriptors: Tuple[str] = ImmutableProperty()

    def __init__(self, phonemes: Iterable[Union[Phoneme, Phone, str]], tracking_id: TrackingID = None, assure_uniqueness: bool = True):
        """
        Parameters
        ----------
        phonemes: Iterable[Union[Phoneme, Phone, str]]
            A list of all the Phonemes that will constitute the PhonemeCatalog.
        tracking_id: optional, TrackingID
            The tracking identification for linguistic evolution.
        """
        phonemes = [val if isinstance(val, Phoneme) else Phoneme(val.transcription if isinstance(val, Phone) else val)
                    for val in phonemes]

        if not len(phonemes):
            raise ValueError(f'Phoneme list can not be empty.')

        self._phonemes: Tuple[Phoneme] = tuple(sort_by_element_attribute(phonemes, 'transcription'))

        if assure_uniqueness:
            self._assure_allophone_uniqueness()

        self.__post_init__()
        super().__init__(tracking_id)

    def __post_init__(self):
        self._set_phones()
        self._set_all_descriptors()

    def _assure_allophone_uniqueness(self):
        new_phonemes = []
        for phoneme in self.phonemes:
            if phoneme not in new_phonemes:
                new_phonemes.append(phoneme)
            else:
                warnings.warn(f'{phoneme} is a duplicate in the Phoneme list. It will be ignored.')
        self._phonemes = new_phonemes

    def _set_phones(self):
        phones: List[Phone] = []
        for phoneme in self.phonemes:
            for phone in phoneme.allophones:
                if phone not in phones:
                    phones.append(phone)
        self._phones: List[Phone] = phones

    def _set_all_descriptors(self):
        """ Setting the all_descriptors as a tuple of all descriptors appearing in all phonemes. """
        all_descriptors: Set[str] = set.union(*[set(phoneme.all_descriptors) for phoneme in self.phonemes])
        self._all_descriptors: Tuple[str] = tuple(sorted(all_descriptors))

    @property
    def phoneme_transcriptions(self) -> List[str]:
        return [phoneme.transcription for phoneme in self.phonemes]

    @property
    def phone_transcriptions(self) -> List[str]:
        return [phone.transcription for phone in self.phones]

    def find_phones_with_descriptors(self, descriptors: Union[str, List[str]], exact_match: bool = True) -> List[Phone]:
        """
        Parameter
        ---------
        descriptors: Union[str, List[str]]
            A specific descriptor (e.g. 'vowel', 'bilabial', or 'aspired'), or a list of descriptors
            (e.g. ['bilabial', 'aspired']). If a descriptor starts with "!", it means that the descriptor is NOT wanted.
        exact_math: optional, bool
            A variable that determined if all the descriptors must describe the phoneme, or only one is good enough.

        Returns
        -------
        List[Phone]
            A list of all the phones that have all or any of the descriptors in the given list.
        """
        if isinstance(descriptors, str):
            descriptors = [descriptors]

        phones = [phone for phone in self.phones if phone.has_descriptors(descriptors, exact_match)]
        return phones

    def find_phonemes_with_descriptors(self, descriptors: Union[str, List[str]],
                                       exact_match: bool = True) -> List[Phoneme]:
        """
        Parameter
        ---------
        descriptors: Union[str, List[str]]
            A specific descriptor (e.g. 'vowel', 'bilabial', or 'aspired'), or a list of descriptors
            (e.g. ['bilabial', 'aspired']). If a descriptor starts with "!", it means that the descriptor is NOT wanted.
        exact_math: optional, bool
            A variable that determined if all the descriptors must describe the phoneme, or only one is good enough.

        Returns
        -------
        List[Phoneme]
            A list of all the phones that have all or any of the descriptors in the given list.
        """
        if isinstance(descriptors, str):
            descriptors = [descriptors]

        phonemes = [phoneme for phoneme in self.phonemes if phoneme.has_common_descriptors(descriptors, exact_match)]
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
            return self.phonemes[self.phoneme_transcriptions.index(item)]
        except ValueError:
            raise KeyError(f'{item} is not a phoneme transcription in the phoneme catalog.')

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
