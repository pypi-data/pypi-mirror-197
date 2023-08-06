# eon4dice
A library that handles dice rolls for the Swedish tabletop roleplaying game EON IV (https://helmgast.se/eon/).

All six sided dice rolls will explode according to Eon rules, which means that every time a 6 is rolled,
it will be removed and the die replaced two new six sided dice, which can then explode in turn.

As the rules are currently only available in Swedish, the letter T is used instead of D to denote dice.

### Installation
```
pip install eon4dice
```

### How to use
Import and call the 'roll' function. It expects input as arguments (number_of_dice, sides=6, bonus=0) or a string. Note
that the 'sides' and 'bonus' arguments are optional.  For debugging purposes, you can also set verbose=True to allow 
you to see the rolls being made.

Examples:

```Python
from eon4dice import roll

result = roll(1,100) # rolls 1T100
result = roll(3, bonus=3)  # rolls 3T6+3
result = roll(2) # rolls 2T6+0
result = roll('4T6+2')
result = roll('1t100', verbose=True)
```

D6's will always explode. No other dice (such as D10 or D100) will explode. 