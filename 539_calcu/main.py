# 將calcu 全部弄到main
# calcu 提煉defer、times、outlier

from math import exp, nan
import re
from typing import List
from matplotlib import axis
import numpy as np
import pandas as pd
from pandas import DataFrame
import os
import unittest
from unittest.mock import Mock
from pandas.testing import assert_frame_equal
from abc import ABC, abstractmethod
from mlxtend.frequent_patterns import apriori, association_rules
from mlxtend.preprocessing import TransactionEncoder
import itertools
import db
from enum import Enum
import math


class StrategyPrize(Enum):
    Relation_Five_Compose_5 = 1
    Relation_Five_Compose_10 = 2
    Relation_Five_Compose_12 = 3
    Relation_Five_Compose_15 = 4
    Relation_Five_Compose_20 = 5
    Relation_Five_Compose_25 = 6


class ConvertMark:
    """將球號分組"""

    def __init__(self) -> None:
        pass

    def ballToMark(self, ball: str) -> str:
        """
        依照球號排序
        """
        if any(ball == n for n in ['01', '11']):
            return '小一'
        if any(ball == n for n in ['02', '12']):
            return '小二'
        if any(ball == n for n in ['03', '13']):
            return '小三'
        if any(ball == n for n in ['04', '14']):
            return '小四'
        if any(ball == n for n in ['05', '15']):
            return '小五'

        if any(ball == n for n in ['21', '31']):
            return '大一'
        if any(ball == n for n in ['22', '32']):
            return '大二'
        if any(ball == n for n in ['23', '33']):
            return '大三'
        if any(ball == n for n in ['24', '34']):
            return '大四'
        if any(ball == n for n in ['25', '35']):
            return '大五'

        if any(ball == n for n in ['06', '16']):
            return '小六'
        if any(ball == n for n in ['07', '17']):
            return '小七'
        if any(ball == n for n in ['08', '18']):
            return '小八'
        if any(ball == n for n in ['09', '19']):
            return '小九'

        if any(ball == n for n in ['26', '36']):
            return '大六'
        if any(ball == n for n in ['27', '37']):
            return '大七'
        if any(ball == n for n in ['28', '38']):
            return '大八'
        if any(ball == n for n in ['29', '39']):
            return '大九'

        if any(ball == n for n in ['10', '20', '30']):
            return '零'
        return ''

    def markToBalls(self, mark: str) -> list[str]:
        if mark == '小一':
            return ['01', '11']
        if mark == '小二':
            return ['02', '12']
        if mark == '小三':
            return ['03', '13']
        if mark == '小四':
            return ['04', '14']
        if mark == '小五':
            return ['05', '15']

        if mark == '大一':
            return ['21', '31']
        if mark == '大二':
            return ['22', '32']
        if mark == '大三':
            return ['23', '33']
        if mark == '大四':
            return ['24', '34']
        if mark == '大五':
            return ['25', '35']

        if mark == '小六':
            return ['06', '16']
        if mark == '小七':
            return ['07', '17']
        if mark == '小八':
            return ['08', '18']
        if mark == '小九':
            return ['09', '19']

        if mark == '大六':
            return ['26', '36']
        if mark == '大七':
            return ['27', '37']
        if mark == '大八':
            return ['28', '38']
        if mark == '大九':
            return ['29', '39']

        if mark == '零':
            return ['10', '20', '30']
        pass


class BallGroup:
    """
    球號分組資訊
    times單位可為拖期或次數
    """

    def __init__(self, sort: str, times: int):
        self._sort = sort
        self._times = times

    @property
    def sort(self) -> str:
        return self._sort

    @sort.setter
    def sort(self, value: str):
        self._sort = value

    @property
    def times(self) -> int:
        return self._times

    @times.setter
    def times(self, value: int):
        self._times = value


class ExportFile:
    """注入ICalcu子類別結果產出DataFrame To Csv"""

    def __init__(self) -> None:
        pass

    def exportCsv(self, df: DataFrame, path: str, filename: str) -> None:
        file = os.path.join(path, filename)
        # 檢查文件是否存在
        if os.path.exists(file):
            os.remove(file)  # 刪除已存在的文件
        df.to_csv(file, index=False, encoding='utf-8-sig')
        pass


class ICalcu(ABC):

    @abstractmethod
    def calcu(self, inputs: List[str]) -> DataFrame:
        pass


class TimesCalcu(ICalcu):
    """計算出分組標記累計次數"""

    def __init__(self, exportFile: ExportFile, timesBallInfos, convert: ConvertMark, isToCsv=False) -> None:
        self._exportFile = exportFile
        self._timesBallInfos = timesBallInfos
        self._convert = convert
        self._isToCsv = isToCsv
        pass

    def calcu(self, inputs: List[str]) -> DataFrame:
        time2Ds = []
        for idx, arr in enumerate(inputs):
            for ele in arr:
                mark = self._convert.ballToMark(ele)
                timesBall = next(
                    (x for x in self._timesBallInfos if x.sort == mark), None)
                timesBall.times += 1
                times = list(map(lambda x: x.times, self._timesBallInfos))
                std_dev = np.std(times)
                variance = np.var(times)
                times.append(std_dev)
                times.append(variance)
                times.append(inputs[idx])
            time2Ds.append(times)

        timesColumns = [ball.sort for ball in self._timesBallInfos]
        timesColumns.append('std')
        timesColumns.append('var')
        timesColumns.append('num')
        dfTimes = pd.DataFrame(time2Ds, columns=timesColumns)
        if self._isToCsv:
            self._exportFile.exportCsv(
                dfTimes, 'C:/Programs/bingo/bingo_scrapy/539_calcu', 'time.csv')
        return dfTimes

        pass


