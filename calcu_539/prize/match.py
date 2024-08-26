from enum import Enum
from typing import List
import unittest
from unittest.mock import Mock
import sys


class StrategyMatch(Enum):
    TWO = 1
    FIVE = 5


class MatchInfo:

    @property
    def signQty(self) -> int:
        return self._signQty

    @signQty.setter
    def signQty(self, value: int):
        self._signQty = value

    @property
    def matchQty(self) -> int:
        return self._matchQty

    @matchQty.setter
    def matchQty(self, value: int):
        self._matchQty = value

    @property
    def profit(self) -> int:
        return self._profit

    @profit.setter
    def profit(self, value: int):
        self._profit = value

    def __init__(self) -> None:
        self._signQty = 0
        self._matchQty = 0
        self._profit = 0
        pass

    def __eq__(self, other):
        if not isinstance(other, MatchInfo):
            return False
        return (self.signQty == other.signQty and
                self.matchQty == other.matchQty and
                self.profit == other.profit)

    def __hash__(self) -> int:
        return hash(self._signQty, self._matchQty, self._profit)


class FiveThreeNineMatch:
    def __init__(self, strategyMatch=StrategyMatch.TWO) -> None:
        self._cost = 25
        self._prize = 1500
        self._strategyMatch = strategyMatch
        pass

    def _two(self, inputs: List[str], sign: List[str]) -> bool:
        if sign is not None and inputs is not None and len(set(inputs + sign)) == 5:
            return True
        return False
        pass

    def match(self, inputs: List[str], sign2Ds: List[List[str]]) -> MatchInfo:
        """命中2球含以上就算成功"""
        matchInfo = MatchInfo()
        if len(sign2Ds) == 0:
            return matchInfo
        matchInfo.signQty = len(sign2Ds)
        for sign in sign2Ds:
            if self._strategyMatch == StrategyMatch.TWO and self._two(inputs, sign):
                matchInfo.matchQty += 1
        matchInfo.profit = (self._prize * matchInfo.matchQty) - \
            (self._cost * matchInfo.signQty)
        return matchInfo
        pass


class TestFiveThreeNineMatch(unittest.TestCase):
    # error 二合調整
    def test_match_by_two(self):
        # arrange
        fiveThreeNineMatch = FiveThreeNineMatch()
        # act

        input = ['01', '02', '03', '04', '05']
        sign2Ds = [['01', '02'], ['01', '12'], [
            '01', '05'], ['14', '15']]
        matchInfo = fiveThreeNineMatch.match(input, sign2Ds)
        matchInfoExcept = MatchInfo()
        matchInfoExcept.signQty = 4
        matchInfoExcept.matchQty = 2
        matchInfoExcept.profit = 2900
        # assert
        self.assertEqual(matchInfo, matchInfoExcept)
        pass


if __name__ == '__main__':

    try:
        suite = unittest.TestSuite()
        suite.addTest(TestFiveThreeNineMatch('test_match_by_two'))
        runner = unittest.TextTestRunner(verbosity=2)
        runner.run(suite)
    except SystemExit:
        pass

    pass
