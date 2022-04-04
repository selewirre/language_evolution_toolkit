# Phonological Rules

We will start with the simple phonological rule definition, and we will work towards more complicated examples. This [page](https://chridd.nfshost.com/diachronica/all) has multiple sound changes that occurred in languages of the world. Basic rule format is: 

target -> replacement / environment

where:
1. target is the phone that will be changed
2. replacement is the phone that the target will be replaced with
3. environment is the phonological environment (condition) in which the phonological rule will take place.

All phones are denoted in IPA format. No romanization is allowed.
Potential special characters that may be used: -> / & | [] {} () ; # 0 _ , ! ' . $ % + -

| Character | Meaning/Usage                                                        | Example                                              | Example Notes                                                                               |
|-----------|----------------------------------------------------------------------|------------------------------------------------------|---------------------------------------------------------------------------------------------|
| []        | the phone descriptors                                                | t or [alveolar, voiceless, plosive]                  | Two ways to write [t].                                                                      |
| ->        | from target (left) to replacement (right)                            | t -> r                                               | [t] becomes [r].                                                                            |
| \_        | where the sound change will occur in an environment                  | \_a                                                  | Replacement will occur before [a].                                                          |
| #         | the boundary of a word (either start or end)                         | \_#                                                  | Replacement will occur at end of word.                                                      |
| /         | the environment of the change is on the right                        | t -> r / \_#                                         | [t] becomes [r] if [t] is word final.                                                       |
| !         | "except when..." or "not"                                            | s -> ʃ / !\[vowel\]\_                                | [s] becomes [ʃ] if [s] is NOT after a vowel.                                                |
| 0         | nothing                                                              | h -> 0 / #\_                                         | [h] disappears if [h] is word initial.                                                      |
| $         | the boundary of a stem (either start or end)                         | \$\[consonant\][vowel]\$ -> \$[vowel]\[consonant\]\$ | All \[consonant\][vowel] *stems* become [vowel]\[consonant\]. (For Future!)                 |
| % (or .?) | the boundary of a syllable (either start or end)                     | ???                                                  | (For Future!)                                                                               |
| {}        | a list of phones                                                     | s -> 0 / \_{e,i}                                     | [s] disappears if [s] comes before either [e], or [i].                                      |
| '         | stressed  (alternatively, [stress] can be used (e.g.[vowel, stress]) | [vowel] -> 0 / #\_[consonant]'[vowel]                | Vowels disappear if vowel is word initial before a stressed consonant+vowel. (For Future!)  |
| ()        | optional phone or list of phones                                     | i -> a / \_([consonant])a                            | [i] becomes [a] if [a] is found either before [a] or before consonant+[a].                  |


Additional examples:

| Example                              | Notes                                                                                                        |
|--------------------------------------|--------------------------------------------------------------------------------------------------------------|
| s -> h / #\_                         | [s] becomes [h] if [s] is word initial.                                                                      |
| j -> 0 / [consonant] k\_$            | [j] disappears if found after a consonant + [k] and at the end of a stem. (Will work properly in the future) |
| aː -> a / \_#                        | Long [a] becomes [a] if long [a] is word final. (Will work properly in the future)                           |
| w -> 0 / {k,ɡ}\_                     | [w] disappears if found before either [k] or [g].                                                            |
| {t,k} -> 0 / \_#                     | [t] or [k] disappear if [t] or [k] are word final respectively.                                              |
| {b, d, g}[vowel] -> {p, t, k}[vowel] | [b]+vowel becomes [p]+vowel, [d]+vowel becomes [t]+vowel and [g]+vowel becomes [k]+vowel.                    |
| s d -> z r / \_([vowel])j            | \[s\][d] becomes \[z\][r] if \[s\][d] is found before either vowel + [j] or just before [j].                 |
| a -> e / \_{[consonant], #}          | [a] becomes [e] when found either before a constant, or [a] is word final.                                   |
| [vowel, !back] -> o                  | All non-back vowels become [o]. Note here that !back does not mean -back, but rather {front, mid}.           |

Examples that do NOT work:

| Example                              | Notes                                                                                                                      |
|--------------------------------------|----------------------------------------------------------------------------------------------------------------------------|
| [vowel, front] -> [vowel, back]      | All front vowels become back vowels. Can not work because the two strin-lists are not correlated with their other futures. |
| {[vowel, front], !e} -> i            | All front vowels except [e] become [i].                                                                                    |


Special cases (seen in [SCA](http://zompist.com/scahelp.html)):

| Name         | Example      | Notes                                                         |
|--------------|--------------|---------------------------------------------------------------|
| Epenthesis   | 0 -> a /#\_h | All words staring with [h] will now start with \[a\][h].      |
| Metathesis   | -            | Not implemented (regular: rl -> lr).                          |
| Degemination | -            | Not implemented (regular: mm -> m or m -> 0 / m_ or mː -> m). |
| Gemination   | -            | Not implemented (regular: m -> mm).                           |


To be defined:

1. Embedded lists in phone descriptors (e.g. [vowel, {front, mid}]). This can currently be implemented as {[vowel, front], [vowel, mid]}.
2. (Parentheses inside descriptor lists [] are redundant. The descriptor will catch the item in parentheses anyway.)
3. Syllable boundary (%, . by [diachronica](https://chridd.nfshost.com/diachronica/all#Abbreviations)).
4. Angled brackets (see end of [phonological rule wikipedia page](https://en.wikipedia.org/wiki/Phonological_rule#Expanded_Notation)).
5. Wildcard or ... defined in [SCA](http://zompist.com/scahelp.html) and in [diachronica](https://chridd.nfshost.com/diachronica/all#Abbreviations).
6. A few more [diachronica](https://chridd.nfshost.com/diachronica/all#Abbreviations) abbreviations:
   1. X_0 = The same/an identical X
   2. X_n = The nth X of a sequence or series 
   3. X_x = All X of a sequence or series