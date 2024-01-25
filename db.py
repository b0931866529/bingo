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
from datetime import datetime




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

    # region 暫時不用先remark

    # def Insert_BulkWrite(self, DBCollection, BulkRequests):
    #     collection = self.__mongoDB[DBCollection]

    #     # 事務開始
    #     insert_session = self.__client.start_session(causal_consistency=True)
    #     try:
    #         insert_session.start_transaction()
    #         # BulkWrite 支持混合寫入操作（插入、刪除和更新），而 insertMany，如其名稱所示，僅插入文檔。
    #         collection.bulk_write(requests=BulkRequests,
    #                               session=insert_session)
    #     except Exception as e:              # 例外
    #         self.setErr(e)
    #     else:
    #         insert_session.commit_transaction()
    #     finally:
    #         insert_session.end_session()
    # def Count(self, DBCollection, DBQuery):
    #     collection = self.__mongoDB[DBCollection]
    #     return collection.count_documents(DBQuery)

    # def Update(self, DBCollection, DBQuery, DBData):
    #     collection = self.__mongoDB[DBCollection]
    #     try:
    #         update_result = collection.update_many(DBQuery, DBData)
    #     except Exception as e:              # 例外
    #         self.setErr(sys.exc_info()[0])
    #     else:                               # 成功
    #         print("更新筆數:", update_result.modified_count)
    # def DeleteCollection(self, DBCollection):
    #     collection = self.__mongoDB[DBCollection]
    #     collection.drop()
    # endregion


# 模組測試
if __name__ == '__main__':

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

    #將資料轉成日期格式
    #設定日期>型態


    # 宣告資料庫
    db = MongoDbContext("localhost", "LotteryTicket")
    table = "Bingo"

    print("")
    queryKey = {'dDate': {'$gte': datetime(2024, 1, 1)}}
    db.Delete(table, queryKey)

    # region read csv insert db
    currDir = os.path.dirname(os.path.abspath(__file__))
    file = os.path.join(currDir, 'bingo_scrapy', 'bingo_scrapy', 'bingo.csv')
    with open(file, 'r') as f:
        reader = csv.DictReader(f)
        data = []
        for obj in reader:
            newObj = {}
            for key,value in obj.items():
                if key == 'dDate':
                    date_string = obj[key].split('T')[0]
                    date = datetime.strptime(date_string, "%Y-%m-%d")
                    newObj[key] = date
                else:
                    newObj[key] = value
            data.append(newObj)
    db.Insert(table, data)
    # endregion

    # region test用剛剛寫入_id查詢數據
    results = db.Find(table, queryKey)
    # result還算是有db型態list,但若遍歷直接就是字典元素
    twoDatas = []
    for obj in results:
        arr = obj['bigShowOrder'].split(',')
        twoDatas.append(arr)
    # endregion
print("")