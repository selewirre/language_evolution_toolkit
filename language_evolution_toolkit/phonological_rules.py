
import itertools
import re
from typing import List, Union, Tuple, Dict

import numpy as np

from language_evolution_toolkit.phonemes import PhonemeCatalog
from language_evolution_toolkit.transliterator import CustomTransliterator
from language_evolution_toolkit.utils import ImmutableProperty

# A dictionary of abbreviations of descriptor lists (e.g. C for [consonant] and V for [vowel].)
descriptor_abbreviations = {
    # 'A': '{[non-sibilant-affricate],[sibilant-affricate],[lateral-affricate],'
    #      '[ejective-affricate],[lateral-ejective-affricate]}',
    # 'B': '[vowel,back]',
    'C': '[consonant]',
    # 'D': '[voiced,plosive]',
    # 'E': '[vowel,front]',
    # 'F': '{[non-sibilant-fricative],[sibilant-fricative],[lateral-fricative],'
    #      '[ejective-fricative],[lateral-ejective-fricative]}',
    # 'H': Laryngeal,
    # 'J': '[approximant]',
    # 'K': '[velar]',
    # 'Ḱ': Palatovelar,
    # 'L': Liquid,
    # 'M': Diphthong,
    'N': '[nasal]',
    # 'O': Obstruent,
    # 'P': '{[linguolabial],[bilabial]}',
    # 'Q': Uvular consonant click consonant (Khoisan),
    # 'R': Resonant/Sonorant,
    # 'S': Plosive,
    # 'T': Voiceless plosive,
    # 'U': Syllable,
    'V': '[vowel]',
    # 'W': '{[approximant],[lateral-approximant]}',
    # 'Z': Continuant,
}

descriptor_abbreviation_transliterator = CustomTransliterator(descriptor_abbreviations)


