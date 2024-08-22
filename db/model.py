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
        return self.amt == other.amt and set(self.bingoInfos) == set(other.bingoInfos)

    def __hash__(self) -> int:
        return hash((self.amt, tuple(set(self.bingoInfos))))


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


class MapBingoProfitInfoToDb:
    def __init__(self, dbContext: MSSQLDbContext):
        self._dbContext = dbContext
        pass

    def insert(self, bingoProfitInfos: List[BingoProfitInfo]) -> str:
        """回朔運算結果轉成表頭和表身塞入資料庫,retrun 是否err"""
        pass

    def select(self, sql: str) -> List[BingoProfitInfo]:
        """資料庫回朔運算結果轉成結構,錯誤retrun 空列表"""
        pass


class TestMapBingoProfitInfoToDb:
    def __init__(self) -> None:
        self._dbContext = MSSQLDbContext({'server': 'wpdb2.hihosting.hinet.net', 'user': 'p89880749_p89880749',
                                          'password': 'Jonny1070607!@#$%', 'database': 'p89880749_test'})
        self._target = MapBingoProfitInfoToDb(self._dbContext)
        self._lists = [BingoProfitInfo(), BingoProfitInfo()]
        pass

    def test_insert_3head_9detail(self):
        """
        回朔資料連續3期,每期有3筆資料,驗證是否正常塞入資料庫
        """

        # arrange
        # act
        # assert
        pass

    def test_insert_exception(self):
        """
        明細內含有錯誤資料,驗證交易是否正常作動沒有將資料塞入資料庫
        """
        pass

    def test_select_3head_9detail(self):
        """
        資料庫回朔資料連續3期,每期有3筆資料,驗證撈取後是否轉成正確結構
        """
        pass

    def test_select_exception(self):
        """
        撈取SQL有錯誤,驗證是否無丟exception並且return空列表
        """
        pass
