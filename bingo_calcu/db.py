# -*- coding:utf-8 -*-
from abc import ABC, abstractmethod
import csv
import os
import traceback
from typing import List
from bson import ObjectId
import pymongo
import sys
import logging
from pymongo import InsertOne, DeleteOne, ReplaceOne
from datetime import date, datetime
import pymssql
import unittest


class BingoProfitInfo:
    """
    單期簽注資訊(內含有多期)
    """

    def __init__(self):
        """利潤"""
        self.amt: int = 0
        """期數"""
        self.drawTerm: int = 0
        """算法名稱"""
        self.algorithmName: str = ''
        """單注簽注"""
        self.bingoInfos: List[BingoInfo] = []

    def __eq__(self, other):
        if not isinstance(other, BingoProfitInfo):
            return False
        return self.amt == other.amt and set(self.bingoInfos) == set(other.bingoInfos)

    def __hash__(self) -> int:
        return hash((self.amt, tuple(set(self.bingoInfos))))


class BingoInfo:
    """
    單注簽注資訊
    """

    def __init__(self):
        self._double: int = 1
        self._cost: int = 25
        self._amt: int = 0
        self._isDouble: bool = True
        self._nums: List[str] = []
        self._matchs: List[str] = []

    @property
    def double(self) -> int:
        return self._double

    @property
    def cost(self) -> int:
        return self._cost

    @double.setter
    def double(self, value: int):
        """設定是否加倍，連帶設定成本"""
        self._double = value
        self._cost = 25 * value

    @property
    def amt(self) -> int:
        """取得獎金"""
        return self._amt

    @amt.setter
    def amt(self, value: int):
        """設定獎金"""
        self._amt = value

    @property
    def nums(self) -> List[str]:
        """取得簽注球號"""
        return self._nums

    @nums.setter
    def nums(self, value: List[str]):
        """設定簽注球號"""
        self._nums = value

    @property
    def matchs(self) -> List[str]:
        """取得中獎球號"""
        return self._matchs

    @matchs.setter
    def matchs(self, value: List[str]):
        """設定中獎球號"""
        self._matchs = value

    @property
    def isDouble(self) -> bool:
        """取得台彩是否加倍"""
        return self._isDouble

    @isDouble.setter
    def isDouble(self, value: bool):
        """設定台彩是否加倍"""
        self._isDouble = value

    def __eq__(self, other):
        if not isinstance(other, BingoInfo):
            return False
        numSetQty = len(set(self.nums + other.nums))
        matchSetQty = len(set(self.matchs + other.matchs))
        isNumEqual = numSetQty == len(self.nums) and len(
            self.nums) == len(other.nums)
        isMatchEqual = matchSetQty == len(self.matchs) and len(
            self.matchs) == len(other.matchs)
        return (self.double == other.double and
                self.cost == other.cost and
                self.amt == other.amt and
                self.isDouble == other.isDouble and
                isNumEqual and isMatchEqual)

    def __hash__(self) -> int:
        return hash((self._double, self._cost, self._amt, self._isDouble, tuple(set(self._nums)), tuple(set(self._matchs))))


class IDbContext(ABC):

    @property
    def err(self):
        return self.__err

    @err.setter
    def err(self, value):
        self.__err = value

    def __init__(self):
        self.__err = ''

    @abstractmethod
    def getCollection(self, DBCollection):
        pass

    @abstractmethod
    def Insert(self, DBCollection, DBData):
        pass

    @abstractmethod
    def Find(self, DBCollection, DBQuery):
        pass

    @abstractmethod
    def Delete(self, DBCollection, DBQuery):
        pass


class MSSQLDbContext:
    def __init__(self, db_setting):
        self.conn = pymssql.connect(
            server=db_setting['server'], user=db_setting['user'], password=db_setting['password'], database=db_setting['database'])
        # self.conn = pymssql.connect(
        #     host=db_setting['host'],
        #     database=db_setting['database'],
        #     as_dict=True
        # )
        self.cur = self.conn.cursor(as_dict=True)

    def select(self, sql):
        self.cur.execute(sql)
        return self.cur.fetchall()

    def delete(self, sql):
        try:
            self.cur.execute(sql)
            self.conn.commit()
            return ''
        except Exception as e:
            return e

    def insert(self, table, datas):
        sql = ''
        for data in datas:
            sql += self.getInsertSQL(table, data)

        try:
            self.cur.execute(sql)
            self.conn.commit()
            return ''
        except Exception as e:
            return e

    def getInsertSQL(self, table, data):
        tableKey = '('
        tableValue = '('
        for key, value in data.items():
            tableKey += key+','

            if value == "CURRENT_TIMESTAMP":
                tableValue += value+","
            elif type(value) == int:
                tableValue += str(value)+","
            elif type(value) == datetime or type(value) == date:
                tableValue += "'"+str(value)+"',"
            else:
                tableValue += "'"+value+"',"

        tableKey += ')'
        tableValue += ')'
        tableKey = tableKey.replace(",)", ")")
        tableValue = tableValue.replace(",)", ")")
        sql = "insert into "+table+tableKey+" VALUES"+tableValue
        return sql

    def close(self):
        self.cur.close()
        self.conn.close()