class PhonologicalRule:
    """
    PhonologicalRule is a class that processes and holds information about a single phonological rule/sound change.
    It only requires a rule string and a phoneme catalog to find out what sound combinations will be involved in the
    given rule.

    Attributes
    ----------
    rule: str
        The main string of a rule, given in the format "Target -> Replacement / Environment".
        The special characters are:

        - Square brackets "[]": in which you can put the phone descriptors (e.g. [alveolar, voiceless, plosive] for t).
        - Curly brackets "{}": in which you can put a list of individual phones (e.g. {p,t,k})
        - Parentheses "()": in which you can put optional phones or lists of phones. (e.g. ([consonant])). No parenthesis inside [] is allowed for now!
        - Underscore "_": represents the place were the target resides in the environment.
        - Hashtag "#": word boundary.
        - exclamation mark "!": declares exception (e.g. !N meaning for non-nasals)
        - The number zero "0": declares "nothing" (e.g. h -> 0 / #_ as in h disappears if word initial)

        Special characters to be implemented:

        - Dollar sign "$": for stem boundaries
        - A way to use . as syllable boundary (probably simple)
        - Triple dot "...": A wildcard, meaning anywhere before or anywhere after (e.g. _...V)
        - Numerals to indicate something I do not yet understand.

    phoneme_catalog: Union[PhonemeCatalog, None]
        The PhonemeCatalog the phonological rule will be applied to.
    target: str
        The "Target" part of the rule.
    replacement: str
        The "Replacement" part of the rule.
    environment: str
        The "Environment" part of the rule.
    change_dict: Dict[str, str]
        A dict where the keys are all the sound strings that could potentially be changed
        (e.g. h -> 0 / #_ would a single key '#h'.) and the corresponding values are the strings the keys will turn to
        (e.g. h -> 0 / #_ would give 'h'.)
    change_transliterator: CustomTransliterator
        Defined by the change_dict, it is a transliterator that can be used to apply all the potential sound changes.
    """
    rule: str = ImmutableProperty()
    phoneme_catalog: Union[PhonemeCatalog, None] = ImmutableProperty()

    target: str = ImmutableProperty()
    replacement: str = ImmutableProperty()
    environment: str = ImmutableProperty()

    change_dict: Dict[str, str] = ImmutableProperty()
    change_transliterator: CustomTransliterator = ImmutableProperty()

    def __init__(self, rule: str, phoneme_catalog: Union[PhonemeCatalog, None] = None):
        """
        Parameters
        ----------
        rule: str
            The main string of a rule, given in the format "Target -> Replacement / Environment".
            The special characters are:

            - Square brackets "[]": in which you can put the phone descriptors (e.g. [alveolar, voiceless, plosive] for t).
            - Curly brackets "{}": in which you can put a list of individual phones (e.g. {p,t,k})
            - Parentheses "()": in which you can put optional phones or lists of phones. (e.g. ([consonant])). No parenthesis inside [] is allowed for now!
            - Underscore "_": represents the place were the target resides in the environment.
            - Hashtag "#": word boundary.
            - exclamation mark "!": declares exception (e.g. !N meaning for non-nasals)
            - The number zero "0": declares "nothing" (e.g. h -> 0 / #_ as in h disappears if word initial)

            Special characters to be implemented:

            - Dollar sign "$": for stem boundaries
            - A way to use . as syllable boundary (probably simple)
            - Triple dot "...": A wildcard, meaning anywhere before or anywhere after (e.g. _...V)
            - Numerals to indicate something I do not yet understand.

        phoneme_catalog: Union[PhonemeCatalog, None]
            The PhonemeCatalog the phonological rule will be applied to.
        """
        self._rule: str = rule

        self._set_target_str()
        self._set_replacement_str()
        self._set_environment_str()

        self._phoneme_catalog: Union[PhonemeCatalog, None] = phoneme_catalog
        self._set_change_dict()

        # if not self.is_valid():
        #     warnings.warn(f'{self.rule} is not valid.')

    def _set_target_str(self):
        """ Setting the target of given the rule. """
        self._target = extract_rule_target_string(self.rule)

    def _set_replacement_str(self):
        """ Setting the replacement of given the rule. """
        self._replacement = extract_rule_replacement_string(self.rule)

    def _set_environment_str(self):
        """ Setting the environment of given the rule. """
        self._environment = extract_rule_environment_string(self.rule)

    def is_valid(self) -> bool:
        """ Tests the validity of the rule string (not yet fully implemented). """
        validity = True

        validity = validity and self.rule.count('->') <= 1
        validity = validity and self.rule.count('/') <= 1

        return validity

    def _set_change_dict(self):
        """ Getting the lists of changes. """
        if self.phoneme_catalog is not None:
            target_list = process_rule_element(self.target.replace('0', ''), self.phoneme_catalog)
            replacement_list = process_rule_element(self.replacement, self.phoneme_catalog)
            environment_list = process_rule_element(self.environment, self.phoneme_catalog)

            self._change_dict = get_change_dict(target_list, replacement_list, environment_list)
            self._change_transliterator = CustomTransliterator(self.change_dict)
        else:
            self._change_dict = None
            self._change_transliterator = None

    def load_phoneme_catalog(self, phoneme_catalog: Union[PhonemeCatalog, None]):
        """ Loading new phoneme catalog. The initial and final lists are updated. """
        self._phoneme_catalog = phoneme_catalog
        self._set_change_dict()

    def _clear_phoneme_catalog(self):
        """ Clears the phoneme catalog and the initial and final lists. """
        self._phoneme_catalog = None
        self._change_dict = None
        self._change_transliterator = None

    def apply_rule(self, words: Union[str, List[str]]) -> Tuple[List[str], List[bool]]:
        """
        Parameters
        ----------
        words: Union[str, List[str]]
            A word or a list of words to apply the phonological rule onto.
        Returns
        -------
        Tuple[List[str], List[bool]]
            A list of the changed words and a list of bools showing which words changed and which did not.
        """
        if isinstance(words, str):
            words = [words]

        return apply_sound_change(words, self._change_transliterator)


def extract_rule_target_string(rule: str) -> str:
    """
    A function to locate the "Target" part of a phonological rule.
    Context: A phonological rule has the format "Target -> Replacement / Environment".

    Parameters
    ----------
    rule: str
        A string that contains a phonological rule (e.g. "t -> r / _#").

    Returns
    -------
    str
        A string that contains only the "Target" part of the phonological rule ("t" in the given example rule).

    Raises
    ValueError
        If there is more than one arrows (->).

    Examples
    --------
    >>> extract_rule_target_string("t -> r / _#")
    't'
    """
    arrow_count = rule.count('->')
    if not arrow_count:
        return ''
    elif arrow_count == 1:
        return rule.split('->')[0].replace(' ', '')
    else:
        raise ValueError(f"{rule} has more than one '->'.")


