from matplotlib.pyplot import cla
import numpy as np
import pandas as pd
from pandas import DataFrame, Series
import unittest
from unittest.mock import Mock
from collections.abc import Callable


class StateExclude:

    def __init__(self, exlcudeFunc: Callable[[], bool]) -> None:
        self._exlcudeFunc = exlcudeFunc
        pass

    def exclude(self, row: pd.Series) -> str:
        if self._exlcudeFunc(row):
            return 'cold'

        return 'hot'
        pass
    pass


class TestStateExclude(unittest.TestCase):

    def test_exclude_Q4(self):
        row = pd.Series({'varQ': 'Q4', 'numOutliers': 10})

        def excludeFuncQ4(row):
            return row['varQ'] == 'Q4'
        stateExclude = StateExclude(excludeFuncQ4)

        state = stateExclude.exclude(row)
        excepted = 'cold'
        self.assertEqual(state, excepted)
        pass

    def test_not_exclude_Q3(self):
        row = pd.Series({'varQ': 'Q4', 'numOutliers': 10})

        def excludeFuncQ3(row):
            return row['varQ'] == 'Q3'
        stateExclude = StateExclude(excludeFuncQ3)

        state = stateExclude.exclude(row)
        excepted = 'hot'
        self.assertEqual(state, excepted)
        pass


if __name__ == '__main__':

    # region test case

    try:
        suite = unittest.TestSuite()
        suite.addTest(TestStateExclude('test_exclude_Q4'))
        suite.addTest(TestStateExclude('test_not_exclude_Q3'))
        runner = unittest.TextTestRunner(verbosity=2)
        runner.run(suite)
    except SystemExit:
        pass

    # endregion
