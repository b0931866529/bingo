import unittest
from unittest.mock import Mock


class NumMark:

    def __init__(self) -> None:
        pass

    def loadStds(self, allBallQty: int, composeQty: int) -> list[str]:
        """
        allBallQty: 總球數
        composeQty: 組合數
        格式ex: 01_02_03:['01','02','03']
        """
        pass

    def ballToMark(self, ball: str) -> str:
        """
        將球號轉換為標記
        """
        pass

    def markToBalls(self, mark: str) -> list[str]:
        """
        將標記轉換為球號集合
        """
        pass

    pass


class TestNumMark(unittest.TestCase):

    # # 驗證是否有重複組合,若有print
    # excepted = math.comb(len(excludeBalls), 2)
    # if excepted != len(ball2DResults):
    #     print('有重複組合')

    def test_ballToMark_by_composeQty_3_allQty_4(self):
        """
        總球數: 4
        組合數: 3
        測試轉換球號為標記是否正確
        """
        pass

    def test_markToBalls_by_composeQty_3_allQty_4(self):
        """
        總球數: 4
        組合數: 3
        測試轉換標記為球號集合是否正確
        """
        pass

    def test_ballToMark_by_composeQty_2_allQty_4(self):
        """
        總球數: 4
        組合數: 2
        測試轉換球號為標記是否正確
        """
        pass

    def test_markToBalls_by_composeQty_2_allQty_4(self):
        """
        總球數: 4
        組合數: 2
        測試轉換標記為球號集合是否正確
        """
        pass

    pass


if __name__ == '__main__':
    try:
        suite = unittest.TestSuite()
        suite.addTest(TestNumMark('test_ballToMark_by_composeQty_3_allQty_4'))
        suite.addTest(TestNumMark('test_ballToMark_by_composeQty_3_allQty_4'))
        suite.addTest(TestNumMark('test_ballToMark_by_composeQty_2_allQty_4'))
        suite.addTest(TestNumMark('test_ballToMark_by_composeQty_2_allQty_4'))
        runner = unittest.TextTestRunner(verbosity=2)
        runner.run(suite)
    except SystemExit:
        pass
    pass
