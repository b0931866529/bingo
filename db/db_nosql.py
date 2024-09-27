# -*- coding:utf-8 -*-
from abc import ABC, abstractmethod
import csv
import os
import traceback
from bson import ObjectId
import pymongo
import sys
import logging
from pymongo import InsertOne, DeleteOne, ReplaceOne
from datetime import date, datetime
import pymssql

# from bingo_scrapy.bingo_scrapy.spiders import bingo


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

    # def Update(self, DBCollection, DBQuery, DBData):
    #     print("未定義 IDbContext.Update(...)")


class MongoDbContext(IDbContext):
    __client = None
    __mongoDB = None
    __err = "沒有錯誤"

    # Windows驗證
    def __init__(self, DBIP, DBName):
        DBStr = "mongodb://" + DBIP + ":27017/"
        # print( "資料庫(DBStr):", DBStr)

        self.__client = pymongo.MongoClient(DBStr)
        self.__mongoDB = self.__client[DBName]

    # AP混和驗證
    @classmethod  # 因為 python 無法定義多個 __init__(), 故使用可選建構式
    def AP(cls, DBIP, DBID, DBPW, DBName):
        print("已經定義 IDbContext.AP( DBIP, DBID, DBPW, DBName)")
        return cls(DBIP, DBName)

    def getCollection(self, DBCollection):
        return self.__mongoDB[DBCollection]

    # 統一用批量插入

    def Insert(self, DBCollection, DBData: []):
        collection = self.__mongoDB[DBCollection]
        insert_result = collection.insert_many(DBData)
        print(len(insert_result.inserted_ids))
        # collection = self.__mongoDB[DBCollection]
        # insert_session = self.__client.start_session(causal_consistency=True)
        # try:
        #     insert_session.start_transaction()
        #     insert_result = collection.insert_many(
        #         DBData, session=insert_session)
        #     insert_session.commit_transaction()
        #     # 補齊寫入資訊
        # except Exception as e:              # 例外
        #     insert_session.abort_transaction()
        #     # 補齊錯誤資訊
        #     self.setErr(e)
        # finally:
        #     insert_session.end_session()
        pass

    def Find(self, DBCollection, DBQuery={}):
        collection = self.__mongoDB[DBCollection]
        find_result = {}
        try:
            find_result = collection.find(DBQuery)
            print("查詢筆數:", find_result.count())
        except Exception as e:              # 例外
            self.setErr(sys.exc_info()[0])
        finally:
            return find_result

    def Delete(self, DBCollection, DBQuery):
        collection = self.__mongoDB[DBCollection]
        try:
            delete_result = collection.delete_many(DBQuery)
            print("刪除筆數:", delete_result.deleted_count)
        except Exception as e:              # 例外
            self.setErr(e)


# 模組測試
if __name__ == '__main__':

    DBStr = "mongodb://localhost:27017/"
    # print( "資料庫(DBStr):", DBStr)

    client = pymongo.MongoClient(DBStr)

    # Create database and collection

    # region stragey
    # endregion

    # region bingo insert data
    db = client['bingo']
    bingo_collection = db['bingo']
    bingo_data = {
        "Name": "202409_三星週期打法",
        "TradeDate": datetime(2024, 9, 16),
        "Describe": "先領完上次的錢發現輸不多，開始不斷用三星沒有上倍數去拚，有設定鬧鐘定期換牌，中了幾個周期下來收尾",
        "Profit": 2000,
        "FeedBack1": "遵守不連期規則、定期換牌、周期跑到就走，不以賺小而放棄。",
    }
    # bingo_collection.insert_one(bingo_data)
    # bingo_collection.update_one({"Name": "202409_四星打法"}, {
    #                             "$set": {"TradeDate": datetime(2024, 9, 15)}})
    # queryKey = {'Name': '202409_四星打法'}
    queryKey = {}
    results = bingo_collection.find(queryKey)

    for result in results:
        print("")
    # endregion

    #
    # region option Insert data
    # db = client['trade']
    # trade_collection = db['option']
    # # trade_data = {
    # #     "Name": "22100_put_0904",
    # #     "Qty": "1",
    # #     "TradeDate": datetime(2024, 9, 23, 8, 50),
    # #     "Describe": "已經開盤看其沒有漲很多，並且有點萎縮感，想到日圓升值和以黎，感覺會再崩一次但不肯定時機，看了一下最接近履約成本價很低，120左右，再往下一個檻大概90因此就購買",
    # #     "Cost": 4500,
    # #     "Profit": 2000,
    # # }
    # # trade_collection.insert_one(trade_data)
    # name_value = "22100_put_0904"
    # results = trade_collection.find({"Name": name_value})

    # for result in results:
    #     print("")
    # endregion

    # List all databases
    # for db_name in client.list_database_names():
    #     if not db_name == 'admin':
    #         client.drop_database(db_name)
    # dbs = client.list_database_names()
    print("")

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

    # endregion
    print("")
    pass