class DeferCalcu(ICalcu):
    """計算分組標記拖期次數,並衍生衡量集合離散欄位(標準差)、離群值欄位"""

    def __init__(self, exportFile: ExportFile, deferBallInfos, convert: ConvertMark, isToCsv=False) -> None:
        self._exportFile = exportFile
        self._deferBallInfos = deferBallInfos
        self._convert = convert
        self._isToCsv = isToCsv
        pass

    def _getOutlier(self, dfDefer: DataFrame) -> int:
        # region test 四分位距
        arr = []
        ballDeferColumns = dfDefer.columns[0:19]
        for column in ballDeferColumns:
            arr.extend(dfDefer[column].values)
            pass
        arr = sorted(arr, key=lambda e: e)
        npArr = np.array(arr)
        max = np.max(npArr)
        mean = np.mean(npArr)
        Q1 = np.quantile(npArr, 0.25)
        Q3 = np.quantile(npArr, 0.75)
        IQR = Q3 - Q1

        np.mean(npArr)

        # 設定離散值範圍
        # lower_bound ABS 連續6次0(或者1次也允許)
        # 離散值程度1.5可做調整
        lower_bound = Q1 - 1.5 * IQR
        upper_bound = Q3 + 1.5 * IQR
        return upper_bound
        # endregion

    def _getMarkOutliers(self, row: pd.Series):
        markOutliers = []
        if row['小一'] > 10:
            markOutliers.append('小一')
        if row['小二'] > 10:
            markOutliers.append('小二')
        if row['小三'] > 10:
            markOutliers.append('小三')
        if row['小四'] > 10:
            markOutliers.append('小四')
        if row['小五'] > 10:
            markOutliers.append('小五')
        if row['小六'] > 10:
            markOutliers.append('小六')
        if row['小七'] > 10:
            markOutliers.append('小七')
        if row['小八'] > 10:
            markOutliers.append('小八')
        if row['小九'] > 10:
            markOutliers.append('小九')

        if row['大一'] > 10:
            markOutliers.append('大一')
        if row['大二'] > 10:
            markOutliers.append('大二')
        if row['大三'] > 10:
            markOutliers.append('大三')
        if row['大四'] > 10:
            markOutliers.append('大四')
        if row['大五'] > 10:
            markOutliers.append('大五')
        if row['大六'] > 10:
            markOutliers.append('大六')
        if row['大七'] > 10:
            markOutliers.append('大七')
        if row['大八'] > 10:
            markOutliers.append('大八')
        if row['大九'] > 10:
            markOutliers.append('大九')
        return markOutliers
        pass

    def calcu(self, inputs: List[str]) -> DataFrame:
        """
        計算拖期
        """
        defer2Ds = []
        self._convert = ConvertMark()
        for idx, arr in enumerate(inputs):
            marks = [self._convert.ballToMark(ele) for ele in arr]
            for deferBall in self._deferBallInfos:
                if any(mark == deferBall.sort for mark in marks):
                    deferBall.times = 0
                else:
                    deferBall.times += 1
            defers = list(map(lambda x: x.times, self._deferBallInfos))
            std_dev = np.std(defers)
            variance = np.var(defers)
            defers.append(std_dev)
            defers.append(variance)
            defers.append(inputs[idx])
            defer2Ds.append(defers)

        deferColumns = [ball.sort for ball in self._deferBallInfos]
        deferColumns.append('std')
        deferColumns.append('var')
        deferColumns.append('num')
        dfDefer = pd.DataFrame(defer2Ds, columns=deferColumns)

        # 計算符合離群值mark
        outlier = self._getOutlier(dfDefer)
        dfDefer['markOutliers'] = dfDefer.apply(
            lambda row: self._getMarkOutliers(row), axis=1)

        if self._isToCsv:
            self._exportFile.exportCsv(
                dfDefer, 'C:/Programs/bingo/bingo_scrapy/539_calcu', 'defer.csv')
        return dfDefer
        pass

    pass


class RelationTerm:
    """計算二球之間關聯式規則,參數可透過前幾期、最小支持、信賴度來做關卡,過濾二球以上關聯規則"""
    @property
    def min_support(self):
        return self.__min_support

    @min_support.setter
    def min_support(self, value):
        self._min_support = value

    @property
    def frt(self):
        return self._frt

    @frt.setter
    def frt(self, value):
        self._frt = value

    @property
    def end(self):
        return self._end

    @end.setter
    def end(self, value):
        self._end = value

    @property
    def min_threshold(self):
        return self._min_threshold

    @min_threshold.setter
    def min_threshold(self, value):
        self._min_threshold = value

    def __init__(self, inputs: List[str]) -> None:
        self._min_support = 0
        self._min_threshold = 0
        self._inputs = inputs
        pass

    def calcu(self) -> List[List[str]]:

        ball2Ds = self._inputs[self._frt:self._end]
        te = TransactionEncoder()
        te_ary = te.fit(ball2Ds).transform(ball2Ds)
        df = pd.DataFrame(te_ary, columns=te.columns_)
        # 使用apriori找出频繁项集
        frequent_itemsets = apriori(
            df, min_support=self._min_support, use_colnames=True)
        if frequent_itemsets.empty:
            return []
        # 生成关联规则
        rules = association_rules(
            frequent_itemsets, metric="confidence", min_threshold=self._min_threshold)
        dfRelation = rules
        # 空的DataFrame
        if dfRelation.empty:
            return []
        dfRelation['result'] = dfRelation.apply(
            lambda row: self._mapToArrayFilterThree(row), axis=1)

        temps = list(
            filter(self._includeThree, dfRelation['result'].tolist()))
        temps = sorted(
            temps, key=lambda q: q['lift'], reverse=True)
        results = list(map(lambda x: x['arr'], temps))

        # 將每個內部陣列轉換為集合
        set_list = [set(inner_list) for inner_list in results]

        # 使用集合來比較內部陣列是否有重複
        unique_set_list = []

        for s in set_list:
            if s not in unique_set_list:
                unique_set_list.append(s)
        relationShips = [list(item) for item in unique_set_list]
        return relationShips
        pass

    # 過濾掉3個元素
    def _includeThree(self, obj):
        return len(obj['arr']) == 2
        print("")
        pass

    # 因為可能有3個元素存在,所以將frozenset to list and filter len == 2
    def _mapToArrayFilterThree(self, row: pd.Series):
        # 先將其合成一個obj,內含array and lift
        arrAntecedents = list(row['antecedents'])
        arrConsequents = list(row['consequents'])
        arrAntecedents.extend(arrConsequents)
        lift = float(row['lift'])
        return {'lift': lift, 'arr': arrAntecedents}
        print('')
        pass