def extract_rule_replacement_string(rule: str) -> str:
    """
    A function to locate the "Replacement" part of a phonological rule.
    Context: A phonological rule has the format "Target -> Replacement / Environment".

    Parameters
    ----------
    rule: str
        A string that contains a phonological rule (e.g. "t -> r / _#").

    Returns
    -------
    str
        A string that contains only the "Replacement" part of the phonological rule ("r" in the given example rule).

    Raises
    ValueError
        If there is more than one arrows (->) or  forward slashes (/).

    Examples
    --------
    >>> extract_rule_replacement_string("t -> r / _#")
    'r'
    """
    arrow_count = rule.count('->')
    slash_count = rule.count('/')
    if not arrow_count and slash_count == 1:
        return rule.split('/')[0].replace(' ', '')
    elif arrow_count == 1 and not slash_count:
        return rule.split('->')[1].replace(' ', '')
    elif arrow_count == 1 and slash_count == 1:
        return rule.split('->')[1].split('/')[0].replace(' ', '')
    else:
        raise ValueError(f"{rule} has more than one '->' or '/'.")


def extract_rule_environment_string(rule: str) -> str:
    """
    A function to locate the "Environment" part of a phonological rule.
    Context: A phonological rule has the format "Target -> Replacement / Environment".

    Parameters
    ----------
    rule: str
        A string that contains a phonological rule (e.g. "t -> r / _#"). The "Environment", when defined, must always
        come with an underscore (_).

    Returns
    -------
    str
        A string that contains only the "Environment" part of the phonological rule ("_#" in the given example rule).

    Raises
    ValueError
        If there is more than one forward slashes (/) or if the underscore (_) is missing.

    Examples
    --------
    >>> extract_rule_environment_string("t -> r / _#")
    '_#'
    """
    slash_count = rule.count('/')
    if not slash_count:
        return '_'
    elif slash_count:
        underscore_count = rule.count('_')
        if not underscore_count:
            raise ValueError(f"{rule} does not have an underscore ('_') in the environment.")
        return rule.split('/')[-1].replace(' ', '')
    else:
        raise ValueError(f"{rule} has more than one '/'.")


def process_descriptor_abbreviations(string: str) -> str:
    """
    Transliterates a part of a phonological rule's string from descriptor abbreviations to string-lists of descriptors.

    Parameters
    ----------
    string: str
        A part of a phonological rule's string, may it be the target, replacement or environment.

    Returns
    -------
    str
        A string with replaced abbreviations with their equivalent string-lists of descriptors.

    Examples
    --------
    >>> process_descriptor_abbreviations('VN(t)_!#')
    '[vowel][nasal](t)_!#'
    """
    return descriptor_abbreviation_transliterator.translit(string)


def process_square_brackets(string: str, phoneme_catalog: PhonemeCatalog) -> str:
    """
    Replaces any content inside [] (meaning a string-list of descriptors, e.g. [vowel, front]) to their equivalent list
    of phone transcriptions in {}.

    Parameters
    ----------
    string: str
        A part of a phonological rule's string, may it be the target, replacement or environment.
    phoneme_catalog: PhonemeCatalog
        The PhonemeCatalog that the rule will be applied to. Used to provide a list of phones.

    Returns
    -------
    str
        A string with replaced descriptor list (in []) to the equivalent phone list (in {}).

    Examples
    --------
    >>> pc = PhonemeCatalog(['a', 'e', 'i', 'o', 'u', 'y', 'p', 't', 'k', 'l', 'r', 'm', 'n'])
    >>> process_square_brackets('[vowel][nasal](t)_!#', pc)
    '{a,e,i,o,u,y}{m,n}(t)_!#'
    """
    # find occurrences of objects in []. Each disparate occurrence inside [] is only needed
    # once (e.g. [vowel] in [vowel][vowel]). In our example it will be ['[nasal]', '[vowel]']
    results = list(np.unique(re.findall('\[.*?\]', string)))

    # A list of lists of descriptors e.g. [['nasal'], ['vowel']]
    descriptors_list = [result.strip('][').split(',') for result in results]

    # finding phones by descriptor criteria [['nasal'], ['vowel']] -> [['m', 'n'], ['a', 'e', 'i', 'o', 'u', 'y']]
    phone_lists = [[phone.transcription for phone in phoneme_catalog.find_phones_with_descriptors(descriptors, True)]
                   for descriptors in descriptors_list]

    # making the list of lists of IPA characters to a list of string-lists e.g. ['{m,n}', '{a,e,i,o,u,y}']
    phone_curly_bracket_lists = ["{" + ','.join(phone_list) + "}" for phone_list in phone_lists]

    # Takes pairs of []-strings and {}-strings and applies the change to the original string
    # e.g. {a,e,i,o,u,y}{m,n}(t)_!#
    for result, curly_bracketed_lists in zip(results, phone_curly_bracket_lists):
        string = string.replace(result, curly_bracketed_lists)

    return string


