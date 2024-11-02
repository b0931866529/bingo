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

# test

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


# 模組測試
if __name__ == '__main__':

    # region MS-MSSQLDbContext

    # 研究怎用逗號分行

    sql = MSSQLDbContext({'server': 'wpdb2.hihosting.hinet.net', 'user': 'p89880749_p89880749',
                          'password': 'Jonny1070607!@#$%', 'database': 'p89880749_test'})
    # value = {}

    # value['drawTerm'] = 113009421
    # value['dDate'] = date(2024, 2, 25)
    # value['bigShowOrder'] = "04,08,18,19,23,25,29,31,33,36,38,42,43,46,49,57,60,76,78,80"
    # value['createDate'] = 'CURRENT_TIMESTAMP'
    # # value['createDate'] = datetime.now()
    # data = [value]
    # err = sql.insert('Bingo', data)
    # print(err)

    # bingo
    # #  rows = sql.select('select * from Bingo where dDate != \'2024-02-16\'')
    # rows = sql.select('select * from Bingo ORDER BY drawTerm DESC ')
    # for row in rows:
    #     print(row['bigShowOrder'])

    # 539

    tables = sql.select('SELECT table_name \
                      FROM information_schema.tables ')

    rows = sql.select('select * from Daily539')

    print('')

    # 增加刪除和tran commit

    # endregion
    pass


# 原始資料
# |drawTerm|bigShowOrder|
# 表頭
# |drawTerm|algorithmName|amt|createdTime|
# 表身
# |drawTerm|nums|matches|double|amt|createdTime|