class FiveThreeNineSign:
    """
    產出要簽注獎號策略:
    1.冷門球號開始 order by
    2.冷門球號過濾離群值
    3.變異數在某個區間表示夠離散要回補
    4.冷門球號做乘積組合(目前是笛卡爾乘積、但可能用指數)
    5.過濾關聯式和冷門組合球號命中
    6.過濾組合太多規則不明確不簽
    7.過濾變異數下注範圍
    """
    @property
    def strategy(self):
        return self._strategy

    @strategy.setter
    def strategy(self, value):
        self._strategy = value

    @property
    def frtTake(self):
        return self._frtTake

    @frtTake.setter
    def frtTake(self, value):
        self._frtTake = value

    @property
    def min_support(self):
        return self._min_support

    @min_support.setter
    def min_support(self, value):
        self._min_support = value

    @property
    def min_threshold(self):
        return self._min_threshold

    @min_threshold.setter
    def min_threshold(self, value):
        self._min_threshold = value

    @property
    def hot_limit(self):
        return self._hot_limit

    @hot_limit.setter
    def hot_limit(self, value):
        self._hot_limit = value

    def __init__(self, exportFile: ExportFile, convert: ConvertMark, relationCalcu: RelationTerm, isToCsv=False) -> None:
        self._exportFile = exportFile
        self._convert = convert
        self._isToCsv = isToCsv
        self._relationCalcu = relationCalcu
        self._frtTake = 12
        self._min_support = 0.1
        self._min_threshold = 0.7
        self._hot_limit = 13
        pass

    def _getState(self, row: pd.Series):
        if np.isnan(row['varBef'].values[0]):
            return 'cold'
        if row['varBef'].values[0] < 13.65:
            return 'cold'
        if len(row['markOutlierBefs'][0]) < 2:
            return 'cold'
        return 'hot'
        pass

    def sign(self, dfDefer: DataFrame, dfTimes: DataFrame) -> DataFrame:

        dfSign = pd.concat([dfDefer, dfTimes], axis=1, keys=['defer', 'times'])

        # region 刪除不需要計算column
        dfSign.drop(columns=[('defer', '零'), ('defer', '小一'), ('defer', '大一'), ('defer', '小二'), ('defer', '大二'),
                             ('defer', '小三'), ('defer',
                                               '大三'), ('defer', '小四'), ('defer', '大四'),
                             ('defer', '小五'), ('defer',
                                               '大五'), ('defer', '小六'), ('defer', '大六'),
                             ('defer', '小七'), ('defer',
                                               '大七'), ('defer', '小八'), ('defer', '大八'),
                             ('defer', '小九'), ('defer',
                                               '大九'), ('defer', 'std'), ('defer', 'num'),
                             ('times', 'std'), ('times', 'var'),
                             ], axis=1, inplace=True)
        # endregion

        dfSign = dfSign.reset_index(drop=False)
        # 判別期數若<10期直接輸出空array
        # 若>10期先判別標準差是高於10還是低於10,衍生欄位先呈現True、False
        # 後續再加上>10冷門求號 輸出4個
        # 後續再加上<10熱門求號 輸出4個

        # region 衍生欄位冷熱門球號、簽注分類、簽注球號計算方式

        # 這二個欄位是用來判斷是否簽注
        dfSign['varBef'] = dfSign[('defer', 'var')].shift(1).astype(float)
        dfSign['markOutlierBefs'] = dfSign[('defer', 'markOutliers')].shift(1)
        dfSign['state'] = dfSign.apply(lambda x: self._getState(x), axis=1)

        dfSign['balls'] = dfSign.apply(
            lambda row: self._convertRowAsc(row), axis=1)

        dfSign['ballBefs'] = dfSign['balls'].shift(1)

        dfSign['signMark'] = dfSign.apply(
            lambda row: self._getSign(row), axis=1)
        dfSign['signFrtBall2Ds'] = dfSign.apply(
            lambda row: self._getBalls(row), axis=1)

        # 要修改增加關聯式過濾規則
        # dfSign['relation2Ds'] = dfSign.apply(
        #     lambda row: self._getRelation(row), axis=1)

        # 將有吻合關聯式才簽牌,只要其中之一有命中就算
        dfSign['signBall2Ds'] = dfSign.apply(
            lambda row: self._excludeSign(row), axis=1)

        # endregion

        # region 衍生欄位關聯式規則
        # endregion

        if self._isToCsv:
            self._exportFile.exportCsv(
                dfSign, 'C:/Programs/bingo/bingo_scrapy/539_calcu', 'sign.csv')
        return dfSign
        pass

    def _excludeSign(self, row: pd.Series):
        if row['state'].tolist()[0] == 'cold':
            return []
        return row['signFrtBall2Ds'].tolist()[0]
        # 目前暫定不做relation直接將冷門球號簽注
        sign2Ds = []
        signFrtBall2Ds = row['signFrtBall2Ds'].tolist()[0]
        relation2Ds = row['relation2Ds'].tolist()[0]
        if len(signFrtBall2Ds) == 0 or row['state'].tolist()[0] == 'cold':
            return sign2Ds
        for signBall2D in signFrtBall2Ds:
            for relation2D in relation2Ds:
                # test 完全命中
                # if len(set(relation2D + signBall2D)) == 2 or len(set(relation2D + signBall2D)) == 3:
                if len(set(relation2D + signBall2D)) == 2:
                    sign2Ds.append(signBall2D)
                    break
        # 球號太少組合無法精準判別
        # if len(sign2Ds) >= 40:
        #     return []
        return sign2Ds
        pass

    def _getRelation(self, row: pd.Series):
        if int(row['index']) < self._frtTake:
            return []

        self._relationCalcu.min_support = self._min_support  # 最小支持度
        self._relationCalcu.min_threshold = self._min_threshold  # 最小信賴度
        self._relationCalcu.frt = int(row['index']) - self._frtTake  # 開始期數
        self._relationCalcu._end = int(row['index'])  # 結束期數
        results = self._relationCalcu.calcu()
        # 離群值過濾
        ballOutliers = [self._convert.markToBalls(
            c) for c in row[('defer', 'markOutliers')]]
        excludeOutliers = []
        for ele in results:
            if any(set(ele + c) == 2 or set(ele + c) == 3 for c in ballOutliers):
                continue
            excludeOutliers.append(ele)

        return excludeOutliers
        pass

    def _getBalls(self, row: pd.Series):
        marks = row['signMark'].tolist()[0]
        if marks == None or len(marks) == 0:
            return []

        ball2DResults = []
        # isProduct = True
        # # 判別是否笛卡爾乘積
        # if self._strategy == StrategyPrize.Relation_Five_Compose:
        ball2Ds = []
        for mark in marks:
            ball2Ds.append(self._convert.markToBalls(mark))

        # 合并所有列表
        combined_list = ball2Ds[0] + ball2Ds[1] + \
            ball2Ds[2] + ball2Ds[3] + ball2Ds[4] + ball2Ds[5]

        # 生成两个元素为一组的组合
        tpCombinations = list(itertools.product(combined_list, repeat=2))
        combinations = [list(tp) for tp in tpCombinations]

        for arr in combinations:
            if any(len(set(arr + ele)) == 2 for ele in ball2DResults) == False and arr[0] != arr[1]:
                ball2DResults.append(arr)

        # 驗證是否有重複組合,若有print
        excepted = math.comb(len(combined_list), 2)
        if excepted != len(ball2DResults):
            print('有重複組合')

        return ball2DResults
        pass

    def _getSign(self, row: pd.Series):
        if int(row['index']) < self._frtTake:
            return []
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

    def _convertRowAsc(self, row: pd.Series):
        rowBallGroups = [BallGroup('小一', row['times']['小一']), BallGroup('大一', row['times']['大一']),
                         BallGroup('小二', row['times']['小二']), BallGroup(
                             '大二', row['times']['大二']),
                         BallGroup('小三', row['times']['小三']), BallGroup(
                             '大三', row['times']['大三']),
                         BallGroup('小四', row['times']['小四']), BallGroup(
                             '大四', row['times']['大四']),
                         BallGroup('小五', row['times']['小五']), BallGroup(
                             '大五', row['times']['大五']),
                         BallGroup('小六', row['times']['小六']), BallGroup(
                             '大六', row['times']['大六']),
                         BallGroup('小七', row['times']['小七']), BallGroup(
                             '大七', row['times']['大七']),
                         BallGroup('小八', row['times']['小八']), BallGroup(
                             '大八', row['times']['大八']),
                         BallGroup('小九', row['times']['小九']), BallGroup(
                             '大九', row['times']['大九']),
                         ]
        rowBallGroups = sorted(rowBallGroups, key=lambda q: q.times)
        marks = list(map(lambda x: x.sort, rowBallGroups))
        return marks
        pass


