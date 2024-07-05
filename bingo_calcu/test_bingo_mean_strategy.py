from typing import List
import unittest
from typing import Callable
# strategy mean
# all put not buy
# all call buy
# 3 and 6 and 12 call buy
# feedback


class BingoParam:
    def __init__(self, star, num):
        self.star = star
        self.num = num

    # def __eq__(self, other):
    #     if not isinstance(other, NumMeanLineInfo):
    #         return False
    #     return self.num == other.num and self.mean == other.mean

    # def __hash__(self) -> int:
    #     return hash((self.num, self.mean))


class NumMeanLine:
    def __init__(self, num: str, mean: int) -> None:
        self.num = num
        self.mean = mean
        pass

    def __eq__(self, other):
        if not isinstance(other, NumMeanLine):
            return False
        return self.num == other.num and self.mean == other.mean

    def __hash__(self) -> int:
        return hash((self.num, self.mean))


class BingoInfo:
    def __init__(self):
        self._double: int = 1
        self._cost: int = 25
        self._amt: int = 0
        self._isDouble: bool = True
        self._nums: List[str] = []
        self._matchs: List[str] = []

    @property
    def double(self) -> int:
        return self._double

    @property
    def cost(self) -> int:
        return self._cost

    @double.setter
    def double(self, value: int):
        """設定是否加倍，連帶設定成本"""
        self._double = value
        self._cost = 25 * value

    @property
    def amt(self) -> int:
        """取得獎金"""
        return self._amt

    @amt.setter
    def amt(self, value: int):
        """設定獎金"""
        self._amt = value

    @property
    def nums(self) -> List[str]:
        """取得簽注球號"""
        return self._nums

    @nums.setter
    def nums(self, value: List[str]):
        """設定簽注球號"""
        self._nums = value

    @property
    def matchs(self) -> List[str]:
        """取得中獎球號"""
        return self._matchs

    @matchs.setter
    def matchs(self, value: List[str]):
        """設定中獎球號"""
        self._matchs = value

    @property
    def isDouble(self) -> bool:
        """取得台彩是否加倍"""
        return self._isDouble

    @isDouble.setter
    def isDouble(self, value: bool):
        """設定台彩是否加倍"""
        self._isDouble = value

    def __eq__(self, other):
        if not isinstance(other, BingoInfo):
            return False
        numSetQty = len(set(self.nums + other.nums))
        matchSetQty = len(set(self.matchs + other.matchs))
        isNumEqual = numSetQty == len(self.nums) and len(
            self.nums) == len(other.nums)
        isMatchEqual = matchSetQty == len(self.matchs) and len(
            self.matchs) == len(other.matchs)
        return (self.double == other.double and
                self.cost == other.cost and
                self.amt == other.amt and
                self.isDouble == other.isDouble and
                isNumEqual and isMatchEqual)

    def __hash__(self) -> int:
        return hash((self._double, self._cost, self._amt, self._isDouble, tuple(set(self._nums)), tuple(set(self._matchs))))


class NumMeanLineInfo:
    def __init__(self, mean: int, means: List[NumMeanLine]) -> None:
        self.mean = mean
        self.means = means
        pass


class BingoMeanStrategy:

    def __init__(self, meanBingo, logger) -> None:
        self._meanBingo = meanBingo
        self._logger = logger
        pass

    def calcu(self, inputs: List[BingoParam], filters: List[Callable[[], bool]]) -> List[BingoInfo]:
        """從參數中生成對應彩券(先將接口寫鬆)"""
        # filter 3、6、12、36 all call
        # filter 3、6、12 call
        # take main ball

        pass


class TestBingoMeanStrategy(unittest.TestCase):

    def test_calcu_put_not_buy_3(self):
        """
        # all call buy 2 num by 2 unit
        # 2連號最高機率
        # 3 and 6 and 12 call buy 2 num by 2 unit
        # 2連號拆開單一號碼去計算另一號碼
        # 3 and 6 and 12 call buy 1 num by 1 unit
        # compose 3 star 2 * 4 = 6 num

        # 2連號驗證order
        # 單一號碼驗證order
        # 組合驗證
        """
        pass

    # def test_calcu_put_not_buy_4(self):
    #     """
    #     # all call buy 3 num
    #     # 3 and 6 and 12 call buy 4 num
    #     # compose 4 star 4 num
    #     """
    #     pass


# test strategy filter and compose ball
# test feedback match amt DI prize and strategy