def process_parenthesis(string: str) -> str:
    """
    With a rule that has gone through the abbreviation and square bracket processes, finds optional elements with ()
    and adds an empty value to a list (e.g. from {a,e,i,o,u,y} to {a,e,i,o,u,y,}).

    Parameters
    ----------
    string: str
        A rule that has gone through the abbreviation and square bracket processes.

    Returns
    -------
    str:
        A string with replaced parenthesis for a list with an added empty element.

    Examples
    --------
    >>> process_parenthesis('{a,e,i,o,u,y}{m,n}(t)_!#')
    '{a,e,i,o,u,y}{m,n}{t,}_!#'
    """
    # similar to process_square_brackets, finds all unique parenthesis occurrences, e.g. ['(t)']
    results = np.unique(re.findall('\(.*?\)', string))

    # gets the list of lists of IPA characters, e.g. [['t', '']]
    parenthesis_content = [result.strip(')(}{').split(',') + [''] for result in results]

    # turns each list of IPA characters into a string-list, e.g. ['{t,}']
    phone_curly_bracket_lists = ["{" + ','.join(phone_list) + "}" for phone_list in parenthesis_content]

    # apply changes to initial string, yielding the final result '{a,e,i,o,u,y}{m,n}{t,}_!#'
    for result, curly_bracketed_lists in zip(results, phone_curly_bracket_lists):
        string = string.replace(result, curly_bracketed_lists)

    return string


def process_exclamation_mark(string: str, phoneme_catalog: PhonemeCatalog) -> str:
    """
    Processing the exclaimation mark (!) notation in a phonological rule's string that has been almost fully processed
    and only contains IPA characters, underscores "_" and word boundary marks (#).

    When using "!", we also assume word boundary is in the list of available phones.

    Parameters
    ----------
    string: str
        A rule that has gone through the abbreviation, square bracket and parenthesis processes.
    phoneme_catalog: PhonemeCatalog
        The PhonemeCatalog that the rule will be applied to. Used to provide a list of phones.

    Returns
    -------
        A string that replaced any "!" and their proceding character list to its opposite (allowed) character list.

    Examples
    --------
    >>> pc = PhonemeCatalog(['a', 'e', 'i', 'o', 'u', 'y', 'p', 't', 'k', 'l', 'r', 'm', 'n'])
    >>> process_exclamation_mark('{a,e,i,o,u,y}{m,n}{t,}_!#', pc)
    '{a,e,i,o,u,y}{m,n}{t,}_{a,e,i,k,l,m,n,o,p,r,t,u,y}'
    """
    available_phones = [phone.transcription for phone in phoneme_catalog.phones] + ['#']

    all_marks = list(re.finditer('!', string))
    while len(all_marks):
        mark = all_marks[0]
        if string[mark.start() + 1] == '{':  # if the proceeding is a list of characters

            # the end index of the list, is the same as the closing of the bracket that starts after the "!".
            end_index = [result.start() for result in re.finditer('}', string) if result.start() > mark.start()][0]

            # getting the string-list of prohibited characters.
            substring = string[mark.start() + 2: end_index]

            # getting the list of characters that are prohibited.
            char_list = [char for char in substring if char not in [',', ' ']]

        else:  # if the proceeding is a single character
            end_index = mark.start() + 1
            char_list = [string[end_index]]

        # getting the characters that are not prohibited as a string-list.
        new_element = '{' + ','.join([phone for phone in available_phones if phone not in char_list]) + '}'

        # replace !+character-list with allowed elements list
        string = string[:mark.start()] + new_element + string[end_index + 1:]

        all_marks = list(re.finditer('!', string))

    return string