class FiveThreeNinePrize:
    """檢驗簽注號碼是否命中,並統計當期簽注和命中數量、是否簽注和命中"""

    def __init__(self, exportFile: ExportFile, convert: ConvertMark, isToCsv=False) -> None:
        self._convert = convert
        self._exportFile = exportFile
        self._isToCsv = isToCsv
        pass

    def _varToQ(self, row: pd.Series):
        Q1 = 7.27
        Q2 = 10.48
        Q3 = 13.65
        if np.isnan(row[('varBef', '')]) or row[('varBef', '')] < Q1:
            return 'Q1'
        elif row[('varBef', '')] >= Q1 and row[('varBef', '')] < Q2:
            return 'Q2'
        elif row[('varBef', '')] >= Q2 and row[('varBef', '')] < Q3:
            return 'Q3'
        elif row[('varBef', '')] > Q3:
            return 'Q4'

    def _toOutlierQty(self, row: pd.Series):
        if row[('markOutlierBefs', '')] == None:
            return 0
        return len(row[('markOutlierBefs', '')])
        pass

    def prize(self, inputs: List[str], dfSign: DataFrame) -> DataFrame:

        dfPrize = pd.DataFrame(inputs, columns=['1', '2', '3', '4', '5'])
        dfPrize['一'] = dfPrize['1'].apply(
            lambda ele: self._convert.ballToMark(ele))
        dfPrize['二'] = dfPrize['2'].apply(
            lambda ele: self._convert.ballToMark(ele))
        dfPrize['三'] = dfPrize['3'].apply(
            lambda ele: self._convert.ballToMark(ele))
        dfPrize['四'] = dfPrize['4'].apply(
            lambda ele: self._convert.ballToMark(ele))
        dfPrize['五'] = dfPrize['5'].apply(
            lambda ele: self._convert.ballToMark(ele))
        dfPrize['stdBalls'] = dfPrize.apply(
            lambda row: [row['1'], row['2'], row['3'], row['4'], row['5']], axis=1)
        dfPrize['stdMarks'] = dfPrize.apply(
            lambda row: [row['一'], row['二'], row['三'], row['四'], row['五']], axis=1)
        dfPrize = pd.concat([dfSign, dfPrize], axis=1)
        dfPrize.drop(columns=['1', '2', '3', '4', '5', '一', '二',
                     '三', '四', '五', 'stdMarks'], axis=1, inplace=True)
        dfPrize['matchQty'] = dfPrize.apply(
            lambda row: self._match(row), axis=1)
        dfPrize['signQty'] = dfPrize.apply(
            lambda arr: self._calcuQty(arr), axis=1)

        dfPrize['actualProfit'] = dfPrize['matchQty'] * \
            1500 - dfPrize['signQty'] * 25
        dfPrize['outlierQty'] = dfPrize.apply(
            lambda arr: self._toOutlierQty(arr), axis=1)

        # 統計用:是否有簽注、是否都無命中
        dfPrize['isSign'] = dfPrize['signQty'] != 0
        dfPrize['isMatch'] = dfPrize.apply(
            lambda row: row['signQty'] != 0 and row['matchQty'] != 0, axis=1)

        # 變異數四分位距
       # Q1 = np.quantile(npArr, 0.25) #7.27
        # Q2 = np.quantile(npArr, 0.5) #10.48
        # Q3 = np.quantile(npArr, 0.75)#13.65
        dfPrize['varQ'] = dfPrize.apply(lambda row: self._varToQ(row), axis=1)

        # column 只留下matchQty、signQty、stdBalls、index (中獎、簽注數量、索引)
        dfPrize.drop(columns=[
            ('times', '小一'),  ('times', '小二'), ('times', '小三'), ('times', '小四'),
            ('times', '小五'),  ('times', '小六'), ('times',
                                                '小七'), ('times', '小八'), ('times', '小九'),
            ('times', '大一'),  ('times', '大二'), ('times', '大三'), ('times', '大四'),
            ('times', '大五'),  ('times', '大六'), ('times',
                                                '大七'), ('times', '大八'), ('times', '大九'),
            ('times', '零'),  ('balls', ''), ('signMark', ''), ('signFrtBall2Ds', ''),
            ('signBall2Ds', ''), ('signFrtBall2Ds', ''), ('times', 'num')], axis=1, inplace=True)

        if self._isToCsv:
            self._exportFile.exportCsv(
                dfPrize, 'C:/Programs/bingo/bingo_scrapy/539_calcu', 'prize.csv')
        return dfPrize
        pass

    def _calcuQty(self, row: pd.Series):
        if len(row[('signBall2Ds', '')]) == 0:
            return 0
        return len(row[('signBall2Ds', '')])
        pass

    def _match(self, row: pd.Series):
        if len(row[('signBall2Ds', '')]) == 0:
            return 0
        stdBalls = row['stdBalls']
        match = 0
        for balls in row[('signBall2Ds', '')]:
            if len(set(stdBalls + balls)) == 5:
                match += 1
        return match

    pass


