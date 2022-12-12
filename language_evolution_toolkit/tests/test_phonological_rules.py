from language_evolution_toolkit.phonemes import PhonemeCatalog, Phoneme
from language_evolution_toolkit.phonological_rules import PhonologicalRule


word_list = [
    'hat',
    'ase',
    'set',
    'ipa',
    'ipe',
    'apia',
    'star',
    'stat',
    'strap',
    'pat',
    'pʰat',
    'pse',
    'pʰse',
    'ask',
    'askʰ',
    'apa',
    'apʰa',
    'ata',
    'atʰa',
]

pc = PhonemeCatalog(['a', 'e', 'i', 'o', 'u', 'y', 'l', 'r', 'm', 'n', 's', 'ʃ', 'h',
                     {'p': ['p', 'pʰ']}, {'t': ['t', 'tʰ']}, {'k': ['k', 'kʰ']}])
print(pc.phonemes)


pr = PhonologicalRule('t -> r /a_#', pc)
print(pr.apply_rule(word_list))

pr = PhonologicalRule('s -> ʃ / ![vowel]_', pc)
print(pr.apply_rule(word_list))

pr = PhonologicalRule('h -> 0 / #_', pc)
print(pr.apply_rule(word_list))

pr = PhonologicalRule('s -> 0 / _{e,i}', pc)
print(pr.apply_rule(word_list))

pr = PhonologicalRule('i -> e / _([consonant])a', pc)
print(pr.apply_rule(word_list))

pr = PhonologicalRule('s -> h / #_', pc)
print(pr.apply_rule(word_list))

pr = PhonologicalRule('{t,k} -> 0 / _#', pc)
print(pr.apply_rule(word_list))

pr = PhonologicalRule('{p, t, k}[vowel] -> {b, d, g}[vowel]', pc)
print(pr.apply_rule(word_list))
print(pr.change_dict)

pr = PhonologicalRule('{p, t, k, pʰ, tʰ, kʰ}[vowel] -> {b, d, g, bʰ, dʰ, gʰ}[vowel]', pc)
print(pr.apply_rule(word_list))


pr = PhonologicalRule('s t -> z d / _([vowel])r', pc)
print(pr.apply_rule(word_list))

pr = PhonologicalRule(' a -> e / _{[consonant], #}', pc)
print(pr.apply_rule(word_list))

pr = PhonologicalRule('[vowel, !back] -> o', pc)
print(pr.apply_rule(word_list))
#
pr = PhonologicalRule('0 -> a /#_Xt', pc)
print(pr.apply_rule(word_list))

# print(get_change_dict(['p'], ['b'], ['_']))  # n=1, m=1, k=1
# print(get_change_dict(['p', 'b'], ['m'], ['_']))  # n=2, m=1, k=1
# print(get_change_dict(['p'], ['b'], ['#_', '_#']))  # n=1, m=2, k=1
# print(get_change_dict(['p', 'b'], ['m'], ['#_', '_#']))  # n=2, m=2, k=1
# print(get_change_dict(['p', 't', 'k'], ['b', 'd', 'g'], ['_']))  # n=3, m=1, k=n
# print(get_change_dict(['p', 't', 'k'], ['b', 'd', 'g'], ['#_', '_#']))  # n=3, m=2, k=n
# print(get_change_dict(['a'], ['es', 'ih'], ['_s', '_h']))  # n=1, m=2, k=n*m
