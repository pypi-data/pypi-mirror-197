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
Import and call the 'roll' function with the desired roll as a string:

```Python
from eon4dice import dice

result = dice.roll('4T6+2')
result2 = dice.roll('1t100')
```

D6's will always explode. No other dice (such as D10 or D100) will explode. Bonus is optional. Minus (-) can not
be used instead of plus (+)