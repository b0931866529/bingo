from typing import List
import unittest
from unittest.mock import Mock
from mlxtend.preprocessing import TransactionEncoder
import pandas as pd
from bingoModel import NumMeanInfo, NumMeanLine


class MeanBingo:

    @property
    def compose(self) -> int:
        return self._compose

    @compose.setter
    def compose(self, value: int):
        self._compose = value

    def __init__(self, dbContext) -> None:
        self.dbContext = dbContext
        self.arr2Ds = []
        self._compose = 1
        pass

    def loadSource(self, sql: str):
        # load 2D arrays
        dbResult = self.dbContext.select(sql)
        self.arr2Ds = list(
            map(lambda x: x['bigShowOrder'].split(','), dbResult))

    def calcu(self, days: List[int]) -> List[List[NumMeanLine]]:
        try:
            # one-hot
            te = TransactionEncoder()
            te_ary = te.fit(self.arr2Ds).transform(self.arr2Ds)
            dfOneHot = pd.DataFrame(te_ary, columns=te.columns_)
            # one-hot bool to number,好讓其能計算mean
            dfTimes = dfOneHot.applymap(lambda x: 1 if x else 0)
            result2Ds = []
            if len(dfTimes) < days[-1]:
                return NumMeanInfo([], 0)
            for day in days:
                dfMean = dfTimes.head(day).mean()
                results: List[NumMeanLine] = []
                for index, value in dfMean.items():
                    numDigit2 = round(value, 2)
                    nums = [index]
                    results.append(NumMeanLine(nums, numDigit2))
                resultInfo = NumMeanInfo(results, day)
                result2Ds.append(resultInfo)
        except:
            return NumMeanInfo([], 0)
        return result2Ds
        pass
# 3
# 6
# 12
# 36
# pass TDD