def process_curly_brackets(string: str) -> List[str]:
    """
    Finds all the potential combinations in a string of character string-lists
    (e.g. {e, i}{n,m}_ would yield ['en_', 'em_', 'in_', 'im_']).

    Parameters
    ----------
    string: str
        A rule that has gone through the abbreviation, square bracket, parenthesis and exclamation mark processes.

    Returns
    -------
    List[str]
        A list of strings of all the potential combinations.

    Examples
    --------
    >>> process_curly_brackets('{e,i}{m,n}_')
    ['em_', 'en_', 'im_', 'in_']
    >>> process_curly_brackets('{a,e,i,o,u,y}{m,n}{t,}_{a,e,i,k,l,m,n,o,p,r,t,u,y}')
    ['amt_a', 'amt_e', 'amt_i', 'amt_k', 'amt_l', 'amt_m', 'amt_n', 'amt_o', 'amt_p', 'amt_r', 'amt_t', 'amt_u', 'amt_y', 'am_a', 'am_e', 'am_i', 'am_k', 'am_l', 'am_m', 'am_n', 'am_o', 'am_p', 'am_r', 'am_t', 'am_u', 'am_y', 'ant_a', 'ant_e', 'ant_i', 'ant_k', 'ant_l', 'ant_m', 'ant_n', 'ant_o', 'ant_p', 'ant_r', 'ant_t', 'ant_u', 'ant_y', 'an_a', 'an_e', 'an_i', 'an_k', 'an_l', 'an_m', 'an_n', 'an_o', 'an_p', 'an_r', 'an_t', 'an_u', 'an_y', 'emt_a', 'emt_e', 'emt_i', 'emt_k', 'emt_l', 'emt_m', 'emt_n', 'emt_o', 'emt_p', 'emt_r', 'emt_t', 'emt_u', 'emt_y', 'em_a', 'em_e', 'em_i', 'em_k', 'em_l', 'em_m', 'em_n', 'em_o', 'em_p', 'em_r', 'em_t', 'em_u', 'em_y', 'ent_a', 'ent_e', 'ent_i', 'ent_k', 'ent_l', 'ent_m', 'ent_n', 'ent_o', 'ent_p', 'ent_r', 'ent_t', 'ent_u', 'ent_y', 'en_a', 'en_e', 'en_i', 'en_k', 'en_l', 'en_m', 'en_n', 'en_o', 'en_p', 'en_r', 'en_t', 'en_u', 'en_y', 'imt_a', 'imt_e', 'imt_i', 'imt_k', 'imt_l', 'imt_m', 'imt_n', 'imt_o', 'imt_p', 'imt_r', 'imt_t', 'imt_u', 'imt_y', 'im_a', 'im_e', 'im_i', 'im_k', 'im_l', 'im_m', 'im_n', 'im_o', 'im_p', 'im_r', 'im_t', 'im_u', 'im_y', 'int_a', 'int_e', 'int_i', 'int_k', 'int_l', 'int_m', 'int_n', 'int_o', 'int_p', 'int_r', 'int_t', 'int_u', 'int_y', 'in_a', 'in_e', 'in_i', 'in_k', 'in_l', 'in_m', 'in_n', 'in_o', 'in_p', 'in_r', 'in_t', 'in_u', 'in_y', 'omt_a', 'omt_e', 'omt_i', 'omt_k', 'omt_l', 'omt_m', 'omt_n', 'omt_o', 'omt_p', 'omt_r', 'omt_t', 'omt_u', 'omt_y', 'om_a', 'om_e', 'om_i', 'om_k', 'om_l', 'om_m', 'om_n', 'om_o', 'om_p', 'om_r', 'om_t', 'om_u', 'om_y', 'ont_a', 'ont_e', 'ont_i', 'ont_k', 'ont_l', 'ont_m', 'ont_n', 'ont_o', 'ont_p', 'ont_r', 'ont_t', 'ont_u', 'ont_y', 'on_a', 'on_e', 'on_i', 'on_k', 'on_l', 'on_m', 'on_n', 'on_o', 'on_p', 'on_r', 'on_t', 'on_u', 'on_y', 'umt_a', 'umt_e', 'umt_i', 'umt_k', 'umt_l', 'umt_m', 'umt_n', 'umt_o', 'umt_p', 'umt_r', 'umt_t', 'umt_u', 'umt_y', 'um_a', 'um_e', 'um_i', 'um_k', 'um_l', 'um_m', 'um_n', 'um_o', 'um_p', 'um_r', 'um_t', 'um_u', 'um_y', 'unt_a', 'unt_e', 'unt_i', 'unt_k', 'unt_l', 'unt_m', 'unt_n', 'unt_o', 'unt_p', 'unt_r', 'unt_t', 'unt_u', 'unt_y', 'un_a', 'un_e', 'un_i', 'un_k', 'un_l', 'un_m', 'un_n', 'un_o', 'un_p', 'un_r', 'un_t', 'un_u', 'un_y', 'ymt_a', 'ymt_e', 'ymt_i', 'ymt_k', 'ymt_l', 'ymt_m', 'ymt_n', 'ymt_o', 'ymt_p', 'ymt_r', 'ymt_t', 'ymt_u', 'ymt_y', 'ym_a', 'ym_e', 'ym_i', 'ym_k', 'ym_l', 'ym_m', 'ym_n', 'ym_o', 'ym_p', 'ym_r', 'ym_t', 'ym_u', 'ym_y', 'ynt_a', 'ynt_e', 'ynt_i', 'ynt_k', 'ynt_l', 'ynt_m', 'ynt_n', 'ynt_o', 'ynt_p', 'ynt_r', 'ynt_t', 'ynt_u', 'ynt_y', 'yn_a', 'yn_e', 'yn_i', 'yn_k', 'yn_l', 'yn_m', 'yn_n', 'yn_o', 'yn_p', 'yn_r', 'yn_t', 'yn_u', 'yn_y']
    """
    string_list = re.split('{|}', string)
    # string_list = [s for s in string_list if s != '']  # ignore empty string lists ({}).
    chars_lists = [s.split(',') for s in string_list]

    combinations = chars_lists[0]
    for i in range(1, len(chars_lists)):
        combinations = list(itertools.product(combinations, chars_lists[i]))
        combinations = [''.join(x) for x in combinations]

    return combinations


