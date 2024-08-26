from enum import Enum
import unittest
import numpy as np
from pandas import DataFrame, Series


class QLevel(Enum):
    Q4 = 'Q4'
    Q10 = 'Q10'


class Quantile:

    @property
    def lowerLimit(self):
        return self._lowerLimit

    @lowerLimit.setter
    def lowerLimit(self, value):
        self._lowerLimit = value

    @property
    def upperLimit(self):
        return self._upperLimit

    @upperLimit.setter
    def upperLimit(self, value):
        self._upperLimit = value

    @property
    def cutFrt(self):
        return self._cutFrt

    @cutFrt.setter
    def cutFrt(self, value):
        self._cutFrt = value

    @property
    def cutEnd(self):
        return self._cutEnd

    @cutEnd.setter
    def cutEnd(self, value):
        self._cutEnd = value

    def __init__(self, QLevel: QLevel) -> None:
        self._lowerLimit = 1.5
        self._upperLimit = 1.5
        self._Q1 = 0
        self._Q2 = 0
        self._Q3 = 0
        self._Q4 = 0
        self._Q5 = 0
        self._Q6 = 0
        self._Q7 = 0
        self._Q8 = 0
        self._Q9 = 0
        self._Q10 = 0
        self._QLevel = QLevel
        pass

    def _loadQInfo_Q4(self, row):
        arr = row.values.tolist()
        arrAsc = sorted(arr, key=lambda e: e)
        npArr = np.array(arrAsc)
        self._Q1 = np.quantile(npArr, 0.25)
        self._Q2 = np.quantile(npArr, 0.5)
        self._Q3 = np.quantile(npArr, 0.75)

    def _loadQInfo_Q10(self, row):
        arr = row.values.tolist()
        arrAsc = sorted(arr, key=lambda e: e)
        npArr = np.array(arrAsc)
        self._Q1 = np.quantile(npArr, 0.1)
        self._Q2 = np.quantile(npArr, 0.2)
        self._Q3 = np.quantile(npArr, 0.3)
        self._Q4 = np.quantile(npArr, 0.4)
        self._Q5 = np.quantile(npArr, 0.5)
        self._Q6 = np.quantile(npArr, 0.6)
        self._Q7 = np.quantile(npArr, 0.7)
        self._Q8 = np.quantile(npArr, 0.8)
        self._Q9 = np.quantile(npArr, 0.9)

    def loadQInfo(self, row: Series):
        if self._QLevel == QLevel.Q4:
            self._loadQInfo_Q4(row)
        elif self._QLevel == QLevel.Q10:
            self._loadQInfo_Q10(row)
            pass
        pass

    def _calcuLevelQs_Q4(self, row: Series, colName: str) -> Series:
        """衍生欄位輸出四分位距Q1、Q2、Q3、Q4"""

        if np.isnan(row[colName]):
            return 'Q1'

        if row[colName] < self._Q1:
            return 'Q1'
        elif row[colName] >= self._Q1 and row[colName] < self._Q2:
            return 'Q2'
        elif row[colName] >= self._Q2 and row[colName] < self._Q3:
            return 'Q3'
        elif row[colName] > self._Q3:
            return 'Q4'
        pass

    def _calcuLevelQs_Q10(self, row: Series, colName: str) -> Series:
        """衍生欄位輸出四分位距Q1、Q2、Q3、Q4"""

        if np.isnan(row[colName]):
            return 'Q1'

        if row[colName] < self._Q1:
            return 'Q1'
        elif row[colName] >= self._Q1 and row[colName] < self._Q2:
            return 'Q2'
        elif row[colName] >= self._Q2 and row[colName] < self._Q3:
            return 'Q3'
        elif row[colName] >= self._Q3 and row[colName] < self._Q4:
            return 'Q4'
        elif row[colName] >= self._Q4 and row[colName] < self._Q5:
            return 'Q5'
        elif row[colName] >= self._Q5 and row[colName] < self._Q6:
            return 'Q6'
        elif row[colName] >= self._Q6 and row[colName] < self._Q7:
            return 'Q7'
        elif row[colName] >= self._Q7 and row[colName] < self._Q8:
            return 'Q8'
        elif row[colName] >= self._Q8 and row[colName] < self._Q9:
            return 'Q9'
        elif row[colName] > self._Q9:
            return 'Q10'
        pass

    def calcuLevelQs(self, row: Series, colName: str) -> Series:
        """衍生欄位輸出四分位距Q1、Q2、Q3、Q4"""
        if self._QLevel == QLevel.Q4:
            return self._calcuLevelQs_Q4(row, colName)
        elif self._QLevel == QLevel.Q10:
            return self._calcuLevelQs_Q10(row, colName)
            pass

    def calcuOutlierInfo(self, df: DataFrame) -> dict:
        """字典輸出離群值lower、upper(只能計算Q4離群)"""
        arr = []
        ballDeferColumns = df.columns[self._cutFrt:self._cutEnd]
        for column in ballDeferColumns:
            arr.extend(df[column].values)
            pass
        arr = sorted(arr, key=lambda e: e)
        npArr = np.array(arr)
        Q1 = np.quantile(npArr, 0.25)
        Q3 = np.quantile(npArr, 0.75)
        IQR = Q3 - Q1

        # 設定離散值範圍
        # lower_bound ABS 連續6次0(或者1次也允許)
        # 離散值程度1.5可做調整
        lower = Q1 - self._lowerLimit * IQR
        lower = abs(lower)
        upper = Q3 + self._upperLimit * IQR
        return {'lower': lower, 'upper': upper}
        pass

    pass


