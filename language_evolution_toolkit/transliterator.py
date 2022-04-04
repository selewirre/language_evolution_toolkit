from transliterate.base import TranslitLanguagePack as TLPack
from typing import Tuple, Dict


class CustomTransliterator(TLPack):
    """
    CustomTransliterator is a class based on the transliterate-package class TranslitLanguagePack.
    It is used to easily replace a list of characters with another list of characters, either it is
    a sound change, an inflexion or abbreviations on phonoogical rules.

    Example
    -------
    >>> data_dict = {'C': '[consonant]', 'N': '[nasal]', 'V': '[vowel]'}
    >>> ct = CustomTransliterator(data_dict)
    >>> ct.translit('CV')
    '[consonant][vowel]'
    >>> ct.translit('[nasal]', reversed=True)
    'N'
    """

    language_name = ''
    language_code = ''

    def __init__(self, data_dictionary: Dict):
        transliterator_data = TransliteratorData(data_dictionary)
        self.mapping = transliterator_data.mapping
        self.pre_processor_mapping = transliterator_data.pre_processor_mapping
        self.reversed_specific_pre_processor_mapping = transliterator_data.reversed_specific_pre_processor_mapping

        super().__init__()


class TransliteratorData:
    def __init__(self, mapping_dictionary: Dict):
        self.mapping_dictionary: Dict = mapping_dictionary
        self.mapping, self.pre_processor_mapping, self.reversed_specific_pre_processor_mapping = \
            get_transliteration_mapping_from_dictionary(self.mapping_dictionary)

    def __repr__(self):
        return repr({'Mapping': self.mapping,
                     'Pre-processor Mapping': self.pre_processor_mapping,
                     'Reversed Pre-processor Mapping': self.reversed_specific_pre_processor_mapping})


def get_transliteration_mapping_from_dictionary(mapping_dictionary: Dict) -> Tuple[Tuple, Dict, Dict]:
    single_char_from = []
    single_char_to = []
    multi_from_dict = {}
    multi_to_dict = {}

    for i in range(len(mapping_dictionary.keys())):
        letter_from = list(mapping_dictionary.keys())[i]
        letter_to = list(mapping_dictionary.values())[i]

        if len(letter_from) == 1 and len(letter_to) == 1:
            single_char_from.append(letter_from)
            single_char_to.append(letter_to)

        if len(letter_from) != 1:
            multi_to_dict[letter_to] = letter_from

        if len(letter_to) != 1:
            multi_from_dict[letter_from] = letter_to

    return (''.join(single_char_from), ''.join(single_char_to)), multi_from_dict, multi_to_dict