def process_rule_element(string: str, phoneme_catalog: PhonemeCatalog) -> List[str]:
    """
    Applies all the processes required to turn a phonological rule's substring to a list of strings for each different
    option.

    Parameters
    ----------
    string: str
        The initial string to be processed, either it is a target, replacement or environment.
    phoneme_catalog: PhonemeCatalog
        Here to provide a list of valid phones to replaces the descriptors and the descriptor abbreviations.

    Returns
    -------
    List[str]
        A list of strings for every individual option in the given rule substring.

    Examples
    --------
    >>> pc = PhonemeCatalog(['a', 'e', 'i', 'o', 'u', 'y', 'p', 't', 'k', 'l', 'r', 'm', 'n'])
    >>> process_rule_element('VN(t)_!#', pc)
        ['amt_a', 'amt_e', 'amt_i', 'amt_k', 'amt_l', 'amt_m', 'amt_n', 'amt_o', 'amt_p', 'amt_r', 'amt_t', 'amt_u', 'amt_y', 'am_a', 'am_e', 'am_i', 'am_k', 'am_l', 'am_m', 'am_n', 'am_o', 'am_p', 'am_r', 'am_t', 'am_u', 'am_y', 'ant_a', 'ant_e', 'ant_i', 'ant_k', 'ant_l', 'ant_m', 'ant_n', 'ant_o', 'ant_p', 'ant_r', 'ant_t', 'ant_u', 'ant_y', 'an_a', 'an_e', 'an_i', 'an_k', 'an_l', 'an_m', 'an_n', 'an_o', 'an_p', 'an_r', 'an_t', 'an_u', 'an_y', 'emt_a', 'emt_e', 'emt_i', 'emt_k', 'emt_l', 'emt_m', 'emt_n', 'emt_o', 'emt_p', 'emt_r', 'emt_t', 'emt_u', 'emt_y', 'em_a', 'em_e', 'em_i', 'em_k', 'em_l', 'em_m', 'em_n', 'em_o', 'em_p', 'em_r', 'em_t', 'em_u', 'em_y', 'ent_a', 'ent_e', 'ent_i', 'ent_k', 'ent_l', 'ent_m', 'ent_n', 'ent_o', 'ent_p', 'ent_r', 'ent_t', 'ent_u', 'ent_y', 'en_a', 'en_e', 'en_i', 'en_k', 'en_l', 'en_m', 'en_n', 'en_o', 'en_p', 'en_r', 'en_t', 'en_u', 'en_y', 'imt_a', 'imt_e', 'imt_i', 'imt_k', 'imt_l', 'imt_m', 'imt_n', 'imt_o', 'imt_p', 'imt_r', 'imt_t', 'imt_u', 'imt_y', 'im_a', 'im_e', 'im_i', 'im_k', 'im_l', 'im_m', 'im_n', 'im_o', 'im_p', 'im_r', 'im_t', 'im_u', 'im_y', 'int_a', 'int_e', 'int_i', 'int_k', 'int_l', 'int_m', 'int_n', 'int_o', 'int_p', 'int_r', 'int_t', 'int_u', 'int_y', 'in_a', 'in_e', 'in_i', 'in_k', 'in_l', 'in_m', 'in_n', 'in_o', 'in_p', 'in_r', 'in_t', 'in_u', 'in_y', 'omt_a', 'omt_e', 'omt_i', 'omt_k', 'omt_l', 'omt_m', 'omt_n', 'omt_o', 'omt_p', 'omt_r', 'omt_t', 'omt_u', 'omt_y', 'om_a', 'om_e', 'om_i', 'om_k', 'om_l', 'om_m', 'om_n', 'om_o', 'om_p', 'om_r', 'om_t', 'om_u', 'om_y', 'ont_a', 'ont_e', 'ont_i', 'ont_k', 'ont_l', 'ont_m', 'ont_n', 'ont_o', 'ont_p', 'ont_r', 'ont_t', 'ont_u', 'ont_y', 'on_a', 'on_e', 'on_i', 'on_k', 'on_l', 'on_m', 'on_n', 'on_o', 'on_p', 'on_r', 'on_t', 'on_u', 'on_y', 'umt_a', 'umt_e', 'umt_i', 'umt_k', 'umt_l', 'umt_m', 'umt_n', 'umt_o', 'umt_p', 'umt_r', 'umt_t', 'umt_u', 'umt_y', 'um_a', 'um_e', 'um_i', 'um_k', 'um_l', 'um_m', 'um_n', 'um_o', 'um_p', 'um_r', 'um_t', 'um_u', 'um_y', 'unt_a', 'unt_e', 'unt_i', 'unt_k', 'unt_l', 'unt_m', 'unt_n', 'unt_o', 'unt_p', 'unt_r', 'unt_t', 'unt_u', 'unt_y', 'un_a', 'un_e', 'un_i', 'un_k', 'un_l', 'un_m', 'un_n', 'un_o', 'un_p', 'un_r', 'un_t', 'un_u', 'un_y', 'ymt_a', 'ymt_e', 'ymt_i', 'ymt_k', 'ymt_l', 'ymt_m', 'ymt_n', 'ymt_o', 'ymt_p', 'ymt_r', 'ymt_t', 'ymt_u', 'ymt_y', 'ym_a', 'ym_e', 'ym_i', 'ym_k', 'ym_l', 'ym_m', 'ym_n', 'ym_o', 'ym_p', 'ym_r', 'ym_t', 'ym_u', 'ym_y', 'ynt_a', 'ynt_e', 'ynt_i', 'ynt_k', 'ynt_l', 'ynt_m', 'ynt_n', 'ynt_o', 'ynt_p', 'ynt_r', 'ynt_t', 'ynt_u', 'ynt_y', 'yn_a', 'yn_e', 'yn_i', 'yn_k', 'yn_l', 'yn_m', 'yn_n', 'yn_o', 'yn_p', 'yn_r', 'yn_t', 'yn_u', 'yn_y']
    """
    string = process_descriptor_abbreviations(string)
    string = process_square_brackets(string, phoneme_catalog)
    string = process_parenthesis(string)
    string = process_exclamation_mark(string, phoneme_catalog)
    return process_curly_brackets(string)


