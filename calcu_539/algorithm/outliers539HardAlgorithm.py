from typing import List
import itertools
from pandas import Series, DataFrame
from calcu_539.algorithm.sign539ColdOverlay import Sign539ColdOverlay
from db.db import MSSQLDbContext
from calcu_539.algorithm.calcu_old import DeferCalcu, QLevel, TimesCalcu, DfInfo
from calcu_539.algorithm.mark_old import BeginConvertMark, ConvertMark, ConvertOddEvenMark
from calcu_539.excel.exportFile import ExportFile
from calcu_539.static.quantile_old import Quantile


class Outliers539HardAlgorithm:

    def __init__(self):
        pass

    def calcu(self, inputs: List[str]) -> List[List[str]]:
        # region 產生各種拖期:目前小一、單一、原始球號
        exportFile = ExportFile()
        quantileGroup2 = Quantile(QLevel=QLevel.Q10)
        quantileGroup2.cutFrt = 0
        quantileGroup2.cutEnd = 19

        # 小一group
        convertMark = ConvertMark()
        deferSmallMarkCalcu = DeferCalcu(
            exportFile, convertMark, quantileGroup2)
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

        def example_filter_function(row: Series) -> List[str]:
            # 可透過號碼數量來衡量權重
            # limit 越大、組數越小 要簽越少
            # limit 越小、組數越大 可簽越多
            # asc weight
            takeQty = 5
            # takeBalls = []
            if row[('index', '')] is None or row[('index', '')] < 10:
                return []
            takeBalls = row['times', 'asc'][:takeQty]
            # for num in nums:
            #     if num < 10:
            #         takeQty = 3

            return takeBalls

        import inspect
        # Get the signature of the function
        signature = inspect.signature(example_filter_function)
        # Get the parameters of the function
        parameters = signature.parameters
        # Print the number of parameters and their types
        print(f"Number of parameters: {len(parameters)}")
        for name, param in parameters.items():
            print(f"Parameter name: {name}, Type: {param.annotation}")
        print('')
        sign539ColdOverlay = Sign539ColdOverlay(filter_function=example_filter_function,
                                                obtain_ball_number=example_obtain_ball_number)

        dfs = [dfDeferSmallMarkInfo.dfDrop,
               dfDeferOddMarkInfo.dfDrop, dfDeferBallInfo.dfDrop]
        keys = ['deferSmallMark', 'deferOddMark', 'deferBall']

        # Use the calculation method
        dfSignInfo = sign539ColdOverlay.sign(
            dfs, dfTimesInfo.dfDrop, keys, 'times')
        return dfSignInfo.dfDrop
        pass
    pass


if __name__ == '__main__':
    # region db info
    dbContext = MSSQLDbContext({'server': 'wpdb2.hihosting.hinet.net', 'user': 'p89880749_p89880749',
                                'password': 'Jonny1070607!@#$%', 'database': 'p89880749_test'})
    rows = dbContext.select(
        'select top 100 drawNumberSize,lotteryDate from Daily539 ORDER BY period')
    inputs = list(map(lambda row: row['drawNumberSize'].split(','), rows))
    # endregion

    outliers539HardAlgorithm = Outliers539HardAlgorithm()
    results = outliers539HardAlgorithm.calcu(inputs)
    pass
