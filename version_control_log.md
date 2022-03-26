# Version Control Log

- 26/03/2022: Initial commit.
  - Defined *LinguisticObject* as a base object for later operations, such as object comparisons and tracking the object progression over different language evolution stages.
  - Defined *TrackingID* to track changes of *LinguisticObjects* over different language evolution stages.
  - Defined *ImmutableProperty* as the main properties of *LinguisticObjects* and *TrackingID*.
  - Defined *Phoneme* as a *LinguisticObject* with *ImmutableProperties*: *unicode_string*, *romanization*, *ipa_chars*, and *descriptors*.
