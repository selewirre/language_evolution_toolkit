from typing import Dict


class Transliterator:
    """
    This is a simple bidirectional transliterator inspired by the "transliterate" package written by barseghyanartur.
    Check out their [github page](https://github.com/barseghyanartur/transliterate) for more information.
    Here, we use a simple one-to-one mapping dictionary as input, where each key is the source and each value is the
    target of the transliteration process.

    Attributes
    ----------
    mapping_dictionary: Dict[str, str]
        A simple one-to-one mapping dictionary. Each key is the source string and each value is the target string.
    _single_source_to_target_mapping: Dict[int, str]
        The processed mapping that originates from single-character sources. Keys are single character sources
        (represented as unicode integers), and values are single or multi-character targets.
    _single_target_to_source_mapping: Dict[int, str]
        The processed mapping that originates from single-character targets. Keys are single character targets
        (represented as unicode integers), and values are single or multi-character sources.
    _multi_source_to_target_mapping: Dict[str, str]
        The processed mapping that originates from multi-character sources. Keys are single character sources, and
        values are single or multi-character targets.
    _multi_target_to_source_mapping: Dict[str, str]
        The processed mapping that originates from multi-character targets. Keys are single character targets, and
        values are single or multi-character sources.

    Examples
    --------
    >>> map_dict2 = {'a': 'e', 'b': 'mp', 'gh': 'c', 'rh': 'qv'}
    >>> trans = Transliterator(map_dict2)
    >>> a = trans.transliterate('parbghonirh')
    >>> print(a)
    permpconiqv
    >>> b = trans.transliterate(a, True)
    >>> print(b)
    parbghonirh


    """

    def __init__(self, mapping_dictionary: Dict[str, str]):
        """
        Parameters
        ----------
        mapping_dictionary: Dict[str, str]
             A simple one-to-one mapping dictionary. Each key is the source string and each value is the target string.
        """
        self.mapping_dictionary: Dict = mapping_dictionary
        self._single_source_to_target_mapping: Dict[int, str] = {}
        self._single_target_to_source_mapping: Dict[int, str] = {}
        self._multi_source_to_target_mapping: Dict[str, str] = {}
        self._multi_target_to_source_mapping: Dict[str, str] = {}
        self._set_transliteration_mapping_from_dictionary()

    def transliterate(self, string: str, reverse: bool = False) -> str:
        """
        This function replaces all the characters in the "string" that are equal to a key in a map with the
        corresponding values of the map.

        Parameters
        ----------
        string: str
            The value that will be transliterated.
        reverse: bool
            If False, the transliteration will use the mapping from source to target. If True, it will use the reverse
            mapping.

        Returns
        -------
        str
            The processed, transliterated string.
        """
        if not reverse:
            string = self._transliterate_source_to_target(string)
        else:
            string = self._transliterate_target_to_source(string)

        return string

    def _transliterate_source_to_target(self, string: str) -> str:
        """
        This function performs transliteration using the source-to-target map.

        Parameters
        ----------
        string: str
            The value that will be transliterated.

        Returns
        -------
        str
            The processed, transliterated string.
        """
        for key, value in self._multi_source_to_target_mapping.items():
            string = string.replace(key, value)
        string = string.translate(self._single_source_to_target_mapping)

        return string

    def _transliterate_target_to_source(self, string: str) -> str:
        """
        This function performs transliteration using the target-to-source map.

        Parameters
        ----------
        string: str
            The value that will be transliterated.

        Returns
        -------
        str
            The processed, transliterated string.
        """
        for key, value in self._multi_target_to_source_mapping.items():
            string = string.replace(key, value)
        string = string.translate(self._single_target_to_source_mapping)

        return string

    def _set_transliteration_mapping_from_dictionary(self):
        """
        This function processes the initializing mapping dictionary. It finds and separated the mapping in four
        categories: two distinctions occur between single-characters and multiple characters, two more distinctions
        occur between source-to-target and target-to-source mappings.

        The single characters can be readily replaced with  the native "str.translate" function, all at once. We use the
        "str.maketrans" function that produces a unicode key - any value mapping dictionary.

        The multiple characters can be replaced by iterating through the dictionary strings and using the function
        "str.replace".
        """
        for i in range(len(self.mapping_dictionary.keys())):
            source_chars = list(self.mapping_dictionary.keys())[i]
            target_chars = list(self.mapping_dictionary.values())[i]

            # TODO: May be nice to add None case to delete items (exploiting the translate mapping option).
            if len(source_chars) == 1:
                self._single_source_to_target_mapping[source_chars] = target_chars
            else:
                self._multi_source_to_target_mapping[source_chars] = target_chars

            if len(target_chars) == 1:
                self._single_target_to_source_mapping[target_chars] = source_chars
            else:
                self._multi_target_to_source_mapping[target_chars] = source_chars

        self._single_source_to_target_mapping = str.maketrans(self._single_source_to_target_mapping)
        self._single_target_to_source_mapping = str.maketrans(self._single_target_to_source_mapping)