from typing import List
import numpy as np
import pandas as pd
from pandas import DataFrame, Series
from calcu_539.algorithm.calcu import ExportFile
from calcu_539.prize.match import FiveThreeNineMatch


class FiveThreeNinePrize:
    """檢驗簽注號碼是否命中,並統計當期簽注和命中數量、是否簽注和命中"""

    def __init__(self, exportFile: ExportFile, match: FiveThreeNineMatch, isToCsv=False, path=None, filename=None) -> None:
        self._exportFile = exportFile
        self._isToCsv = isToCsv
        self._match = match
        self._path = path
        self._filename = filename
        pass

    def _matchInfo(self, row: Series):
        inputs = row[('times', 'num')]
        sign2Ds = row['signBall2Ds'].tolist()[0]
        matchInfo = self._match.match(inputs, sign2Ds)
        return matchInfo
        pass

    def _getParameter(self, dfPrize: DataFrame):
        signTerm = len(
            list(filter(lambda e: e != 0, dfPrize['signQty'].values)))
        matchTerm = len(
            list(filter(lambda e: e != 0, dfPrize['matchQty'].values)))
        termPercent = 0 if signTerm == 0 else matchTerm / signTerm
        termFormatedPercent = '{:.2%}'.format(termPercent)
        matchSumQty = dfPrize['matchQty'].sum()
        signSumQty = dfPrize['signQty'].sum()
        matchPercent = matchSumQty / signSumQty
        formatedPercent = '{:.2%}'.format(matchPercent)
        profits = list(map(lambda e: e.profit, dfPrize['matchInfo'].values))
        profit = np.array(profits).sum()
        cost = 25 * signSumQty
        dfParameter = pd.DataFrame(
            {'總損益': [profit], '成本': [cost], '期數命中率': [termFormatedPercent], '注數命中率': [formatedPercent]
             })
        return dfParameter
        pass

    def prize(self, dfSign: DataFrame, varQColumns: List[str], numOutliersColumns: List[str]) -> DataFrame:

        dfPrize = dfSign.copy(deep=True)

        dfPrize['matchInfo'] = dfSign.apply(
            lambda row: self._matchInfo(row), axis=1)
        dfPrize['matchQty'] = dfPrize['matchInfo'].apply(
            lambda row: row.matchQty)
        dfPrize['signQty'] = dfPrize['matchInfo'].apply(
            lambda row: row.signQty)
        dfPrize['profit'] = dfPrize['matchInfo'].apply(
            lambda row: row.profit)

        profitVar2Ds = []
        for varQColumn in varQColumns:
            colVar = dfPrize.groupby(varQColumn).groups.keys()
            profitVar = dfPrize.groupby(varQColumn)[
                'profit'].sum().tolist()
            profitVar2Ds.append(profitVar)
        dfVar = pd.DataFrame(profitVar2Ds, columns=colVar, index=varQColumns)
        # region 離散組數數量利潤計算
        numOutlier2Ds = []
        colNumOutlier2Ds = []
        for numOutliersColumn in numOutliersColumns:
            name = str(numOutliersColumn).split("'")[1] + '_Qty'
            dfPrize[name] = dfPrize[numOutliersColumn].apply(
                lambda row: 0 if row == None else len(row))
            colNumOutliers = dfPrize.groupby(name).groups.keys()
            colNumOutlier2Ds.append(colNumOutliers)
            profitNumOutliers = dfPrize.groupby(name)[
                'profit'].sum().tolist()
            print(name)
            print(profitNumOutliers)
            numOutlier2Ds.append(profitNumOutliers)
        colNumOutlier2Ds = sorted(
            colNumOutlier2Ds, key=len, reverse=True)
        dfOutlier = pd.DataFrame(
            numOutlier2Ds, columns=colNumOutlier2Ds[0], index=numOutliersColumns)
        dfOutlier.fillna(0, inplace=True)
        # endregion

        miss2Ds = []
        misses = []
        # 和標準值計算二者之間是否閃避、未閃避數量
        for numOutliersColumn in numOutliersColumns:
            nameMissQty = str(numOutliersColumn).split("'")[1] + '_missQty'
            nameNotMissQty = str(numOutliersColumn).split("'")[
                1] + '_notMissQty'
            missQty = dfPrize[nameMissQty].sum()
            notMissQty = dfPrize[nameNotMissQty].sum()
            allQty = missQty + notMissQty
            percentMiss = missQty / allQty
            misses.append(percentMiss)
            pass
        miss2Ds.append(misses)
        dfMiss = pd.DataFrame(
            miss2Ds, columns=numOutliersColumns)
        dfParameter = self._getParameter(dfPrize)
        if self._isToCsv and self._path is not None and self._filename is not None:
            self._exportFile.exportExcel(
                [dfPrize, dfParameter, dfVar, dfOutlier, dfMiss], ['dfPrize', 'dfParameter', 'dfVar', 'dfOutlier', 'dfMiss'], self._path, self._filename)
        return dfPrize

    pass
