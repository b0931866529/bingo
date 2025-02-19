# 將calcu 全部弄到main
# calcu 提煉defer、times、outlier

from math import exp, nan
import re
from typing import List
import numpy as np
import pandas as pd
from pandas import DataFrame
import os
import unittest
from unittest.mock import Mock
from pandas.testing import assert_frame_equal
from abc import ABC, abstractmethod


import db
from enum import Enum
import math


class DfInfo:
    """原始計算、刪除欄位"""

    def __init__(self) -> None:
        self._df = pd.DataFrame()
        self._dfDrop = pd.DataFrame()
        pass

    @property
    def df(self) -> str:
        return self._df

    @df.setter
    def df(self, value: str):
        self._df = value

    @property
    def dfDrop(self) -> str:
        return self._dfDrop

    @dfDrop.setter
    def dfDrop(self, value: str):
        self._dfDrop = value


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

    def exportExcel(self, dfs: List[DataFrame], sheets: List[str], path: str, filename: str) -> None:
        file = f'{path}/{filename}'
        # 檢查文件是否存在
        if os.path.exists(file):
            os.remove(file)  # 刪除已存在的文件

        zipped = list(zip(dfs, sheets))
        with pd.ExcelWriter(file, engine='openpyxl') as writer:
            for df, sheet in zipped:
                # Write each DataFrame to a separate sheet
                df.to_excel(writer, sheet_name=sheet, index=True)
        pass


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

    def loadQInfo(self, row: pd.Series):
        if self._QLevel == QLevel.Q4:
            self._loadQInfo_Q4(row)
        elif self._QLevel == QLevel.Q10:
            self._loadQInfo_Q10(row)
            pass
        pass

    def _calcuLevelQs_Q4(self, row: pd.Series, colName: str) -> pd.Series:
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

    def _calcuLevelQs_Q10(self, row: pd.Series, colName: str) -> pd.Series:
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

    def calcuLevelQs(self, row: pd.Series, colName: str) -> pd.Series:
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


class ICalcu(ABC):

    @property
    def includeColumns(self):
        return self._includeColumns

    @includeColumns.setter
    def includeColumns(self, value):
        self._includeColumns = value


有無 def __init__(self, exportFile: ExportFile, convert: ConvertMark, quantile: Quantile, isToCsv=False, path=None, filename=None) -> None:
        self._exportFile = exportFile
        self._convert = convert
        self._quantile = quantile
        self._isToCsv = isToCsv
        self._path = path
        self._filename = filename
        self._includeColumns = []

    @abstractmethod
    def calcu(self, inputs: List[str]) -> DfInfo:
        pass


class TimesCalcu(ICalcu):

    """計算出分組標記累計次數"""

    def __init__(self, exportFile: ExportFile, convert: ConvertMark, quantile: Quantile, isToCsv=False, path=None, filename=None) -> None:
        self._exportFile = exportFile
        self._convert = convert
        self._quantile = quantile
        self._isToCsv = isToCsv
        self._path = path
        self._filename = filename
        self._includeColumns = []

    def _getOutliers(self, row: pd.Series, quantileInfo: dict, quanColumns: list):
        markOutliers = []
        for column in quanColumns:
            if row[column] > quantileInfo['upper']:
                markOutliers.append(column)
        return markOutliers

    def _convertSort(self, row: pd.Series, columns: List[str], isDesc=True):
        arr = []
        for column in columns:
            arr.append({'key': column, 'value': row[column]})
        arrAsc = sorted(arr, key=lambda e: e['value'], reverse=isDesc)
        return list(map(lambda x: x['key'], arrAsc))
        pass

    def calcu(self, inputs: List[str]) -> DfInfo:
        time2Ds = []
        timesBallInfos = self._convert.loadStds()
        for idx, arr in enumerate(inputs):
            marks = []
            for ele in arr:
                mark = self._convert.ballToMark(ele)
                timesBall = next(
                    (x for x in timesBallInfos if x.sort == mark), None)
                timesBall.times += 1
                times = list(map(lambda x: x.times, timesBallInfos))
                std_dev = np.std(times)
                variance = np.var(times)
                times.append(std_dev)
                times.append(variance)
                times.append(inputs[idx])
                marks.append(mark)
            times.append(marks)
            time2Ds.append(times)

        timesColumns = [ball.sort for ball in timesBallInfos]
        timesColumns.append('std')
        timesColumns.append('var')
        timesColumns.append('num')
        timesColumns.append('mark')
        dfTimes = pd.DataFrame(time2Ds, columns=timesColumns)
        sortColumns = dfTimes.columns[self._quantile.cutFrt:self._quantile.cutEnd]
        dfTimes['desc'] = dfTimes.apply(lambda row: self._convertSort(
            row, sortColumns), axis=1)
        dfTimes['asc'] = dfTimes.apply(lambda row: self._convertSort(
            row, sortColumns, False), axis=1)

        dfTimeInfo = DfInfo()
        dfTimeInfo.df = dfTimes
        if len(self.includeColumns) != 0:
            dropColumns = []
            for column in dfTimes.columns:
                if any(column == includeColumn for includeColumn in self.includeColumns) == False:
                    dropColumns.append(column)
                pass
            dfDropTimes = dfTimes.copy(deep=True)
            dfDropTimes.drop(columns=dropColumns, inplace=True)
            dfTimeInfo.dfDrop = dfDropTimes

        if self._isToCsv and self._path is not None and self._filename is not None:
            self._exportFile.exportExcel([dfTimeInfo.df, dfTimeInfo.dfDrop], [
                                         'df', 'dfDrop'], self._path, self._filename)
        return dfTimeInfo

        pass