def get_change_dict(targets: List[str], replacements: List[str], environments: List[str]) -> Dict[str, str]:
    """
    Converts the processed Target, Replacement and Environment lists into a dictionary with "before" and "after"
    phonological change substrings as keys-values. The conversition happens by taking all the combinations
    of target and replacement and putting them in the position of the '_' in the environment.

    Parameters
    ----------
    targets: List[str]
        A list of Target strings for a given phonological change.
    replacements: List[str]
        A list of replacement strings for a given phonological change.
    environments: List[str]
        A list of environment strings for a given phonological change.

    Returns
    -------
    Dict[str, str]
        A dict of before-after lists. The keys are the before-change sounds and the values are the after-change sounds.

    Examples
    --------
    From the phonological rule "N -> r / V_#" with N={m,n} and V={a,e,i,o,u,y}

    >>> get_change_dict(['m', 'n'], ['r'], ['a_#', 'e_#', 'i_#', 'o_#', 'u_#', 'y_#'])
    {'am#': 'ar#', 'em#': 'er#', 'im#': 'ir#', 'om#': 'or#', 'um#': 'ur#', 'ym#': 'yr#', 'an#': 'ar#', 'en#': 'er#', 'in#': 'ir#', 'on#': 'or#', 'un#': 'ur#', 'yn#': 'yr#'}
    """

    # gets all the combinations of each target and environment and put them in one list of tuples
    # e.g. for targets=['m', 'n'] and environments=['a_#', 'e_#', 'i_#', 'o_#', 'u_#', 'y_#']:
    # [('m', 'a_#'), ('m', 'e_#'), ('m', 'i_#'), ('m', 'o_#'), ('m', 'u_#'), ('m', 'y_#'),
    #  ('n', 'a_#'), ('n', 'e_#'), ('n', 'i_#'), ('n', 'o_#'), ('n', 'u_#'), ('n', 'y_#')]
    string_combinations = list(itertools.product(targets, environments))

    # we combine the tuples in the list, by replacing the "_" in the environment (second position in each tuple)
    # in our example: ['am#', 'em#', 'im#', 'om#', 'um#', 'ym#', 'an#', 'en#', 'in#', 'on#', 'un#', 'yn#']
    init_list = [comb_str[1].replace('_', comb_str[0]) for comb_str in string_combinations]

    # if the replacement is a single item, then we multiply it by the length of the initial list.
    # TODO: play around with different rules with different number of replacements, targets and environments.
    if len(replacements) == 1:
        replacements = replacements * len(init_list)

    # use the same function we used for the init_list, to get the final list. Now we re substituting '_' with each
    # replacement string.
    # in our example: ['ar#', 'er#', 'ir#', 'or#', 'ur#', 'yr#', 'ar#', 'er#', 'ir#', 'or#', 'ur#', 'yr#']
    final_list = [comb_str[1].replace('_', replacements[i]) for i, comb_str in enumerate(string_combinations)]

    return {init: final for (init, final) in zip(init_list, final_list)}


def apply_sound_change(words: List[str], change_transliterator: CustomTransliterator) -> Tuple[List[str], List[bool]]:
    """
    Using a custom transliterator, this function applies sounds changes to a list of words.
    Pending: This function will become more complex when we add the wildcard option "...", the stem option "$" or the
    weird number options.

    Parameters
    ----------
    words: List[str]
        A list of all the words that may undergo phonological change.
    change_transliterator: Dict[str, str]
        A transliterator that can be used to apply a set of sound changes.

    Returns
    -------
    Tuple[List[str], List[bool]]
        A tuple of two items; the list of words that the phonological change has been applied to, and a list of bool
        indicating whether a word has changed by index.
    """
    did_words_change = []
    new_words = []
    for word in words:  # iterating through word list
        new_word = change_transliterator.translit(f'#{word}#').strip('#').replace('0', '')
        did_words_change.append(new_word != word)
        new_words.append(new_word)

    return new_words, did_words_change
