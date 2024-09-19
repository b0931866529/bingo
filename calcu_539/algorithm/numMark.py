from itertools import combinations
import unittest
from unittest.mock import Mock

# 2h


class NumMark:

    def __init__(self) -> None:
        self._balls = []
        pass

    def loadStds(self, allBallQty: int, composeQty: int) -> list[str]:
        """
        allBallQty: 總球數
        composeQty: 組合數
        list[str]:組數集合
        ex 1:
        allBallQty=3
        composeQty=1
        return ['01', '02', '03']
        ex 2:
        allBallQty=4
        composeQty=2
        return ['01_02','01_03','01_04','02_03','02_04','03_04']
        ex 3:
        allBallQty=4
        composeQty=3
        return ['01_02_03','01_02_04','02_03_04','01_03_04']
        ex 4:
        allBallQty=5
        composeQty=2
        return ['01_02','01_03','01_04','01_05','02_03','02_04','02_05','03_04','03_05','04_05']
        """
        self._balls = [f"{i:02}" for i in range(1, allBallQty + 1)]
        if composeQty == 1:
            return self._balls
        self._balls = ['_'.join(combo)
                       for combo in combinations(self._balls, composeQty)]
        return self._balls
        pass

    def ballToMarks(self, ball: str) -> list[str]:
        """
        將球號轉換為標記
        ex 2:
        allBallQty=4
        composeQty=2
        return ['01_02','01_03','01_04','02_03','02_04','03_04']
        """
        matches = [r for r in self._balls if r.find(ball) != -1]
        return matches
        pass

    def markToBalls(self, mark: str) -> list[str]:
        """
        將標記轉換為球號集合
        ex 2:
        allBallQty=4
        composeQty=2
        mark='01_02'
        return ['01','02']
        """
        return mark.split('_')
        pass

    pass

# 0.5h


