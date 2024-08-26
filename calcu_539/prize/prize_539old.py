from typing import List
import numpy as np
import pandas as pd
from pandas import DataFrame, Series
from calcu_539.prize.match import FiveThreeNineMatch


class FiveThreeNinePrize:
    """檢驗簽注號碼是否命中,並統計當期簽注和命中數量、是否簽注和命中"""

    def __init__(self, match: FiveThreeNineMatch) -> None:
        self._match = match
        pass

    def _matchInfo(self, row: Series):
        inputs = row[('times', 'num')]
        sign2Ds = row['signBall2Ds'].tolist()[0]
        matchInfo = self._match.match(inputs, sign2Ds)
        return matchInfo
        pass

    def prize(self, dfSign: DataFrame) -> DataFrame:

        dfPrize = dfSign.copy(deep=True)

        dfPrize['matchInfo'] = dfSign.apply(
            lambda row: self._matchInfo(row), axis=1)
        dfPrize['matchQty'] = dfPrize['matchInfo'].apply(
            lambda row: row.matchQty)
        dfPrize['signQty'] = dfPrize['matchInfo'].apply(
            lambda row: row.signQty)
        dfPrize['profit'] = dfPrize['matchInfo'].apply(
            lambda row: row.profit)
        return dfPrize

    pass
