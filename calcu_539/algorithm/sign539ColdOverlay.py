from typing import Callable, List
from numpy import mat, sign, take
import pandas as pd
from pandas import Series, DataFrame
import inspect
import re
import itertools
from calcu_539.algorithm.calcu_old import DeferCalcu, QLevel, TimesCalcu, DfInfo
from calcu_539.algorithm.mark_old import BeginConvertMark, ConvertMark, ConvertOddEvenMark
from calcu_539.excel.exportFile import ExportFile
from calcu_539.static.quantile_old import Quantile
from calcu_539.prize.prize_539old import FiveThreeNinePrize
from db.db import MSSQLDbContext
from calcu_539.prize.match import FiveThreeNineMatch


class Sign539ColdOverlay:
    """
    A class to represent a ball filter with two proxy functions and a calculation method.
    """

    def __init__(self, filter_function: Callable[[Series], List[str]], obtain_ball_number: Callable[[List[str]], List[List[str]]]) -> None:
        """
        Initialize the BallFilter class with two proxy functions.

        :param filter_function:依據欄位設定各種條件，所生成要簽注號碼列表(目前是透過拖期越久去撈取離群值)
        :param obtain_ball_number: 依據過濾後的號碼，組合成對應要簽注二合號碼，若要加注直接重複產生二合號碼即可
        """
        self._filter_function = filter_function
        self._obtain_ball_number = obtain_ball_number

    def _calcuFrt(self, row: pd.Series):
        order = 0
        matchTime = 0
        if row[('times', 'asc')] == None:
            return 0
        for asc in row[('times', 'asc')]:
            if any(asc == num for num in row[('times', 'num')]):
                order += 1
                matchTime += 1
            else:
                order += 1
            if matchTime == 2:
                return order
        return order
        pass

    def sign(self, dfs: List[DataFrame], dfTimes: DataFrame, deferKeys: List[str], timesKey: str) -> DfInfo:
        """
        將拖期numOutliers、varQ 都shift(1)到下一期
        將開出次數asc都shift(1)到下一期
        insert last row 將shift少掉最後一期的資料補上

        :param df: The input DataFrame.
        :return: A DataFrame signBall2Ds、num
        """
        dfTemps = dfs
        dfTemps.append(dfTimes)
        tempKeys = deferKeys.copy()
        tempKeys.append(timesKey)
        dfSign = pd.concat(dfTemps, axis=1, keys=tempKeys)
        dfSign.reset_index(inplace=True)
        for deferKey in deferKeys:
            dfSign[f'{deferKey}_varQ'] = dfSign[(
                deferKey, 'varQ')].shift(1)
            dfSign[f'{deferKey}_numOutliers'] = dfSign[(
                deferKey, 'numOutliers')].shift(1)

        dfSign[f'{timesKey}_asc'] = dfSign[(timesKey, 'asc')].shift(1)

        # region insert last row 將shift少掉最後一期的資料補上
        AlastIdx = dfSign[(timesKey, 'asc')].size - 1
        row = {}
        for col in dfSign.columns:
            strCol = str(col[0])
            strSort = str(col[1])
            varQResult = next(
                (deferKey for deferKey in deferKeys if strCol == f'{deferKey}_varQ'), None)
            numOutliersResult = next(
                (deferKey for deferKey in deferKeys if strCol == f'{deferKey}_numOutliers'), None)
            if strCol == f'{timesKey}_asc':
                row[col] = dfSign[(timesKey, 'asc')].iloc[AlastIdx]
            elif varQResult is not None and strSort == '':
                row[col] = dfSign[(varQResult, 'varQ')].iloc[AlastIdx]
            elif numOutliersResult is not None and strSort == '':
                row[col] = dfSign[(numOutliersResult,
                                   'numOutliers')].iloc[AlastIdx]
            else:
                row[col] = None
        dfSign = dfSign.append(row, ignore_index=True)
        # dfSign = dfSign.append(row, ignore_index=True)
        # endregion

        import inspect
        # Get the signature of the function
        signature = inspect.signature(self._filter_function)
        # Get the parameters of the function
        parameters = signature.parameters

        # Print the number of parameters and their types
        print(f"Number of parameters: {len(parameters)}")
        for name, param in parameters.items():
            print(f"Parameter name: {name}, Type: {param.annotation}")

        dfSign['orderMatch'] = dfSign.apply(
            lambda row: self._calcuFrt(row), axis=1)
        dfSign['takeBalls'] = dfSign.apply(
            lambda row: self._filter_function(row), axis=1)
        dfSign['signBall2Ds'] = dfSign.apply(
            lambda row: self._obtain_ball_number(row[('takeBalls', '')]), axis=1)
        dfSignInfo = DfInfo()
        dfSignInfo.df = dfSign
        dropColumns = []
        includeColumns = [('times', 'num'), ('signBall2Ds', '')]
        for column in dfSign.columns:
            if any(column == includeColumn for includeColumn in includeColumns) == False:
                dropColumns.append(column)
        dfSignDrop = dfSign.copy(deep=True)
        dfSignDrop.drop(columns=dropColumns, inplace=True)
        dfSignInfo.dfDrop = dfSignDrop
        return dfSignInfo