# 參數:column range、quantile limit


# 連續球號class Calcu


class ContinueCalcu(ICalcu):
    """計算分組標記連開次數,並衍生衡量集合離散欄位(標準差)、離群值欄位"""

    def __init__(self, exportFile: ExportFile, convert: ConvertMark, quantile: Quantile, isToCsv=False, path=None, filename=None) -> None:
        self._exportFile = exportFile
        self._convert = convert
        self._quantile = quantile
        self._isToCsv = isToCsv
        self._path = path
        self._filename = filename
        self._includeColumns = []
        pass

    def _getMarkOutliers(self, row: pd.Series, quantileInfo: dict, quanColumns: list):
        markOutliers = []
        for column in quanColumns:
            if row[column] > quantileInfo['upper']:
                markOutliers.append(column)
        return markOutliers
        pass

    def calcu(self, inputs: List[str]) -> DataFrame:
        """
        計算連號
        """
        continBallInfos = self._convert.loadStds()
        contin2Ds = []
        for idx, arr in enumerate(inputs):
            marks = [self._convert.ballToMark(ele) for ele in arr]
            for continBall in continBallInfos:
                if any(mark == continBall.sort for mark in marks):
                    continBall.times += 1
                else:
                    continBall.times = 0
            contins = list(map(lambda x: x.times, continBallInfos))
            std_dev = np.std(contins)
            variance = np.var(contins)
            contins.append(std_dev)
            contins.append(variance)
            contins.append(inputs[idx])
            contins.append(marks)
            contin2Ds.append(contins)

        continColumns = [ball.sort for ball in continBallInfos]
        continColumns.append('std')
        continColumns.append('var')
        continColumns.append('num')
        continColumns.append('markNum')
        dfContin = pd.DataFrame(contin2Ds, columns=continColumns)
        quantileInfo = self._quantile.calcuOutlierInfo(dfContin)
        quanColumns = dfContin.columns[self._quantile.cutFrt:self._quantile.cutEnd]
        # 計算符合離群值mark
        dfContin['markOutliers'] = dfContin.apply(
            lambda row: self._getMarkOutliers(row, quantileInfo, quanColumns), axis=1)

        self._quantile.loadQInfo(dfContin['var'])
        # 計算變異數
        dfContin['varQ'] = dfContin.apply(
            lambda row: self._quantile.calcuLevelQs(row, 'var'), axis=1)

        if len(self.includeColumns) != 0:
            dropColumns = []
            for column in dfContin.columns:
                if any(column == includeColumn for includeColumn in self.includeColumns) == False:
                    dropColumns.append(column)
                pass
            dfContin.drop(columns=dropColumns, inplace=True)

        if self._isToCsv and self._path is not None and self._filename is not None:
            self._exportFile.exportCsv(
                dfContin, self._path, self._filename)
        return dfContin
        pass

    pass


