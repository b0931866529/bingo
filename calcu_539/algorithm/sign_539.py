import itertools
import math
from typing import List
import numpy as np
import pandas as pd
from pandas import DataFrame, Series
from exclude import StateExclude
from db.db import MSSQLDbContext
from calcu_539.prize.prize_539 import FiveThreeNinePrize, FiveThreeNineMatch
from calcu_539.algorithm.calcu import DeferCalcu, TimesCalcu, ExportFile


class FiveThreeNineSign:
    """
    產出要簽注獎號策略:
    1.球號次數order asc
    2.球號濾離群值(參數設定離群值過濾與否)
    3.變異數在某個區間表示夠離散要回補(參數設定變異數過濾與否)
    4.冷門球號組數做乘積組合(用指數)
    """

    @property
    def includeColumns(self):
        return self._includeColumns

    @includeColumns.setter
    def includeColumns(self, value):
        self._includeColumns = value

    @ property
    def strategy(self):
        return self._strategy

    @ strategy.setter
    def strategy(self, value):
        self._strategy = value

    @ property
    def take(self):
        return self._take

    @ take.setter
    def take(self, value):
        self._take = value

    def __init__(self, exportFile: ExportFile, stateExclude: StateExclude, fiveThreeNineMatch: FiveThreeNineMatch, isToCsv=False, path=None, filename=None) -> None:
        self._exportFile = exportFile
        self._isToCsv = isToCsv
        self._hot_limit = 13
        """表示前幾組不簽注(因為數據不足)"""
        self._frtSkip = 10
        """取得球號次數前幾組"""
        self._take = 4
        self._path = path
        self._filename = filename
        self._includeColumns = []
        self._stateExclude = stateExclude
        self._fiveThreeNineMatch = fiveThreeNineMatch
        pass

    def _getState(self, row: pd.Series):
        return self._stateExclude.exclude(row)
        """hot簽注、cold不簽注，未來增加其他狀態判別方法"""
        if row['index'].tolist()[0] < self._frtSkip:
            return 'cold'
        # if row[('deferMark', 'varQ')] != 'Q2':
        #     return 'cold'
        # if np.isnan(row['varBef'].values[0]):
        #     return 'cold'
        # if row['varBef'].values[0] < 13.65:
        #     return 'cold'
        # if len(row['markOutlierBefs'][0]) < 2:
        #     return 'cold'
        return 'hot'
        pass

    def _compose2GroupBall2Ds(self, row: pd.Series):
        """將要簽注號碼組合成2號一組"""
        if row['state'].tolist()[0] == 'cold':
            return []

        # 生成两个元素为一组的组合
        excludeBalls = row['excludeBalls'].tolist()[0]
        tpCombinations = list(itertools.product(excludeBalls, repeat=2))
        combinations = [list(tp) for tp in tpCombinations]

        ball2DResults = []
        for arr in combinations:
            if any(len(set(arr + ele)) == 2 for ele in ball2DResults) == False and arr[0] != arr[1]:
                ball2DResults.append(arr)

        # 驗證是否有重複組合,若有print
        excepted = math.comb(len(excludeBalls), 2)
        if excepted != len(ball2DResults):
            print('有重複組合')

        return ball2DResults
        pass

    def _excludeOutlierAndVarQ(self, row: pd.Series, deferKeys: List[str]):
        if row['state'].tolist()[0] == 'cold' or row['state'].tolist()[0] == None:
            return []

        arr = row['times_asc'].tolist()[0]
        results = []
        for ele in arr:
            isExist = False
            for deferKey in deferKeys:
                for numOutliers in row[f'{deferKey}_numOutliers']:
                    if any(ele == num for num in numOutliers):
                        isExist = True
            if isExist == False:
                results.append(ele)
        return results[0:self._take]

    def _outlierMatch(self, row: pd.Series, skipTimesKey: str):
        sign2Ds = row[f'{skipTimesKey}_numOutliers'].tolist()[0]
        if sign2Ds == None or len(sign2Ds) == 0:
            return MatchInfo()
        inputs = row[('times', 'num')]
        matchInfo = self._fiveThreeNineMatch.match(inputs, sign2Ds)
        return matchInfo

    def _missQty(self, row: pd.Series, skipTimesKey: str):
        """離群值閃掉未命中數量"""
        matchInfo = self._outlierMatch(row, skipTimesKey)
        return matchInfo.signQty - matchInfo.matchQty
        pass

    def _notMissQty(self, row: pd.Series, skipTimesKey: str):
        """離群值無閃掉命中數量"""
        matchInfo = self._outlierMatch(row, skipTimesKey)
        return matchInfo.matchQty
        pass

    def sign(self, dfs: List[DataFrame], keys: List[str]) -> DataFrame:
        """拖期離散過濾多組,dfTimes保持一組在結尾"""
        dfSign = pd.concat(dfs, axis=1, keys=keys)
        dfSign.reset_index(inplace=True)
        # dfSign = pd.concat([dfDefer, dfTimes], axis=1, keys=['defer', 'times'])
        # ('defer', '零')
        # 判別期數若<10期直接輸出空array
        # 若>10期先判別標準差是高於10還是低於10,衍生欄位先呈現True、False
        # 後續再加上>10冷門求號 輸出4個
        # 後續再加上<10熱門求號 輸出4個

        # region 衍生欄位冷熱門球號、簽注分類、簽注球號計算方式
        # 判別是否簽注
        dfSign['state'] = dfSign.apply(lambda x: self._getState(x), axis=1)
        dfSign['state'] = dfSign['state'].shift(1)
        # 這二個欄位是用來判斷是否簽注
        skipTimesKeys = keys[:-1]

        for skipTimesKey in skipTimesKeys:
            dfSign[f'{skipTimesKey}_varQ'] = dfSign[(
                skipTimesKey, 'varQ')].shift(1)
            dfSign[f'{skipTimesKey}_numOutliers'] = dfSign[(
                skipTimesKey, 'numOutliers')].shift(1)
            dfSign[f'{skipTimesKey}_numOutliers_missQty'] = dfSign.apply(
                lambda row: self._missQty(row, skipTimesKey), axis=1)
            dfSign[f'{skipTimesKey}_numOutliers_notMissQty'] = dfSign.apply(
                lambda row: self._notMissQty(row, skipTimesKey), axis=1)
        # 計算離群閃避數量
        # 計算離群未閃避數量
        # 補充 閃避和未閃避衝突數量

        # loop會有多個拖期

        dfSign[f'{keys[-1]}_asc'] = dfSign[(keys[-1], 'asc')].shift(1)
        # # 過濾離散組合(且這邊設定take幾組)
        dfSign['excludeBalls'] = dfSign.apply(
            lambda row: self._excludeOutlierAndVarQ(row, skipTimesKeys), axis=1)

        # 最後運算出要簽牌組合
        dfSign['signBall2Ds'] = dfSign.apply(
            lambda row: self._compose2GroupBall2Ds(row), axis=1)

        # endregion

        dfSignInfo = DfInfo()
        dfSignInfo.df = dfSign
        if len(self.includeColumns) != 0:
            dropColumns = []
            for column in dfSign.columns:
                if any(column == includeColumn for includeColumn in self.includeColumns) == False:
                    dropColumns.append(column)
                pass
            dfDropTimes = dfSign.copy(deep=True)
            dfDropTimes.drop(columns=dropColumns, inplace=True)
            dfSignInfo.dfDrop = dfDropTimes

        if self._isToCsv and self._path is not None and self._filename is not None:
            self._exportFile.exportExcel(
                [dfSignInfo.df, dfSignInfo.dfDrop], ['df', 'dfDrop'], self._path, self._filename)
        return dfSignInfo
        pass


