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


class BingoFeedback:

    def __init__(self, prize, meanBingo, db) -> None:
        self._meanBingo = meanBingo
        self._prize = prize
        self._db = db
        pass

    def calcu(self, feedTerm: int) -> List[BingoInfo]:
        """回朔策略和利潤"""
        pass


class TestBingoFeedback(unittest.TestCase):

    def test_action_feedTerm_3(self):
        """
        meanBingo 3,not match output strategy ,沒有產出
        prize 3
        db 3
        """
        pass

    def test_calcu_put_not_buy_4(self):
        """
        match profit
        """
        pass

    def test(self):
        """
        load all 50 term
        mean calcu 30 term
        5 term period
        loop
            31 stop
            32~34 call starategy and prize
            35 stop

        """
        pass

    def test_recent(self):
        """
        from calcu history 30
        mean calcu 30 term
        diff term
        5 term period
        loop
            31 stop
            32~34 call starategy and prize
            35 stop

        """
        pass

# test strategy filter and compose ball
# test feedback match amt DI prize and strategy


# test insert db 1 head 3 details,and check created time
# test check error tran db

# 原始資料
# |drawTerm|bigShowOrder|
# 表頭
# |drawTerm|algorithmName|amt|createdTime|
# 表身
# |drawTerm|nums|matches|double|amt|createdTime|