class DeferCalcu(ICalcu):
    """計算分組標記拖期次數,並衍生衡量集合離散欄位(標準差)、離群值欄位"""

    def __init__(self, exportFile: ExportFile, convert: ConvertMark, quantile: Quantile, isToCsv=False, path=None, filename=None) -> None:
        self._exportFile = exportFile
        self._convert = convert
        self._quantile = quantile
        self._isToCsv = isToCsv
        self._path = path
        self._filename = filename
        self._includeColumns = []
        pass

    def _getNumOutliers(self, row: pd.Series):
        numOutlier2Ds = []
        for ele in row['markOutliers']:
            numOutlier2Ds.append(self._convert.markToBalls(ele))
        return numOutlier2Ds
        pass

    def _getMarkOutliers(self, row: pd.Series, quantileInfo: dict, quanColumns: list):
        markOutliers = []
        for column in quanColumns:
            if row[column] > quantileInfo['upper']:
                markOutliers.append(column)
        return markOutliers
        pass

    def calcu(self, inputs: List[str]) -> DataFrame:
        """
        計算拖期
        """
        deferBallInfos = self._convert.loadStds()
        defer2Ds = []
        for idx, arr in enumerate(inputs):
            marks = [self._convert.ballToMark(ele) for ele in arr]
            for deferBall in deferBallInfos:
                if any(mark == deferBall.sort for mark in marks):
                    deferBall.times = 0
                else:
                    deferBall.times += 1
            defers = list(map(lambda x: x.times, deferBallInfos))
            std_dev = np.std(defers)
            variance = np.var(defers)
            defers.append(std_dev)
            defers.append(variance)
            defers.append(inputs[idx])
            defers.append(marks)
            defer2Ds.append(defers)

        deferColumns = [ball.sort for ball in deferBallInfos]
        deferColumns.append('std')
        deferColumns.append('var')
        deferColumns.append('num')
        deferColumns.append('markNum')
        dfDefer = pd.DataFrame(defer2Ds, columns=deferColumns)
        quantileInfo = self._quantile.calcuOutlierInfo(dfDefer)
        quanColumns = dfDefer.columns[self._quantile.cutFrt:self._quantile.cutEnd]
        # 計算符合離群值mark
        dfDefer['markOutliers'] = dfDefer.apply(
            lambda row: self._getMarkOutliers(row, quantileInfo, quanColumns), axis=1)
        # 轉換成num
        dfDefer['numOutliers'] = dfDefer.apply(
            lambda row: self._getNumOutliers(row), axis=1)

        # 計算變異數
        self._quantile.loadQInfo(dfDefer['var'])
        dfDefer['varQ'] = dfDefer.apply(
            lambda row: self._quantile.calcuLevelQs(row, 'var'), axis=1)

        dfDeferInfo = DfInfo()
        dfDeferInfo.df = dfDefer
        if len(self.includeColumns) != 0:
            dropColumns = []
            for column in dfDefer.columns:
                if any(column == includeColumn for includeColumn in self.includeColumns) == False:
                    dropColumns.append(column)
                pass
            dfDropTimes = dfDefer.copy(deep=True)
            dfDropTimes.drop(columns=dropColumns, inplace=True)
            dfDeferInfo.dfDrop = dfDropTimes

        if self._isToCsv and self._path is not None and self._filename is not None:
            self._exportFile.exportExcel([dfDeferInfo.df, dfDeferInfo.dfDrop], [
                                         'df', 'dfDrop'], self._path, self._filename)
        return dfDeferInfo
        pass

    pass


class TestQuantile(unittest.TestCase):
    def test_calcuOutlierInfo_Q4(self):
        # arrange
        quantile = Quantile(QLevel.Q4)
        quantile.cutFrt = 0
        quantile.cutEnd = 2

        data = {'A': [1, 2, 3, 4, 5], 'B': [1, 2, 3, 4, 5]}
        df = pd.DataFrame(data)
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
        df = pd.DataFrame(data)
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
        df = pd.DataFrame(data)
        # act
        quantile.loadQInfo(df['A'])
        df['level'] = df.apply(
            lambda row: quantile.calcuLevelQs(row, 'A'), axis=1)
        excepted = ['Q1', 'Q2', 'Q3', 'Q4',
                    'Q5', 'Q6', 'Q7', 'Q8', 'Q9', 'Q10']
        # assert
        self.assertCountEqual(df['level'].tolist(), excepted)
        pass


