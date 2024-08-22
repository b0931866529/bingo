import unittest
from unittest.mock import Mock
from typing import List
# region 計算皮爾森相關係數 example
# import numpy as np
# x = [1, 2, 3, 4, 5]
# y = [2, 4, 6, 8, 10]
# correlation_matrix = np.corrcoef(x, y)
# pearson_correlation = correlation_matrix[0, 1]
# print(f"Pearson Correlation Coefficient: {pearson_correlation}")
# endregion


class CorrelationStatic:
    def __init__(self, path: str) -> None:
        """
        參數設定要載入json的路徑

        """
        self._path = path
        pass

    def calcu(self) -> float:
        """
        讀取json檔案
        將其insert mongodb
        query mongodb 弄成型態2個array係數
        計算皮爾森相關係數
        """
        pass


class TestCorrelationStatic(unittest.TestCase):
    """
    json檔案example
    裡面有3個欄位:period、profit、matchPercent
    group by period mean profit
    period group by key array
    profit mean array
    """
    pass


if __name__ == '__main__':
    # 以下是單元測試
    # try:
    #     suite = unittest.TestSuite()
    #     suite.addTest(TestCorrelationStatic(''))
    #     runner = unittest.TextTestRunner(verbosity=2)
    #     runner.run(suite)
    # except SystemExit:
    #     pass