if __name__ == '__main__':

    # region db info
    dbContext = MSSQLDbContext({'server': 'wpdb2.hihosting.hinet.net', 'user': 'p89880749_p89880749',
                                'password': 'Jonny1070607!@#$%', 'database': 'p89880749_test'})
    rows = dbContext.select(
        'select drawNumberSize,lotteryDate from Daily539 ORDER BY period')
    inputs = list(map(lambda row: row['drawNumberSize'].split(','), rows))
    # endregion

    # region dfTimes、dfDefer
    # limits = [0.3, 0.5, 0.7, 0.9, 1.1, 1.3, 1.5]
    limits = [1.5]
    for limit in limits:
        exportFile = ExportFile()
        quantile = Quantile(QLevel=QLevel.Q10)
        quantile.cutFrt = 0
        quantile.cutEnd = 19
        quantile.upperLimit = limit
        # region 小一group
        convertMark = ConvertMark()
        deferSmallMarkCalcu = DeferCalcu(exportFile, convertMark, quantile)
        deferSmallMarkCalcu.includeColumns = ['numOutliers', 'varQ']
        dfDeferSmallMarkInfo = deferSmallMarkCalcu.calcu(inputs)
        # endregion

        # region 單一group
        convertOddEvenMark = ConvertOddEvenMark()
        deferOddMarkCalcu = DeferCalcu(
            exportFile, convertOddEvenMark, quantile)
        deferOddMarkCalcu.includeColumns = ['numOutliers', 'varQ']
        dfDeferOddMarkInfo = deferOddMarkCalcu.calcu(inputs)
        # endregion

        quantile.cutFrt = 0
        quantile.cutEnd = 39
        beginConvertMark = BeginConvertMark()
        deferBallCalcu = DeferCalcu(exportFile, beginConvertMark, quantile)
        deferBallCalcu.includeColumns = ['numOutliers', 'varQ']
        dfDeferBallInfo = deferBallCalcu.calcu(inputs)

        timesCalcu = TimesCalcu(exportFile, beginConvertMark, quantile)
        quantile.cutFrt = 0
        quantile.cutEnd = 39
        timesCalcu.includeColumns = ['num', 'asc']
        dfTimesInfo = timesCalcu.calcu(inputs)
        # endregion

        keys = ['deferSmallMark', 'deferOddMark', 'deferBall', 'times']
        dfs = [dfDeferSmallMarkInfo.dfDrop, dfDeferOddMarkInfo.dfDrop,
               dfDeferBallInfo.dfDrop, dfTimesInfo.dfDrop]

        """設定要排除條件"""
        def excludeState(row: pd.Series):
            if row['index'].tolist()[0] < 10:
                return True
            # if row[('deferMark', 'varQ')] != 'Q2':
            #     return True
            # if row[('deferBall', 'varQ')] != 'Q2':
            #     return True
            # if len(row[('deferBall', 'varQ')]) != 'Q2':
            #     return True
            return False

        for take in range(8, 9):
            pathSign = 'C:/Programs/bingo/bingo_scrapy/539_calcu'
            filenameSign = f'sign{take}_{limit}.xlsx'

            stateExclude = StateExclude(excludeState)
            fiveThreeNineMatch = FiveThreeNineMatch()
            fiveThreeNineSign = FiveThreeNineSign(
                exportFile, stateExclude, fiveThreeNineMatch, True, pathSign, filenameSign)
            fiveThreeNineSign.take = take
            fiveThreeNineSign._frtSkip = 50
            groupKeys = ['varQ', 'numOutliers',
                         'numOutliers_missQty', 'numOutliers_notMissQty']
            varQIncludeColumns = []
            numOutliersIncludeColumns = []
            numOutliersMissQtyIncludeColumns = []
            numOutliersNotMissQtyIncludeColumns = []

            for key in keys[:-1]:
                varQIncludeColumns.append((f'{key}_varQ', ''))
                numOutliersIncludeColumns.append((f'{key}_numOutliers', ''))
                numOutliersMissQtyIncludeColumns.append(
                    (f'{key}_numOutliers_missQty', ''))
                numOutliersNotMissQtyIncludeColumns.append(
                    (f'{key}_numOutliers_notMissQty', ''))

            fiveThreeNineSign.includeColumns = [
                ('times', 'num'), ('times', 'asc'), ('signBall2Ds', '')]
            fiveThreeNineSign.includeColumns.extend(varQIncludeColumns)
            fiveThreeNineSign.includeColumns.extend(numOutliersIncludeColumns)
            fiveThreeNineSign.includeColumns.extend(
                numOutliersMissQtyIncludeColumns)
            fiveThreeNineSign.includeColumns.extend(
                numOutliersNotMissQtyIncludeColumns)
            dfSignInfo = fiveThreeNineSign.sign(dfs, keys)

            pathPrize = 'C:/Programs/bingo/bingo_scrapy/539_calcu'
            filenamePrize = f'prize{take}_{limit}.xlsx'
            fiveThreeNineMatch = FiveThreeNineMatch()
            fiveThreeNinePrize = FiveThreeNinePrize(
                exportFile, fiveThreeNineMatch, True, pathPrize, filenamePrize)
            dfPrize = fiveThreeNinePrize.prize(
                dfSignInfo.dfDrop, varQIncludeColumns, numOutliersIncludeColumns)
    pass