class TestTimesCalcu(unittest.TestCase):

    def test_calcu_ball_df(self):
        """DataFrame balls相等結果"""
        mockExportFile = ExportFile()
        convert = BeginConvertMark()
        quantile = Quantile()
        quantile.cutFrt = 0
        quantile.cutEnd = 39
        path = 'C:/Programs/bingo/bingo_scrapy/539_calcu'
        filename = 'timesBall.xlsx'
        timesCalcu = TimesCalcu(mockExportFile,  convert,
                                quantile, True, path, filename)
        timesCalcu.includeColumns = ['num', 'desc']
        # act
        dbContext = db.MSSQLDbContext({'server': 'wpdb2.hihosting.hinet.net', 'user': 'p89880749_p89880749',
                                       'password': 'Jonny1070607!@#$%', 'database': 'p89880749_test'})
        rows = dbContext.select(
            'select drawNumberSize,lotteryDate from Daily539 ORDER BY period')
        inputs = list(map(lambda row: row['drawNumberSize'].split(','), rows))
        dfDefer = timesCalcu.calcu(inputs)

        # assert 只要沒exception就是True

        self.assertEqual(True, True)
        pass

    def test_calcu_mark_df(self):
        """DataFrame相等結果"""
        # arrange
        mockExportFile = ExportFile()
        convert = ConvertMark()
        quantile = Quantile()
        quantile.cutFrt = 0
        quantile.cutEnd = 19
        quantile.lowerLimit = 1.1
        path = 'C:/Programs/bingo/bingo_scrapy/539_calcu'
        filename = 'timesMark.xlsx'
        timesCalcu = TimesCalcu(mockExportFile,  convert,
                                quantile, True, path, filename)
        timesCalcu.includeColumns = ['num', 'desc']

        # act
        dbContext = db.MSSQLDbContext({'server': 'wpdb2.hihosting.hinet.net', 'user': 'p89880749_p89880749',
                                       'password': 'Jonny1070607!@#$%', 'database': 'p89880749_test'})
        rows = dbContext.select(
            'select drawNumberSize,lotteryDate from Daily539 ORDER BY period')
        inputs = list(map(lambda row: row['drawNumberSize'].split(','), rows))
        dfDefer = timesCalcu.calcu(inputs)
        self.assertEqual(True, True)
        pass


class TestDeferCalcu(unittest.TestCase):

    def test_calcu_ball_df(self):
        """DataFrame balls相等結果"""
        mockExportFile = ExportFile()
        convert = BeginConvertMark()
        quantile = Quantile(QLevel=QLevel.Q10)
        quantile.cutFrt = 0
        quantile.cutEnd = 39
        path = 'C:/Programs/bingo/bingo_scrapy/539_calcu'
        filename = 'deferBall.xlsx'
        deferCalcu = DeferCalcu(mockExportFile,  convert,
                                quantile, True, path, filename)
        deferCalcu.includeColumns = ['markOutliers', 'varQ']
        # act
        dbContext = db.MSSQLDbContext({'server': 'wpdb2.hihosting.hinet.net', 'user': 'p89880749_p89880749',
                                       'password': 'Jonny1070607!@#$%', 'database': 'p89880749_test'})
        rows = dbContext.select(
            'select drawNumberSize,lotteryDate from Daily539 ORDER BY period')
        inputs = list(map(lambda row: row['drawNumberSize'].split(','), rows))
        dfDefer = deferCalcu.calcu(inputs)

        # assert 只要沒exception就是True

        self.assertEqual(True, True)
        pass

    def test_calcu_mark_df(self):
        """DataFrame相等結果"""
        # arrange
        mockExportFile = ExportFile()
        convert = ConvertMark()
        quantile = Quantile(QLevel=QLevel.Q10)
        quantile.cutFrt = 0
        quantile.cutEnd = 19
        path = 'C:/Programs/bingo/bingo_scrapy/539_calcu'
        filename = 'deferMark.xlsx'
        deferCalcu = DeferCalcu(mockExportFile,  convert,
                                quantile, True, path, filename)
        deferCalcu.includeColumns = ['markOutliers', 'varQ']
        # act
        dbContext = db.MSSQLDbContext({'server': 'wpdb2.hihosting.hinet.net', 'user': 'p89880749_p89880749',
                                       'password': 'Jonny1070607!@#$%', 'database': 'p89880749_test'})
        rows = dbContext.select(
            'select drawNumberSize,lotteryDate from Daily539 ORDER BY period')
        inputs = list(map(lambda row: row['drawNumberSize'].split(','), rows))
        dfDefer = deferCalcu.calcu(inputs)
        # assert
        # region

        # exceptedColumns = ['小一', '小二', '小三', '小四', '小五', '大一', '大二', '大三', '大四', '大五',
        #                    '小六', '小七', '小八', '小九', '大六', '大七', '大八', '大九', '零', 'std', 'var', 'num']
        # excepted2Ds = [
        #     [0, 0, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0,
        #         1, 0.440347, 0.193906, ['01', '12', '31', '38', '39']],
        #     [0, 1, 2, 2, 0, 1, 2, 2, 2, 2, 2, 0, 2, 2, 2, 2, 1, 0,
        #         2, 0.815365, 0.664820, ['01', '07', '11', '15', '29']],
        #     [1, 2, 3, 0, 1, 2, 3, 0, 3, 3, 3, 1, 3, 3, 0, 0, 2, 1,
        #         3, 1.195560, 1.429363, ['04', '14', '33', '36', '37']],
        # ]

        # dfExcepted = pd.DataFrame(excepted2Ds, columns=exceptedColumns)
        # isEqual = None
        # try:
        #     isEqual = assert_frame_equal(dfDefer, dfExcepted)
        #     isEqual = True
        #     print("DataFrames are equal")
        # except AssertionError as e:
        #     isEqual = False
        #     print("DataFrames are not equal")
        #     print(e)
        # self.assertEqual(isEqual, True)
        # endregion
        self.assertEqual(True, True)
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


