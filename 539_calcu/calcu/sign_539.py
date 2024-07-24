import itertools
import math
from typing import List
import numpy as np
import pandas as pd
from pandas import DataFrame, Series
from calcu import ExportFile, DeferCalcu, TimesCalcu, ConvertMark, Quantile, BeginConvertMark, DfInfo
import db
from match import FiveThreeNineMatch, MatchInfo


class FiveThreeNinePrize:
    """檢驗簽注號碼是否命中,並統計當期簽注和命中數量、是否簽注和命中"""

    def __init__(self, exportFile: ExportFile, match: FiveThreeNineMatch, isToCsv=False, path=None, filename=None) -> None:
        self._exportFile = exportFile
        self._isToCsv = isToCsv
        self._match = match
        self._path = path
        self._filename = filename
        pass

    def _matchQty(self, row: Series):
        inputs = row[('times', 'num')]
        sign2Ds = row['signBall2Ds'].tolist()[0]
        matchInfo = self._match.match(inputs, sign2Ds)
        return matchInfo.matchQty
        pass

    def prize(self, dfSign: DataFrame) -> DataFrame:

        dfPrize = dfSign.copy(deep=True)
        dfPrize['matchQty'] = dfSign.apply(
            lambda row: self._matchQty(row), axis=1)
        if self._isToCsv and self._path is not None and self._filename is not None:
            self._exportFile.exportExcel(
                [dfPrize], ['dfPrize'], self._path, self._filename)
        return dfPrize

    pass


class FiveThreeNineSign:
    """
    產出要簽注獎號策略:
    1.球號次數order desc
    2.球號濾離群值(參數設定離群值過濾與否)
    3.變異數在某個區間表示夠離散要回補(參數設定變異數過濾與否)
    4.冷門球號組數做乘積組合(用指數)
    """
    @property
    def strategy(self):
        return self._strategy

    @strategy.setter
    def strategy(self, value):
        self._strategy = value

    @property
    def take(self):
        return self._take

    @take.setter
    def take(self, value):
        self._take = value

    def __init__(self, exportFile: ExportFile, isToCsv=False, path=None, filename=None) -> None:
        self._exportFile = exportFile
        self._isToCsv = isToCsv
        self._hot_limit = 13
        """表示前幾組不簽注(因為數據不足)"""
        self._frtSkip = 10
        """取得球號次數前幾組"""
        self._take = 4
        self._path = path
        self._filename = filename
        pass

    def _getState(self, row: pd.Series):
        """hot簽注、cold不簽注，未來增加其他狀態判別方法"""
        if row['index'].tolist()[0] > self._frtSkip:
            return 'hot'
        return 'cold'
        if np.isnan(row['varBef'].values[0]):
            return 'cold'
        if row['varBef'].values[0] < 13.65:
            return 'cold'
        if len(row['markOutlierBefs'][0]) < 2:
            return 'cold'
        return 'hot'
        pass

    def _excludeOutlier(self, row: pd.Series):
        """排除離群值,並且設定取得前幾組"""
        if row['state'] == 'cold':
            return []
        row['times_asc']
        arr = row['ballBefs'].tolist()[0]
        take = 6
        if str(row['state'].tolist()[0]) == 'hot':
            arr.reverse()
            arrHot = []
            # 離群值移除
            for ele in arr:
                if any(ele == c for c in row['markOutlierBefs']):
                    continue
                arrHot.append(ele)
            return arrHot[0:take]
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
        if row['state'].tolist()[0] == 'cold':
            return []

        arr = row['times_desc'].tolist()[0]
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

        # 這二個欄位是用來判斷是否簽注
        skipTimesKeys = keys[:-1]

        for skipTimesKey in skipTimesKeys:
            dfSign[f'{skipTimesKey}_varQ'] = dfSign[(
                skipTimesKey, 'varQ')].shift(1)
            dfSign[f'{skipTimesKey}_numOutliers'] = dfSign[(
                skipTimesKey, 'numOutliers')].shift(1)

        # loop會有多個拖期

        dfSign[f'{keys[-1]}_desc'] = dfSign[(keys[-1], 'desc')].shift(1)
        # # 過濾離散組合(且這邊設定take幾組)
        dfSign['excludeBalls'] = dfSign.apply(
            lambda row: self._excludeOutlierAndVarQ(row, skipTimesKeys), axis=1)

        # 最後運算出要簽牌組合
        dfSign['signBall2Ds'] = dfSign.apply(
            lambda row: self._compose2GroupBall2Ds(row), axis=1)

        # endregion

        if self._isToCsv and self._path is not None and self._filename is not None:
            self._exportFile.exportExcel(
                [dfSign], ['dfSign'], self._path, self._filename)
        return dfSign
        pass


if __name__ == '__main__':

    # region db info
    dbContext = db.MSSQLDbContext({'server': 'wpdb2.hihosting.hinet.net', 'user': 'p89880749_p89880749',
                                   'password': 'Jonny1070607!@#$%', 'database': 'p89880749_test'})
    rows = dbContext.select(
        'select drawNumberSize,lotteryDate from Daily539 ORDER BY period')
    inputs = list(map(lambda row: row['drawNumberSize'].split(','), rows))
    # endregion

    # region dfTimes、dfDefer
    exportFile = ExportFile()
    convertMark = ConvertMark()
    quantile = Quantile()
    quantile.cutFrt = 0
    quantile.cutEnd = 19
    deferMarkCalcu = DeferCalcu(exportFile, convertMark, quantile)
    deferMarkCalcu.includeColumns = ['numOutliers', 'varQ']
    dfDeferMarkInfo = deferMarkCalcu.calcu(inputs)

    quantile.cutFrt = 0
    quantile.cutEnd = 39
    beginConvertMark = BeginConvertMark()
    deferBallCalcu = DeferCalcu(exportFile, beginConvertMark, quantile)
    deferBallCalcu.includeColumns = ['numOutliers', 'varQ']
    dfDeferBallInfo = deferBallCalcu.calcu(inputs)

    timesCalcu = TimesCalcu(exportFile, beginConvertMark, quantile)
    quantile.cutFrt = 0
    quantile.cutEnd = 39
    timesCalcu.includeColumns = ['num', 'desc']
    dfTimesInfo = timesCalcu.calcu(inputs)
    # endregion
    keys = ['deferMark', 'deferBall', 'times']
    dfs = [dfDeferMarkInfo.dfDrop, dfDeferBallInfo.dfDrop, dfTimesInfo.dfDrop]
    path = 'C:/Programs/bingo/bingo_scrapy/539_calcu'
    filename = 'sign.xlsx'
    fiveThreeNineSign = FiveThreeNineSign(exportFile, True, path, filename)
    fiveThreeNineSign.take = 4
    dfSign = fiveThreeNineSign.sign(dfs, keys)

    pathPrize = 'C:/Programs/bingo/bingo_scrapy/539_calcu'
    filenamePrize = 'prize.xlsx'
    fiveThreeNineMatch = FiveThreeNineMatch()
    fiveThreeNinePrize = FiveThreeNinePrize(
        exportFile, fiveThreeNineMatch, True, pathPrize, filenamePrize)
    dfPrize = fiveThreeNinePrize.prize(dfSign)
    pass
