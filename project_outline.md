# Language Evolution Project: A coding base-structure proposal
## Introduction

I would like to start off by saying that this is a very exciting project!

Here I will build base-code that allows users to apply changes on a given/imported language/conlang.


## Linguistic entities

I would like to start off by figuring out an efficient format to represent various linguistic entities.

1. Phone
2. Phoneme
3. PhonemeCatalog
4. Conditions
5. Phonotactics
6. Phonology
7. Inflections
8. Words
9. Word families
10. Lexicon
11. Grammar
12. Syntax
13. Language
14. Phonetic change
15. Language History

In the following, I will talk about each entity and how I envision/implement its structure. 
Each entity type mentioned has its own unique base ID number and a "version" number.  Then, throughout the course of linguistic history, the base ID number stays the same, but the version number changes. This will help in easily tracking down the history of each entity.  

### Phone
A *Phone* is an object that holds:

1. The IPA symbols representing the speech sounds (e.g. [pʰ] as pʰ).
2. The descriptors of the sound (e.g. bilabial consonant plosive voiceless aspirated).

### Phoneme
A *Phoneme* is an object that carries the information of a single phonemic transcription:

1. The phonemic transcription (e.g. /p/ as p).
2. Multiple *Phones* which are the allophones of the phoneme (e.g. pʰ and p).
3. The common descriptors of all the sounds comprising the phoneme (e.g. bilabial consonant plosive voiceless).
4. Rules for where to use different phonemes (for implementation I might use/get inspired by this: https://github.com/Schyrsivochter/PythonSCA).

### Conditions
*Condition* is a set of rules of phonetic alteration in a given phonetic environment.
It can be used for *Inflections*, *PhoneticChanges* etc. I have tried research/figuring out a good way to represent conditions, but I would like to ask the community's help on this one. The requirement is that each condition needs to have its own symbol so that it can be recognizable and at the same time readable by the user.

Here is the set of rules I have come up with regarding inflections (it is partially specified for input in a python code, so please forgive my weird format). They are given in a form of a rather absurd example of noun inflections.

| Dummy Inflection Name | Example Condition                              | Type of Phonetic Change/Inflection                                                                                   |
|-----------------------|------------------------------------------------|----------------------------------------------------------------------------------------------------------------------|
| Singular/Nominative   | '-os'                                          | suffix                                                                                                               |
| Singular/Accusative   | ('r-', 'L1 is: a')                             | prefix only if before 'a', else nothing                                                                              |
| Singular/Dative       | {('ke-t', 'L1 is: C'), ('k-t', 'L1: is V')}    | circumfix with two conditions for consonants and vowels. First rule above second etc.                                |
| Singular/Locative     | 'S2+it+S1'                                     | infix inserted after the second syllable and before one syllable (eg. a.pu.re -> apuruitre)                          |
| Singular/Genitive     | '~ba',                                         | right duplifix (e.g. tuk -> tuk~batuk)                                                                               |
| Plural/Nominative     | 'en~S2>',                                      | left duplifix duplicated up to second syllable (e.g. tukera -> entuke~tukera) if S2all then: tukera -> enkera~tukera |
| Plural/Accusative     | ('L1+i+L2+e+L3')                               | transfix on discontinuous stem (e.g. ktb-> kiteb). The number of 'L...' marks the number of stem letters.            |
| Plural/Dative         | 'L2<+e+L3',                                    | partial transfix on discontinuous stem (e.g. ktb-> kteb)                                                             |
| Plural/Locative       | ('ee', 'Starts with: Coo', 'Has syllables: 1') | simulfix (replacement of ee with oo after first consonant (e.g. foot -> feet)                                        |
| Plural/Genitive       | 'S2->0'                                        | disfix (e.g. on second syllable tukari -> turi)                                                                      |
| Dual/Nominative       | TBD about tones and stress                     | suprafix                                                                                                             |

Writing this, I know see that there's alot missing, alongside some mistakes, but I believe it is a good start.


### Phonotactics
*Phonotactics* is an alternative entity that will hold all the given *Conditions* of appearance of phonemes (e.g. ŋ appearing at non-initial word positions).


### Phonology
*Phonology* will be the entity that hold:

1. All *Phonemes* of a given *Language*.
2. The *Phonotactics* of a given *language*.
3. The transliteration matrices for changing between *IPA*, *Romanization*, and *Glyphs*.
4. *Phonology* will also be able to warn the user if their romanization and IPA can be cross-transliterated.


### Inflections
An *Inflection* is an entity that holds:

1. The *Phonemes* that comprise the inflection.
2. The part of speach the inflection refers to.
3. The *Conditions* that dictate its application.


### Words
A *Word* is an entity that hold:

1. The *Stem* of the word.
2. The part of speech that it belongs to (automatic inflection will be applied).
3. Semantics of the word.
4. *Words* are always part of a *WordFamily* (see below). They are not sand-alone entities.


### Word Families
A *WordFamily* is an entity that holds:

1. The *Stem* of the word.
2. All possible inflections and parts of speech.
3. All the *words* that are derived from the stem and each inflection.


### Lexicon
*Lexicon* is a list of all the *WordFamilies* contained in a *Language*.


### Grammar
*Grammar* is the list of all possible infections contained in a *Language*.


### Syntax
*Syntax* is a list of all conditions/rules which the *Lexicon* can follow. This is very vague and needs to be quantitatively defined for programming purposes.


### Language
*Language* is the entity that holds:

1. *Phonology*
2. *Lexicon*.
3. *Grammar*.
4. *Syntax*.


### Phonetic change
*PhoneticChange* is a *Condition*. Unless otherwise specified, it will be applied in all words in the lexicon.


### Language History
*LanguageHistory* is the one that will apply and hold all the information about a give language and its evolution over time. It holds:

1. A list of all phonetic changes.
2. A list of all languages after each phonetic change. 


## Closing Remarks

For now, this is the structure I am working on right now. It is not without its faults. I would love suggestions about all the above and figure out an optimal definition and functionality for each entity.

Best,

Selewirre (they/them)