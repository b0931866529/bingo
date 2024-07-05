from typing import List


class BallGroup:
    """
    球號分組資訊
    times單位可為拖期或次數
    """

    def __init__(self, sort: str, times: int):
        self._sort = sort
        self._times = times

    @property
    def sort(self) -> str:
        return self._sort

    @sort.setter
    def sort(self, value: str):
        self._sort = value

    @property
    def times(self) -> int:
        return self._times

    @times.setter
    def times(self, value: int):
        self._times = value

    pass


class BingoProfitInfo:
    """
    單期簽注資訊(內含有多期)
    """

    def __init__(self):
        """利潤"""
        self.amt: int = 0
        """期數"""
        self.drawTerm: int = 0
        """算法名稱"""
        self.algorithmName: str = ''
        """單注簽注"""
        self.bingoInfos: List[BingoInfo] = []

    def __eq__(self, other):
        if not isinstance(other, BingoProfitInfo):
            return False
        return self.amt == other.amt and self.drawTerm == other.drawTerm and self.algorithmName == other.algorithmName and set(self.bingoInfos) == set(other.bingoInfos)

    def __hash__(self) -> int:
        return hash((self.amt, self.drawTerm, self.algorithmName, tuple(set(self.bingoInfos))))


class BingoInfo:
    """
    單注簽注資訊
    """

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


class NumMeanLine:
    """
    球號均線
    """

    def __init__(self, nums: List[str], mean: int) -> None:
        """
        球號可能為組合(因此型別用List)
        """
        self.nums = nums
        """
        平均次數
        """
        self.mean = mean
        pass

    def __eq__(self, other):
        if not isinstance(other, NumMeanLine):
            return False
        return set(self.nums) == set(other.nums) and self.mean == other.mean

    def __hash__(self) -> int:
        return hash((tuple(set(self.nums)), self.mean))


class NumMeanInfo:
    """
    均日,均線資訊陣列
    """

    def __init__(self, meanLines: List[NumMeanLine], mean: int) -> None:
        self.meanLines = meanLines
        self.mean = mean
        pass

    def __eq__(self, other):
        if not isinstance(other, NumMeanInfo):
            return False
        return set(self.meanLines) == set(other.meanLines) and self.mean == other.mean

    def __hash__(self) -> int:
        return hash((tuple(set(self.meanLines)), self.mean))