class TestConvertMark(unittest.TestCase):
    def test_ballToMark(self):
        """球號轉換"""
        # arrange
        convert = ConvertMark()
        # act
        inputs = ['01', '12', '31', '38', '39']
        marks = [convert.ballToMark(ele) for ele in inputs]
        # assert
        excepteds = ['小一', '小二', '大一', '大九', '大八']
        self.assertCountEqual(marks, excepteds)
        pass

    def test_markToBalls(self):
        """分類轉球號"""
        # arrange
        convert = ConvertMark()
        # act
        inputs = ['小一', '小二', '大一', '大九', '大八']
        ball2Ds = [convert.markToBalls(ele) for ele in inputs]
        # assert
        excepted2Ds = [['02', '12'], ['01', '11'],  [
            '21', '31'], ['29', '39'], ['28', '38']]
        self.assertCountEqual(ball2Ds, excepted2Ds)
        pass


class TestDeferCalcu(unittest.TestCase):

    def test_calcu_df(self):
        """DataFrame相等結果"""
        # arrange
        mockExportFile = Mock()
        convert = ConvertMark()
        deferBallInfos = [
            BallGroup('小一', 0), BallGroup('小二', 0), BallGroup(
                '小三', 0), BallGroup('小四', 0), BallGroup('小五', 0),
            BallGroup('大一', 0), BallGroup('大二', 0), BallGroup(
                '大三', 0), BallGroup('大四', 0), BallGroup('大五', 0),
            BallGroup('小六', 0), BallGroup('小七', 0), BallGroup(
                '小八', 0), BallGroup('小九', 0),
            BallGroup('大六', 0), BallGroup('大七', 0), BallGroup(
                '大八', 0), BallGroup('大九', 0),
            BallGroup('零', 0),
        ]
        deferCalcu = DeferCalcu(mockExportFile, deferBallInfos, convert, True)

        # act
        sources = [
            {'bigShowOrder': "04,14,33,36,37"}, {'bigShowOrder': "01,07,11,15,29"}, {
                'bigShowOrder': "01,12,31,38,39"},
        ]
        results = list(
            map(lambda x: x['bigShowOrder'].split(','), sources))
        results.reverse()
        inputs = results
        dfDefer = deferCalcu.calcu(inputs)
        # assert
        exceptedColumns = ['小一', '小二', '小三', '小四', '小五', '大一', '大二', '大三', '大四', '大五',
                           '小六', '小七', '小八', '小九', '大六', '大七', '大八', '大九', '零', 'std', 'var', 'num']
        excepted2Ds = [
            [0, 0, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0,
                1, 0.440347, 0.193906, ['01', '12', '31', '38', '39']],
            [0, 1, 2, 2, 0, 1, 2, 2, 2, 2, 2, 0, 2, 2, 2, 2, 1, 0,
                2, 0.815365, 0.664820, ['01', '07', '11', '15', '29']],
            [1, 2, 3, 0, 1, 2, 3, 0, 3, 3, 3, 1, 3, 3, 0, 0, 2, 1,
                3, 1.195560, 1.429363, ['04', '14', '33', '36', '37']],
        ]

        dfExcepted = pd.DataFrame(excepted2Ds, columns=exceptedColumns)
        isEqual = None
        try:
            isEqual = assert_frame_equal(dfDefer, dfExcepted)
            isEqual = True
            print("DataFrames are equal")
        except AssertionError as e:
            isEqual = False
            print("DataFrames are not equal")
            print(e)
        self.assertEqual(isEqual, True)
        pass

    def test_to_csv_df(self):
        """ToCsv呼叫"""
        # arrange
        mockExportFile = Mock()
        convert = ConvertMark()
        deferCalcu = DeferCalcu(mockExportFile, [], convert, True)
        # act
        deferCalcu.calcu([])
        # assert
        excepted = 1
        self.assertEqual(excepted, mockExportFile.exportCsv.call_count)
        pass


