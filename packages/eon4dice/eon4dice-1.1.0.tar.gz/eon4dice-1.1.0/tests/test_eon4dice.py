from unittest import TestCase
from src.eon4dice import dice


class Test(TestCase):
    def test_roll(self):
        test_series = [
            '5T6+2',
            '1T6',
            '1t100',
            '2T6+0',
        ]
        for test in test_series:
            assert(dice.roll(test, verbose=True) > 0)

        assert(dice.roll(2) > 0)
        assert (dice.roll(3, sides=10, bonus=0, verbose=True) > 0)
        assert (dice.roll(1, 100, 1) > 0)
        assert (dice.roll(4, bonus=3, verbose=True) > 0)
        assert (dice.roll(1, 10) > 0)