if __name__ == '__main__':

    def example_filter_function(row: Series) -> List[str]:
        # 可透過號碼數量來衡量權重
        # limit 越大、組數越小 要簽越少
        # limit 越小、組數越大 可簽越多
        # asc weight
        takeQty = 5
        takeBalls = []
        if row[('index', '')] is None or row[('index', '')] < 10:
            return []
        takeBalls = row['times', 'asc'][:takeQty]
        # for num in nums:
        #     if num < 10:
        #         takeQty = 3

        return takeBalls

    def example_obtain_ball_number(keys: List[str]) -> List[List[str]]:
        if len(keys) == 0:
            return []
        tpCombinations = list(itertools.product(keys, repeat=2))
        combinations = [list(tp) for tp in tpCombinations]
        signBall2Ds = []
        for arr in combinations:
            if any(len(set(arr + ele)) == 2 for ele in signBall2Ds) == False and arr[0] != arr[1]:
                signBall2Ds.append(arr)
        return signBall2Ds

    # region db info
    dbContext = MSSQLDbContext({'server': 'wpdb2.hihosting.hinet.net', 'user': 'p89880749_p89880749',
                                'password': 'Jonny1070607!@#$%', 'database': 'p89880749_test'})
    rows = dbContext.select(
        'select top 100 drawNumberSize,lotteryDate from Daily539 ORDER BY period')
    inputs = list(map(lambda row: row['drawNumberSize'].split(','), rows))
    # endregion

    # region 產生各種拖期:目前小一、單一、原始球號
    exportFile = ExportFile()
    quantileGroup2 = Quantile(QLevel=QLevel.Q10)
    quantileGroup2.cutFrt = 0
    quantileGroup2.cutEnd = 19

    # 小一group
    convertMark = ConvertMark()
    deferSmallMarkCalcu = DeferCalcu(exportFile, convertMark, quantileGroup2)
    deferSmallMarkCalcu.includeColumns = ['numOutliers', 'varQ']
    dfDeferSmallMarkInfo = deferSmallMarkCalcu.calcu(inputs)

    # 單一group
    convertOddEvenMark = ConvertOddEvenMark()
    deferOddMarkCalcu = DeferCalcu(
        exportFile, convertOddEvenMark, quantileGroup2)
    deferOddMarkCalcu.includeColumns = ['numOutliers', 'varQ']
    dfDeferOddMarkInfo = deferOddMarkCalcu.calcu(inputs)

    quantile = Quantile(QLevel=QLevel.Q10)
    quantile.cutFrt = 0
    quantile.cutEnd = 39
    beginConvertMark = BeginConvertMark()
    deferBallCalcu = DeferCalcu(exportFile, beginConvertMark, quantile)
    deferBallCalcu.includeColumns = ['numOutliers', 'varQ']
    dfDeferBallInfo = deferBallCalcu.calcu(inputs)

    # endregion

    # region 冷門球號次數
    timesCalcu = TimesCalcu(exportFile, beginConvertMark, quantile)
    quantile.cutFrt = 0
    quantile.cutEnd = 39
    timesCalcu.includeColumns = ['num', 'asc']
    dfTimesInfo = timesCalcu.calcu(inputs)

    # endregion

    # Create an instance of BallFilter with the example functions
    sign539ColdOverlay = Sign539ColdOverlay(filter_function=example_filter_function,
                                            obtain_ball_number=example_obtain_ball_number)

    dfs = [dfDeferSmallMarkInfo.dfDrop,
           dfDeferOddMarkInfo.dfDrop, dfDeferBallInfo.dfDrop]
    keys = ['deferSmallMark', 'deferOddMark', 'deferBall']

    # Use the calculation method
    dfSignInfo = sign539ColdOverlay.sign(
        dfs, dfTimesInfo.dfDrop, keys, 'times')
    fiveThreeNineMatch = FiveThreeNineMatch()
    fiveThreeNinePrize = FiveThreeNinePrize(fiveThreeNineMatch)
    dfPrize = fiveThreeNinePrize.prize(dfSignInfo.dfDrop)
    signQty = dfPrize['signQty'].sum()
    matchQty = dfPrize['matchQty'].sum()
    matchPercent = 0 if signQty == 0 else matchQty/signQty
    matchPercentFormatted = f"{matchPercent:.2%}"
    dfProfit = DataFrame({'profit': [dfPrize['profit'].sum()],
                          'matchPercent': [matchPercentFormatted]})
    exportFile.exportExcel([dfSignInfo.df, dfPrize, dfProfit], ['sign539ColdOverlay', 'prize', 'profit'],
                           'C:/Programs/bingo/bingo_scrapy/calcu_539/test_data', 'sign539ColdOverlay.xlsx')