class TestFiveThreeNinePrize(unittest.TestCase):

    def test_prize(self):
        """獎號計算"""
        # arrange
        exportFileMock = Mock()
        convertMark = ConvertMark()
        fiveThreeNinePrize = FiveThreeNinePrize(
            exportFile=exportFileMock, convert=convertMark)

        # act
        sources = [
            {'bigShowOrder': "04,14,33,36,37"}, {'bigShowOrder': "01,07,11,15,29"}, {
                'bigShowOrder': "01,12,31,38,39"},
        ]
        results = list(
            map(lambda x: x['bigShowOrder'].split(','), sources))
        results.reverse()
        inputs = results
        signColumns = [('signBall2Ds', '')]
        sign2Ds = [
            [[]],
            [[['01', '02'], ['03', '04'], ['11', '14']]],
            [[['01', '02'], ['36', '37']]]
        ]
        dfSign = DataFrame(sign2Ds, columns=signColumns)
        dfPrize = fiveThreeNinePrize.prize(inputs, dfSign)

        # assert
        signQty = dfPrize['signQty'].sum()
        matchQty = dfPrize['matchQty'].sum()
        exceptedSignQty = 5
        exceptedMatchQty = 1
        # signQty、matchQty
        self.assertEqual(signQty, exceptedSignQty)
        self.assertEqual(matchQty, exceptedMatchQty)
        pass


