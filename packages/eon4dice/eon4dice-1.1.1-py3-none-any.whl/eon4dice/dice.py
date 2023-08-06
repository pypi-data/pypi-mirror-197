from random import randint


def roll(number_of_dice, sides=6, bonus=0, verbose=False):
    """Rolls the specified number of dice and returns sum plus bonus (if any). 6-sided dice will explode.

    If input is provided as a dicestring such as "5T6+2" or "1T100", it will call the decode_dicestring
    function to interpet it.
    @param number_of_dice: how many dice to roll, can also be a dicestring such as "4T6+2"
    @param sides: number of sides per dice, intended for D10's and D100's.
    @param bonus: number to modify the result.
    @param verbose: prints the number of dice, sides and bonus. Intended for debug use.
    """
    if not str(number_of_dice).isdigit():  # checks if a dicestring expression was provided
        number_of_dice, sides, bonus = decode_dicestring(number_of_dice)

    if verbose:
        print('Rolling ' + str(number_of_dice) + 'T' + str(sides) + '+' + str(bonus))

    if sides == 6:
        result = d6(number_of_dice)
    else:
        result = other_dice(number_of_dice, sides)

    return result + bonus


def decode_dicestring(dicestring):
    """Decodes a dicestring (such as "2T6+2) and returns number of dice, sides and bonus.

    :param dicestring: should look like "5T6+2", "1T100" or "2t6". Bonus is optional.
    """
    if '+' in dicestring:
        dicestring, bonus = dicestring.split('+')
        bonus = int(bonus)
    else:
        bonus = 0
    number_of_dice, sides = [int(x) for x in dicestring.lower().split('t')]
    return number_of_dice, sides, bonus




def d6(number_of_dice):
    """Rolls a number of exploding six-sided dice.

    Whenever a 6 is rolled, it is removed and two new dice are rolled and added. This is done recursively."""
    result = 0
    for x in range(number_of_dice):
        dice_roll = randint(1, 6)
        if dice_roll == 6:
            dice_roll = d6(2)
        result += dice_roll
    return result


def other_dice(number_of_dice, sides):
    """Rolls a number of dice that are not six-sided.

    This function is intended for rolling D10's and D100's but can also be used to roll other types of dice.
    """
    result = 0
    for x in range(number_of_dice):
        result += randint(1, sides)
    return result