class TestQuantile(unittest.TestCase):
    def test_calcuOutlierInfo_Q4(self):
        # arrange
        quantile = Quantile(QLevel.Q4)
        quantile.cutFrt = 0
        quantile.cutEnd = 2

        data = {'A': [1, 2, 3, 4, 5], 'B': [1, 2, 3, 4, 5]}
        df = DataFrame(data)
        # act
        quantileInfo = quantile.calcuOutlierInfo(df)
        excepted = {'lower': 1, 'upper': 7}
        # assert
        self.assertDictEqual(quantileInfo, excepted)
        pass

    def test_calcuLevelQs_Q4(self):
        # arrange
        quantile = Quantile(QLevel.Q4)
        data = {'A': [1, 2, 3], 'B': [1, 2, 3]}
        df = DataFrame(data)
        # act
        quantile.loadQInfo(df['A'])
        df['level'] = df.apply(
            lambda row: quantile.calcuLevelQs(row, 'A'), axis=1)
        excepted = ['Q1', 'Q3', 'Q4']
        # assert
        self.assertCountEqual(df['level'].tolist(), excepted)
        pass

    def test_calcuLevelQs_Q10(self):
        # arrange
        quantile = Quantile(QLevel.Q10)
        data = {'A': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]}
        df = DataFrame(data)
        # act
        quantile.loadQInfo(df['A'])
        df['level'] = df.apply(
            lambda row: quantile.calcuLevelQs(row, 'A'), axis=1)
        excepted = ['Q1', 'Q2', 'Q3', 'Q4',
                    'Q5', 'Q6', 'Q7', 'Q8', 'Q9', 'Q10']
        # assert
        self.assertCountEqual(df['level'].tolist(), excepted)
        pass


if __name__ == '__main__':
    try:
        suite = unittest.TestSuite()
        suite.addTest(TestQuantile('test_calcuOutlierInfo_Q4'))
        suite.addTest(TestQuantile('test_calcuLevelQs_Q4'))
        suite.addTest(TestQuantile('test_calcuLevelQs_Q10'))
        runner = unittest.TextTestRunner(verbosity=2)
        runner.run(suite)
    except SystemExit:
        pass
