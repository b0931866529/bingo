from calcu_539.prize.match import FiveThreeNineMatch, MatchInfo
from db.db import MSSQLDbContext
import sys
import unittest
from unittest.mock import Mock
import pandas as pd


class FeedBack539:
    """
    """

    def __init__(self, period: int, times: int, dbContext: MSSQLDbContext, fiveThreeNineMatch: FiveThreeNineMatch) -> None:
        """
        設定參數:period測試期間,times測試次數,注入和取得資料庫溝通的物件,注入計算539是否中獎物件
        """
        self._period = period
        self._times = times
        self._dbContext = dbContext
        self._fiveThreeNineMatch = fiveThreeNineMatch
        pass

    def calcu(self) -> pd.DataFrame:
        """
        大致流程:
        先從db將539資料給取出來
        loop times測試次數
        開頭期數用random (要做防呆,開頭期數+測試期間,不能超出總期數否則重新random)
        用開頭期數+測試區間取出要測試期數
        sign 簽注號碼暫時先寫死留接口 每期2維array,內有2 array 1~39亂數 [['01','02','03','04','05'],['11','12','13','14','15']]
        用簽注號碼和取出期數用現有期數去計算獲利FiveThreeNineMatch物件可計算結果
        return DataColumn 期數:List[str],簽注號碼:List[List[str]],計算結果:MatchInfo,profit:int
        """
        pass
    pass


class TestFiveThreeNineMatch(unittest.TestCase):
    """
    此處先不管它,後續有時間再補上單元測試
    """
    pass


if __name__ == '__main__':

    # 怎麼調用FeedBack539寫在這example

    # 以下是單元測試
    # try:
    #     suite = unittest.TestSuite()
    #     suite.addTest(TestFiveThreeNineMatch('test_match'))
    #     runner = unittest.TextTestRunner(verbosity=2)
    #     runner.run(suite)
    # except SystemExit:
    #     pass

    pass