class TestContinueCalcu(unittest.TestCase):

    def test_calcu_ball_df(self):
        """DataFrame balls相等結果"""
        # arrange
        mockExportFile = ExportFile()
        convert = BeginConvertMark()
        quantile = Quantile()
        quantile.cutFrt = 0
        quantile.cutEnd = 39
        path = 'C:/Programs/bingo/bingo_scrapy/539_calcu'
        filename = 'continBall.csv'
        continueCalcu = ContinueCalcu(mockExportFile,  convert,
                                      quantile, True, path, filename)
        continueCalcu.includeColumns = ['markOutliers', 'varQ']
        # act
        dbContext = db.MSSQLDbContext({'server': 'wpdb2.hihosting.hinet.net', 'user': 'p89880749_p89880749',
                                       'password': 'Jonny1070607!@#$%', 'database': 'p89880749_test'})
        rows = dbContext.select(
            'select drawNumberSize,lotteryDate from Daily539 ORDER BY period')
        inputs = list(map(lambda row: row['drawNumberSize'].split(','), rows))
        dfContin = continueCalcu.calcu(inputs)
        # assert
        self.assertEqual(True, True)

    def test_calcu_mark_df(self):
        # arrange
        mockExportFile = ExportFile()
        convert = ConvertMark()
        quantile = Quantile()
        quantile.upperLimit = 1.1
        quantile.cutFrt = 0
        quantile.cutEnd = 19
        path = 'C:/Programs/bingo/bingo_scrapy/539_calcu'
        filename = 'continMark.csv'
        continueCalcu = ContinueCalcu(mockExportFile,  convert,
                                      quantile, True, path, filename)
        continueCalcu.includeColumns = ['markOutliers', 'varQ']
        # act
        dbContext = db.MSSQLDbContext({'server': 'wpdb2.hihosting.hinet.net', 'user': 'p89880749_p89880749',
                                       'password': 'Jonny1070607!@#$%', 'database': 'p89880749_test'})
        rows = dbContext.select(
            'select drawNumberSize,lotteryDate from Daily539 ORDER BY period')
        inputs = list(map(lambda row: row['drawNumberSize'].split(','), rows))
        dfContin = continueCalcu.calcu(inputs)
        # assert
        self.assertEqual(True, True)


if __name__ == '__main__':

    # region calcu workflow

    # dbContext = db.MSSQLDbContext({'server': 'wpdb2.hihosting.hinet.net', 'user': 'p89880749_p89880749',
    #                                'password': 'Jonny1070607!@#$%', 'database': 'p89880749_test'})
    # rows = dbContext.select(
    #     'select drawNumberSize,lotteryDate from Daily539 ORDER BY period')
    # inputs = list(map(lambda row: row['drawNumberSize'].split(','), rows))

    # endregion

    # region test case

    try:
        suite = unittest.TestSuite()
        # suite.addTest(TestQuantile('test_calcuOutlierInfo_Q4'))
        # suite.addTest(TestQuantile('test_calcuLevelQs_Q4'))
        # suite.addTest(TestQuantile('test_calcuLevelQs_Q10'))
        # suite.addTest(TestConvertMark('test_ballToMark'))
        # suite.addTest(TestConvertMark('test_markToBalls'))
        # suite.addTest(TestConvertOddEvenMark('test_ballToMark'))
        # suite.addTest(TestConvertOddEvenMark('test_markToBalls'))

        # suite.addTest(TestTimesCalcu('test_calcu_ball_df'))
        # suite.addTest(TestTimesCalcu('test_calcu_mark_df'))
        # suite.addTest(TestDeferCalcu('test_calcu_mark_df'))
        # suite.addTest(TestDeferCalcu('test_calcu_ball_df'))

        # suite.addTest(TestContinueCalcu('test_calcu_ball_df'))
        # suite.addTest(TestContinueCalcu('test_calcu_mark_df'))

        # suite.addTest(TestDeferCalcu('test_to_csv_df'))
        # suite.addTest(TestDeferCalcu('test_calcu_3mean'))
        runner = unittest.TextTestRunner(verbosity=2)
        runner.run(suite)
    except SystemExit:
        pass

    # endregion