class TestNumMark(unittest.TestCase):

    def test_loadStds_by_composeQty_1_allQty_3(self):
        """
        ex 1:
        allBallQty=3
        composeQty=1
        return ['01', '02', '03']
        """
        # arrange
        numMark = NumMark()
        # act
        actuals = numMark.loadStds(3, 1)
        # assert
        excepted = ['01', '02', '03']
        self.assertCountEqual(actuals, excepted)
        pass

    def test_loadStds_by_composeQty_2_allQty_4(self):
        """
        ex 2:
        allBallQty=4
        composeQty=2
        return ['01_02','01_03','01_04','02_03','02_04','03_04']
        """
        # arrange
        numMark = NumMark()
        # act
        actuals = numMark.loadStds(4, 2)
        # assert
        expected = ['01_02', '01_03', '01_04', '02_03', '02_04', '03_04']
        self.assertCountEqual(actuals, expected)
        pass

    def test_loadStds_by_composeQty_3_allQty_4(self):
        """
        ex 3:
        allBallQty=4
        composeQty=3
        return ['01_02_03','01_02_04','02_03_04','01_03_04']
        """
        # arrange
        numMark = NumMark()
        # act
        actuals = numMark.loadStds(4, 3)
        # assert
        expected = ['01_02_03', '01_02_04', '02_03_04', '01_03_04']
        self.assertCountEqual(actuals, expected)

    def test_loadStds_by_composeQty_2_allQty_5(self):
        """
        ex 4:
        allBallQty=5
        composeQty=2
        return ['01_02','01_03','01_04','01_05','02_03','02_04','02_05','03_04','03_05','04_05']
        """
        # arrange
        numMark = NumMark()
        # act
        actuals = numMark.loadStds(5, 2)
        # assert
        expected = ['01_02', '01_03', '01_04', '01_05', '02_03',
                    '02_04', '02_05', '03_04', '03_05', '04_05']
        self.assertCountEqual(actuals, expected)

    def test_ballToMarks_by_composeQty_1_allQty_3(self):
        """
        ex 1:
        allBallQty=3
        composeQty=1
        ball='01'
        return ['01', '02', '03']
        """
        # arrange
        numMark = NumMark()
        allBallQty = 3
        composeQty = 1
        numMark.loadStds(allBallQty, composeQty)
        # act
        ball = '01'
        actuals = numMark.ballToMarks(ball)
        # assert
        excepted = ['01']
        self.assertCountEqual(actuals, excepted)
        pass

    def test_ballToMarks_by_composeQty_2_allQty_4(self):
        """
        ex 2:
        allBallQty=4
        composeQty=2
        ball='01'
        return ['01_02','01_03','01_04']
        """
        # arrange
        numMark = NumMark()
        allBallQty = 4
        composeQty = 2
        numMark.loadStds(allBallQty, composeQty)
        # act
        ball = '01'
        actuals = numMark.ballToMarks(ball)
        # assert
        excepted = ['01_02', '01_03', '01_04']
        self.assertCountEqual(actuals, excepted)
        pass

    def test_ballToMarks_by_composeQty_3_allQty_4(self):
        """
        ex 3:
        allBallQty=4
        composeQty=3
        ball='01'
        return ['01_02_03','01_02_04','01_03_04']
        """
        # arrange
        numMark = NumMark()
        allBallQty = 4
        composeQty = 3
        numMark.loadStds(allBallQty, composeQty)
        # act
        ball = '01'
        actuals = numMark.ballToMarks(ball)
        # assert
        excepted = ['01_02_03', '01_02_04', '01_03_04']
        self.assertCountEqual(actuals, excepted)
        pass

    def test_ballToMarks_by_composeQty_2_allQty_5(self):
        """
        ex 4:
        allBallQty=5
        composeQty=2
        ball='01'
        return ['01_02','01_03','01_04','01_05']
        """
        # arrange
        numMark = NumMark()
        allBallQty = 5
        composeQty = 2
        numMark.loadStds(allBallQty, composeQty)
        # act
        ball = '01'
        actuals = numMark.ballToMarks(ball)
        # assert
        excepted = ['01_02', '01_03', '01_04', '01_05']
        self.assertCountEqual(actuals, excepted)
        pass

    def test_markToBalls_by_composeQty_1_allQty_3(self):
        """
        ex 1:
        allBallQty=3
        composeQty=1
        mark='01'
        return ['01']
        """
        # arrange
        numMark = NumMark()
        allBallQty = 3
        composeQty = 1
        numMark.loadStds(allBallQty, composeQty)
        # act
        mark = '01'
        actuals = numMark.markToBalls(mark)
        # assert
        excepted = ['01']
        self.assertCountEqual(actuals, excepted)
        pass

    def test_markToBalls_by_composeQty_2_allQty_4(self):
        """
        ex 2:
        allBallQty=4
        composeQty=2
        mark='01_02'
        return ['01','02']
        """
        # arrange
        numMark = NumMark()
        allBallQty = 4
        composeQty = 2
        numMark.loadStds(allBallQty, composeQty)
        # act
        mark = '01_02'
        actuals = numMark.markToBalls(mark)
        # assert
        excepted = ['01', '02']
        self.assertCountEqual(actuals, excepted)
        pass

    def test_markToBalls_by_composeQty_3_allQty_4(self):
        """
        ex 3:
        allBallQty=4
        composeQty=3
        mark='01_02_03'
        return ['01','02','03']
        """
        # arrange
        numMark = NumMark()
        allBallQty = 4
        composeQty = 3
        numMark.loadStds(allBallQty, composeQty)
        # act
        mark = '01_02_03'
        actuals = numMark.markToBalls(mark)
        # assert
        excepted = ['01', '02', '03']
        self.assertCountEqual(actuals, excepted)
        pass

    def test_markToBalls_by_composeQty_2_allQty_5(self):
        """
        ex 4:
        allBallQty=5
        composeQty=2
        mark='01_04'
        return ['01','04']
        """
        # arrange
        numMark = NumMark()
        allBallQty = 5
        composeQty = 2
        numMark.loadStds(allBallQty, composeQty)
        # act
        mark = '01_04'
        actuals = numMark.markToBalls(mark)
        # assert
        excepted = ['01', '04']
        self.assertCountEqual(actuals, excepted)
        pass
    pass


if __name__ == '__main__':
    # numMark = NumMark()
    # a = numMark.loadStds(3, 1)
    # b = numMark.loadStds(4, 2)
    # c = numMark.loadStds(4, 3)
    # print('')
    try:
        suite = unittest.TestSuite()
        suite.addTest(TestNumMark('test_loadStds_by_composeQty_1_allQty_3'))
        suite.addTest(TestNumMark('test_loadStds_by_composeQty_2_allQty_4'))
        suite.addTest(TestNumMark('test_loadStds_by_composeQty_3_allQty_4'))
        suite.addTest(TestNumMark('test_loadStds_by_composeQty_2_allQty_5'))
        suite.addTest(TestNumMark('test_ballToMarks_by_composeQty_1_allQty_3'))
        suite.addTest(TestNumMark('test_ballToMarks_by_composeQty_2_allQty_4'))
        suite.addTest(TestNumMark('test_ballToMarks_by_composeQty_3_allQty_4'))
        suite.addTest(TestNumMark('test_ballToMarks_by_composeQty_2_allQty_5'))
        suite.addTest(TestNumMark('test_markToBalls_by_composeQty_1_allQty_3'))
        suite.addTest(TestNumMark('test_markToBalls_by_composeQty_2_allQty_4'))
        suite.addTest(TestNumMark('test_markToBalls_by_composeQty_3_allQty_4'))
        suite.addTest(TestNumMark('test_markToBalls_by_composeQty_2_allQty_5'))
        runner = unittest.TextTestRunner(verbosity=2)
        runner.run(suite)
    except SystemExit:
        pass
    pass
