from language_evolution_toolkit.phonemes import PhonemeCatalog
from language_evolution_toolkit.phonological_rules import PhonologicalRule


word_list = [
    'apa',
    'ata',
    'hat',
    'pse',
    'ase',
    'set',
    'ipa',
    'ipe',
    'apia',
    'ask',
    'star',
    'stat',
    'strap'
]
pc = PhonemeCatalog(['a', 'e', 'i', 'o', 'u', 'y', 'p', 't', 'k', 'l', 'r', 'm', 'n', 's', 'ʃ', 'h'])

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

pr = PhonologicalRule('s t -> z d / _([vowel])r', pc)
print(pr.apply_rule(word_list))

pr = PhonologicalRule(' a -> e / _{[consonant], #}', pc)
print(pr.apply_rule(word_list))

pr = PhonologicalRule('[vowel, !back] -> o', pc)
print(pr.apply_rule(word_list))
#
pr = PhonologicalRule('0 -> a /#_h', pc)
print(pr.apply_rule(word_list))
