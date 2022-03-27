# Version Control Log

- 27/03/2022; v0.0.2: Added Phoneme list class.
  - Defined *PhonemeCatalog* as a class to hold a list of *Phonemes*.
  - Defined *UniquePhonemeCatalog* as a class to hold a list of unique *Phonemes*.
  - *ImmutableProperty* will now raise an AttributeError if an attempt to change its value is made.
- 26/03/2022; v0.0.1: Initial commit.
  - Defined *LinguisticObject* as a base object for later operations, such as object comparisons and tracking the object progression over different language evolution stages.
  - Defined *TrackingID* to track changes of *LinguisticObjects* over different language evolution stages.
  - Defined *ImmutableProperty* as the main properties of *LinguisticObjects* and *TrackingID*.
  - Defined *Phoneme* as a *LinguisticObject* with *ImmutableProperties*: *unicode_string*, *romanization*, *ipa_chars*, and *descriptors*.
