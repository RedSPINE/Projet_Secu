# Projet_Secu

## Anonymisation process

### ARX

ARX used for k-anonymisation, t-closeness, l-diversité, differencial privacy, and more.

Combination of k-anonymisation and l-diversity. 50% of lines max deleted.

Different hierarchy for quasi-identifier. Each date change to the first of current month. Tests to
find a way to shuffle prices and quantities in an optimized way. The most efficient tactic found
is to create a 2€ interval for the price and not more than plus or minus 4 for quantity 
modificaition.

We fixed each purchase time to 13h37 for more *swag*.

### Refactor scripts

As ARX can't produce files with the format asked by the rules of the competition, some scripts 
were created to refactor data to make it usable.

Hashed identifiers.