class MapBingoProfitInfoToDb:
    def __init__(self, dbContext: MSSQLDbContext):
        self._dbContext = dbContext
        pass

    def insert(self, bingoProfitInfos: List[BingoProfitInfo]) -> str:
        """回朔運算結果轉成表頭和表身塞入資料庫,retrun 是否err"""
        pass

    def select(self, sql: str) -> List[BingoProfitInfo]:
        """資料庫回朔運算結果轉成結構,錯誤retrun 空列表"""
        pass


class TestMapBingoProfitInfoToDb:
    def __init__(self) -> None:
        self._dbContext = MSSQLDbContext({'server': 'wpdb2.hihosting.hinet.net', 'user': 'p89880749_p89880749',
                                          'password': 'Jonny1070607!@#$%', 'database': 'p89880749_test'})
        self._target = MapBingoProfitInfoToDb(self._dbContext)
        self._lists = [BingoProfitInfo(), BingoProfitInfo()]
        pass

    def test_insert_3head_9detail(self):
        """
        回朔資料連續3期,每期有3筆資料,驗證是否正常塞入資料庫
        """

        # arrange
        # act
        # assert
        pass

    def test_insert_exception(self):
        """
        明細內含有錯誤資料,驗證交易是否正常作動沒有將資料塞入資料庫
        """
        pass

    def test_select_3head_9detail(self):
        """
        資料庫回朔資料連續3期,每期有3筆資料,驗證撈取後是否轉成正確結構
        """
        pass

    def test_select_exception(self):
        """
        撈取SQL有錯誤,驗證是否無丟exception並且return空列表
        """
        pass


# 模組測試
if __name__ == '__main__':

    try:
        suite = unittest.TestSuite()
        # suite.addTest(TestMeanBingo('test_insert_3head_9detail'))
        # suite.addTest(TestMeanBingo('test_insert_exception'))
        # suite.addTest(TestMeanBingo('test_select_3head_9detail'))
        # suite.addTest(TestMapBingoProfitInfoToDb('test_select_exception'))
        runner = unittest.TextTestRunner()
        runner.run(suite)
    except SystemExit as e:
        pass
    # region log sample
    # # 準備日誌
    # LogFile = "convert.log"
    # logging.basicConfig(
    #     filename=LogFile,
    #     encoding='utf-8',
    #     level=logging.DEBUG,
    #     format='%(asctime)s [%(levelname)s]: %(message)s',
    #     datefmt='%Y/%m/%d %I:%M:%S',
    # )
    # with open(LogFile, 'w'):  # 清除日誌內容
    #     pass
    # endregion

    # 將資料轉成日期格式
    # 設定日期>型態

    # region mongodb

    # # 宣告資料庫
    # db = MongoDbContext("localhost", "LotteryTicket")
    # table = "Bingo"

    # print("")
    # queryKey = {'dDate': {'$gte': datetime(2024, 1, 1)}}
    # db.Delete(table, queryKey)

    # # region read csv insert db
    # currDir = os.path.dirname(os.path.abspath(__file__))
    # file = os.path.join(currDir, 'bingo_scrapy', 'bingo_scrapy', 'bingo.csv')
    # with open(file, 'r') as f:
    #     reader = csv.DictReader(f)
    #     data = []
    #     for obj in reader:
    #         newObj = {}
    #         for key, value in obj.items():
    #             if key == 'dDate':
    #                 date_string = obj[key].split('T')[0]
    #                 date = datetime.strptime(date_string, "%Y-%m-%d")
    #                 newObj[key] = date
    #             elif key == 'bigShowOrder':
    #                 newObj[key] = value.split(',')
    #             else:
    #                 newObj[key] = value
    #         data.append(newObj)
    # db.Insert(table, data)
    # # endregion

    # # region test用剛剛寫入_id查詢數據
    # results = db.Find(table, queryKey)
    # # result還算是有db型態list,但若遍歷直接就是字典元素
    # twoDatas = []
    # for obj in results:
    #     twoDatas.append(obj['bigShowOrder'])
    # print(twoDatas)
    # # endregion
    # endregion

    # region MS-MSSQLDbContext

    # 研究怎用逗號分行

    # sql = MSSQLDbContext({'server': 'wpdb2.hihosting.hinet.net', 'user': 'p89880749_p89880749',
    #                       'password': 'Jonny1070607!@#$%', 'database': 'p89880749_test'})
    # value = {}

    # value['drawTerm'] = 113009421
    # value['dDate'] = date(2024, 2, 25)
    # value['bigShowOrder'] = "04,08,18,19,23,25,29,31,33,36,38,42,43,46,49,57,60,76,78,80"
    # value['createDate'] = 'CURRENT_TIMESTAMP'
    # # value['createDate'] = datetime.now()
    # data = [value]
    # err = sql.insert('Bingo', data)
    # print(err)
    # #  rows = sql.select('select * from Bingo where dDate != \'2024-02-16\'')
    # rows = sql.select('select * from Bingo ORDER BY drawTerm DESC ')
    # for row in rows:
    #     print(row['bigShowOrder'])
    # 增加刪除和tran commit

    # endregion
    pass


# 原始資料
# |drawTerm|bigShowOrder|
# 表頭
# |drawTerm|algorithmName|amt|createdTime|
# 表身
# |drawTerm|nums|matches|double|amt|createdTime|