if __name__ == '__main__':

    # region calcu workflow

    dbContext = db.MSSQLDbContext({'server': 'wpdb2.hihosting.hinet.net', 'user': 'p89880749_p89880749',
                                   'password': 'Jonny1070607!@#$%', 'database': 'p89880749_test'})

    rows = dbContext.select(
        'select drawNumberSize,lotteryDate from Daily539 ORDER BY period')
    inputs = list(map(lambda row: row['drawNumberSize'].split(','), rows))

    print('')

    # region db來源,未來抽換先用hard code,先用30期模擬

    # firstAna = 0
    # endAna = 50
    # sources = [
    #     # 2024/07/06-2024/07/02
    #     {'bigShowOrder': "04,21,24,33,35"}, {'bigShowOrder': "17,18,23,24,28"}, {
    #         'bigShowOrder': "09,12,15,26,33"}, {'bigShowOrder': "04,20,25,33,34"}, {'bigShowOrder': "03,15,16,20,22"},
    #     # 2024/07/01-2024/06/26
    #     {'bigShowOrder': "08,11,17,19,23"}, {'bigShowOrder': "02,17,26,33,35"}, {
    #         'bigShowOrder': "12,16,25,27,39"}, {'bigShowOrder': "15,18,27,28,31"}, {'bigShowOrder': "02,21,37,38,39"},

    #     # 2024/06/25-2024/06/20
    #     {'bigShowOrder': "25,26,32,36,37"}, {'bigShowOrder': "03,13,17,32,39"}, {
    #         'bigShowOrder': "01,21,22,25,27"}, {'bigShowOrder': "10,12,15,16,23"}, {'bigShowOrder': "12,13,16,20,32"},
    #     # 2024/06/19-2024/06/14
    #     {'bigShowOrder': "02,10,11,14,22"}, {'bigShowOrder': "02,09,15,29,38"}, {
    #         'bigShowOrder': "02,08,26,32,34"}, {'bigShowOrder': "05,08,35,36,37"}, {'bigShowOrder': "01,02,17,20,37"},
    #     # 2024/06/13-2024/06/08
    #     {'bigShowOrder': "03,12,17,30,38"}, {'bigShowOrder': "14,19,20,29,32"}, {
    #         'bigShowOrder': "03,13,26,32,34"}, {'bigShowOrder': "18,19,30,33,38"}, {'bigShowOrder': "11,19,24,31,32"},
    #     # 2024/06/07-2024/06/03
    #     {'bigShowOrder': "01,04,27,34,35"}, {'bigShowOrder': "03,11,20,21,36"}, {
    #         'bigShowOrder': "03,04,06,14,20"}, {'bigShowOrder': "07,11,17,23,25"}, {'bigShowOrder': "06,10,21,24,31"},
    #     # 2024/06/01-2024/05/28
    #     {'bigShowOrder': "04,20,24,28,38"}, {'bigShowOrder': "08,12,13,23,36"}, {
    #         'bigShowOrder': "02,09,32,36,37"}, {'bigShowOrder': "01,07,09,20,32"}, {'bigShowOrder': "16,23,29,36,39"},
    #     # 2024/05/27-2024/05/22
    #     {'bigShowOrder': "05,13,14,17,24"}, {'bigShowOrder': "01,15,32,34,38"}, {
    #         'bigShowOrder': "05,16,22,26,39"}, {'bigShowOrder': "14,23,26,27,34"}, {'bigShowOrder': "11,13,15,23,29"},
    #     # 2024/05/21-2024/05/16
    #     {'bigShowOrder': "01,03,16,24,31"}, {'bigShowOrder': "03,05,28,32,34"}, {
    #         'bigShowOrder': "05,10,11,32,37"}, {'bigShowOrder': "14,19,27,30,38"}, {'bigShowOrder': "09,10,21,33,35"},
    #     # 2024/05/15-2024/05/10
    #     {'bigShowOrder': "04,06,14,26,33"}, {'bigShowOrder': "07,11,18,20,22"}, {
    #         'bigShowOrder': "04,14,33,36,37"}, {'bigShowOrder': "01,07,11,15,29"}, {'bigShowOrder': "01,12,31,38,39"},
    # ]

    # results = list(
    #     map(lambda x: x['bigShowOrder'].split(','), sources))
    # results.reverse()
    # inputs = results[firstAna:endAna]
    # endregion

    deferBallInfos = [
        BallGroup('小一', 0), BallGroup('小二', 0), BallGroup(
            '小三', 0), BallGroup('小四', 0), BallGroup('小五', 0),
        BallGroup('大一', 0), BallGroup('大二', 0), BallGroup(
            '大三', 0), BallGroup('大四', 0), BallGroup('大五', 0),
        BallGroup('小六', 0), BallGroup('小七', 0), BallGroup(
            '小八', 0), BallGroup('小九', 0),
        BallGroup('大六', 0), BallGroup('大七', 0), BallGroup(
            '大八', 0), BallGroup('大九', 0),
        BallGroup('零', 0),
    ]

    convertMark = ConvertMark()
    exportFile = ExportFile()
    deferCalcu = DeferCalcu(
        exportFile=exportFile, deferBallInfos=deferBallInfos, convert=convertMark, isToCsv=True)
    dfDefer = deferCalcu.calcu(inputs)

    timesBallInfos = [BallGroup('小一', 0), BallGroup('小二', 0), BallGroup(
        '小三', 0), BallGroup('小四', 0), BallGroup('小五', 0),
        BallGroup('大一', 0), BallGroup('大二', 0), BallGroup(
        '大三', 0), BallGroup('大四', 0), BallGroup('大五', 0),
        BallGroup('小六', 0), BallGroup('小七', 0), BallGroup(
        '小八', 0), BallGroup('小九', 0),
        BallGroup('大六', 0), BallGroup('大七', 0), BallGroup(
        '大八', 0), BallGroup('大九', 0),
        BallGroup('零', 0),
    ]

    timesCalcu = TimesCalcu(
        exportFile=exportFile, timesBallInfos=timesBallInfos, convert=convertMark, isToCsv=True)
    dfTimes = timesCalcu.calcu(inputs)

    relationTerm = RelationTerm(inputs=inputs)
    # stategy = [StrategyPrize.Relation_Five_Compose_5, StrategyPrize.Relation_Five_Compose_10, StrategyPrize.Relation_Five_Compose_12,
    #            StrategyPrize.Relation_Five_Compose_15, StrategyPrize.Relation_Five_Compose_20, StrategyPrize.Relation_Five_Compose_25]
    stategy = [StrategyPrize.Relation_Five_Compose_12]
    for stat in stategy:
        fiveThreeNineSign = FiveThreeNineSign(
            exportFile, convertMark, relationTerm, True)
        fiveThreeNineSign.strategy = stat
        # if stat == StrategyPrize.Relation_Five_Compose_5:
        #     fiveThreeNineSign.frtTake = 5
        # if stat == StrategyPrize.Relation_Five_Compose_10:
        #     fiveThreeNineSign.frtTake = 10

        if stat == StrategyPrize.Relation_Five_Compose_12:
            fiveThreeNineSign.frtTake = 12
            fiveThreeNineSign.min_support = 0.15
            fiveThreeNineSign.min_threshold = 0.6
            fiveThreeNineSign.hot_limit = 1
        # if stat == StrategyPrize.Relation_Five_Compose_15:
        #     fiveThreeNineSign.frtTake = 15
        # if stat == StrategyPrize.Relation_Five_Compose_20:
        #     fiveThreeNineSign.frtTake = 20
        # if stat == StrategyPrize.Relation_Five_Compose_25:
        #     fiveThreeNineSign.frtTake = 25
        dfSign = fiveThreeNineSign.sign(dfDefer, dfTimes)

        fiveThreeNinePrize = FiveThreeNinePrize(exportFile, convertMark, True)
        dfPrize = fiveThreeNinePrize.prize(inputs, dfSign)

        # region 統計各區間利潤
        # 計算變異數占比
        # 計算離群值占比
        # 各占比所獲得利潤

        colOutlier = dfPrize.groupby('outlierQty').groups.keys()
        countOutlier = dfPrize.groupby('outlierQty')['outlierQty'].count()

        profitOutlier = dfPrize.groupby('outlierQty')[
            'actualProfit'].sum().tolist()
        dfOutlier = pd.DataFrame(
            [profitOutlier, countOutlier], columns=colOutlier, index=['profit', 'num'])

        # var 4分位距
        colVar = dfPrize.groupby('varQ').groups.keys()
        profitVar = dfPrize.groupby('varQ')[
            'actualProfit'].sum().tolist()
        dfVar = pd.DataFrame([profitVar], columns=colVar)
        # arr = sorted(dfPrize[('defer', 'var')].tolist(), key=lambda e: e)
        # npArr = np.array(arr)
        # max = np.max(npArr)
        # mean = np.mean(npArr)
        # Q1 = np.quantile(npArr, 0.25) #7.27
        # Q2 = np.quantile(npArr, 0.5) #10.48
        # Q3 = np.quantile(npArr, 0.75)#13.65
        print('')

        # endregion

        # region 計算收益
        # signTerm = dfPrize['signQty'].count()
        signMax = dfPrize['signQty'].max()
        signTerm = len(
            list(filter(lambda e: e == True, dfPrize['isSign'].values)))
        matchTerm = len(
            list(filter(lambda e: e == True, dfPrize['isMatch'].values)))
        # termPercent = matchTerm / signTerm
        termPercent = 0
        termFormatedPercent = '{:.2%}'.format(termPercent)
        matchSumQty = dfPrize['matchQty'].sum()
        signSumQty = dfPrize['signQty'].sum()
        matchPercent = matchSumQty / signSumQty
        formatedPercent = '{:.2%}'.format(matchPercent)
        profit = 1500 * matchSumQty
        cost = 25 * signSumQty
        actualProfit = profit - cost
        print(f'name:{stat.name}')
        print(f'actualProfit:{actualProfit}')
        print(f'profit:{profit}')
        print(f'cost:{cost}')
        dfProfit = pd.DataFrame(
            {'總損益': [actualProfit], '成本': [cost], '期數命中率': [termFormatedPercent], '注數命中率': [formatedPercent]
             })
        # endregion

        resultFile = 'C:/Programs/bingo/bingo_scrapy/539_calcu/excel/merged_{}.xlsx'.format(
            stat.name)
        if os.path.exists(resultFile):
            os.remove(resultFile)
        with pd.ExcelWriter(resultFile, engine='openpyxl') as writer:
            # Write each DataFrame to a separate sheet
            dfDefer.to_excel(writer, sheet_name='defer', index=False)
            dfTimes.to_excel(writer, sheet_name='times', index=False)
            dfSign.to_excel(writer, sheet_name='sign', index=True)
            dfPrize.to_excel(writer, sheet_name='prize', index=False)
            dfProfit.to_excel(writer, sheet_name='profit', index=False)
            dfOutlier.to_excel(writer, sheet_name='outlier', index=True)
            dfVar.to_excel(writer, sheet_name='var', index=False)

    pass
    # endregion

    # region test case

    # try:
    #     suite = unittest.TestSuite()
    #     suite.addTest(TestDeferCalcu('test_to_csv_df'))
    #     suite.addTest(TestDeferCalcu('test_calcu_df'))
    #     suite.addTest(TestConvertMark('test_ballToMark'))
    #     suite.addTest(TestConvertMark('test_markToBalls'))
    #     suite.addTest(TestFiveThreeNinePrize('test_prize'))
    #     # suite.addTest(TestDeferCalcu('test_calcu_3mean'))
    #     runner = unittest.TextTestRunner(verbosity=2)
    #     runner.run(suite)
    # except SystemExit:
    #     pass

    # endregion


# 優化
# DeferCalcu、TimesCalcu 提煉ICalcu to csv path
# 離群值提煉class,並透過相依注入


# 策略
# 關聯式規則是用在類似離群背景值、而不是動態
# 研究頻率各項目如何計算
# 確認笛卡爾乘積是否2的3次方


# 關聯式規則注中二者之間關聯 (關聯並不受變異數影響,可能要加入在關聯變數內)
# 冷門注重再回補次數
# 目前是冷門有符合關聯才match進去


# 修改
# 變異數占比統計波動
# 了解離群值占比
# 無離群值中獎獲利

# 計算變異數占比
# 計算離群值占比
# 各占比所獲得利潤

# 假定變異數變大會產生要補冷門求號，但關聯式規則應該要加入變異數
# 並且應是透過
# 個人感覺二者策略有衝突，關聯式規則應是增加而不是過濾
# 動態調整萃取關聯式規則

# 確定規則
# 離群值對簽注是有幫助的
# 有多少是有過濾掉離群值