class TestMeanBingo(unittest.TestCase):
    def test_calcu_over_source(self):
        """
        calcu over source
        總共5期,傳入[3,6]參數
        """
        # self.fail("This test has not been developed yet.")
        # arrange
        mockDbContext = Mock()
        mockDbContext.select.return_value = [
            {'bigShowOrder': "01,02,03,04,05,06,07,08,09,10,11,12,13,14,15,16,17,18,19,20"},
            {'bigShowOrder': "01,02,03,04,05,06,07,08,09,10,11,12,13,14,15,16,17,18,19,21"},
            {'bigShowOrder': "01,02,03,04,05,06,07,08,09,10,11,12,13,14,15,16,17,18,19,79"},
            {'bigShowOrder': "01,02,03,04,05,06,07,08,09,10,11,12,13,14,15,16,17,18,19,80"},
            {'bigShowOrder': "01,02,03,04,05,06,07,08,09,10,11,12,13,14,15,16,17,18,21,22"}]
        meanBingo = MeanBingo(mockDbContext)
        meanBingo.loadSource('select sql...')
        # act
        inputs = [3, 6]
        actual = meanBingo.calcu(inputs)
        # assert
        excepted = NumMeanInfo([], 0)
        self.assertEqual(actual, excepted)
        pass

    def test_calcu_3mean(self):
        """
        calcu 3 mean
        01~18 mean 1
        19、21 mean 0.67
        20、22 mean 0.33
        """
        # self.fail("This test has not been developed yet.")
        # arrange
        # # DI DbContext
        mockDbContext = Mock()
        mockDbContext.select.return_value = [
            {'bigShowOrder': "01,02,03,04,05,06,07,08,09,10,11,12,13,14,15,16,17,18,19,20"},
            {'bigShowOrder': "01,02,03,04,05,06,07,08,09,10,11,12,13,14,15,16,17,18,19,21"},
            {'bigShowOrder': "01,02,03,04,05,06,07,08,09,10,11,12,13,14,15,16,17,18,21,22"}]
        meanBingo = MeanBingo(mockDbContext)
        meanBingo.loadSource('select sql...')
        # act
        inputs = [3]
        actual = meanBingo.calcu(inputs)
        # assert
        arr = [NumMeanLine(['01'], 1), NumMeanLine(['02'], 1), NumMeanLine(['03'], 1), NumMeanLine(['04'], 1), NumMeanLine(['05'], 1),
               NumMeanLine(['06'], 1), NumMeanLine(['07'], 1), NumMeanLine(
                   ['08'], 1), NumMeanLine(['09'], 1), NumMeanLine(['10'], 1),
               NumMeanLine(['11'], 1), NumMeanLine(['12'], 1), NumMeanLine(
                   ['13'], 1), NumMeanLine(['14'], 1), NumMeanLine(['15'], 1),
               NumMeanLine(['16'], 1), NumMeanLine(['17'], 1), NumMeanLine(
                   ['18'], 1), NumMeanLine(['19'], 0.67), NumMeanLine(['20'], 0.33),
               NumMeanLine(['21'], 0.67), NumMeanLine(['22'], 0.33)]
        excepted = [NumMeanInfo(arr, 3)]
        self.assertEqual(actual, excepted)
        pass

    def test_obj_call_demo(self):
        """
        object call demo
        """
        # arrange
        mockDbContext = Mock()
        mockDbContext.select.return_value = [
            {'bigShowOrder': "01,02,03,04,05,06,07,08,09,10,11,12,13,14,15,16,17,18,19,20"},
            {'bigShowOrder': "01,02,03,04,05,06,07,08,09,10,11,12,13,14,15,16,17,18,19,21"},
            {'bigShowOrder': "01,02,03,04,05,06,07,08,09,10,11,12,13,14,15,16,17,18,21,22"}]
        meanBingo = MeanBingo(mockDbContext)
        meanBingo.loadSource('select sql...')
        # act
        inputs = [3]
        actual = meanBingo.calcu(inputs)
        # assert
        self.assertEqual(1, mockDbContext.select.call_count)
        pass

    def test_calcu_3mean_by_2unit(self):
        """
        calcu mean
        """
        # arrange
        mockDbContext = Mock()
        mockDbContext.select.return_value = [
            {'bigShowOrder': "01,02,03"},
            {'bigShowOrder': "01,02,04"},
            {'bigShowOrder': "01,02,03"}]
        meanBingo = MeanBingo(mockDbContext)
        meanBingo.loadSource('select sql...')
        meanBingo.compose = 2
        # act
        days = [3]
        actual = meanBingo.calcu(days)
        # assert
        arr = [
            NumMeanLine(['01', '02'], 1), NumMeanLine(
                ['01', '03'], 0.67), NumMeanLine(['01', '04'], 0.33),
            NumMeanLine(['02', '03'], 0.67), NumMeanLine(['02', '04'], 0.33),
            NumMeanLine(['03', '04'], 0)
        ]
        excepted = NumMeanInfo(arr, 3)
        self.assertEqual(actual, excepted)
        # numbers = [1, 2, 3, 4, 5]
        # # Generate all 2-number combinations
        # combinations = list(itertools.combinations(numbers, 2))
        # print(combinations)
        # [(1, 2), (1, 3), (1, 4), (1, 5), (2, 3), (2, 4), (2, 5), (3, 4), (3, 5), (4, 5)]
        pass

    def test_calcu_3mean_by_3unit(self):
        self.fail("This test has not been developed yet.")
        pass

    def test_NumLine(self):
        # arrange
        actual = NumMeanLine(['79', '01'], 1.0)
        actualInfo = NumMeanInfo([actual], 1)
        excepted = NumMeanLine(['01', '79'], 1)
        exceptedInfo = NumMeanInfo([excepted], 1)

        # act

        # assert
        self.assertEqual(actualInfo, exceptedInfo)
        pass


if __name__ == '__main__':
    try:
        suite = unittest.TestSuite()
        suite.addTest(TestMeanBingo('test_NumLine'))
        suite.addTest(TestMeanBingo('test_calcu_over_source'))
        suite.addTest(TestMeanBingo('test_calcu_3mean'))
        # suite.addTest(TestMeanBingo('test_calcu_3mean_by_2unit'))
        runner = unittest.TextTestRunner(verbosity=2)
        runner.run(suite)
    except SystemExit:
        pass

# if __name__ == '__main__':
#     try:
#         unittest.main(verbosity=2)
#     except SystemExit:
#         pass
