# -*- coding:utf-8 -*-
import traceback
from bson import ObjectId
import pymongo
import sys, logging
from pymongo import InsertOne, DeleteOne, ReplaceOne

class IDbContext:
    def Err(self):                      # 若執行SQL錯誤訊息從此取得
        print( "未定義 IDbContext.Err(...)")

    def Insert(self, DBCollection, DBData):
        print( "未定義 IDbContext.Insert(...)")

    def Find(self, DBCollection, DBQuery):
        print( "未定義 IDbContext.Find(...)")

    def Update(self, DBCollection, DBQuery, DBData):
        print( "未定義 IDbContext.Update(...)")

    def Delete(self, DBCollection, DBQuery):
        print( "未定義 IDbContext.Delete(...)")

class MongoDbContext(IDbContext):
    __client = None
    __mongoDB = None
    __err = "沒有錯誤"

    def setErr(self, errMsg):
        self.__err = traceback.format_exc( )
        logging.error( self.__err)

    def Err(self):
        return self.__err

    # Windows驗證
    def __init__(self, DBIP, DBName):
        DBStr = "mongodb://" + DBIP + ":27017/"
        # print( "資料庫(DBStr):", DBStr)

        self.__client = pymongo.MongoClient( DBStr)
        self.__mongoDB = self.__client[ DBName]

    # AP混和驗證
    @classmethod  # 因為 python 無法定義多個 __init__(), 故使用可選建構式
    def AP(cls, DBIP, DBID, DBPW, DBName):
        print( "已經定義 IDbContext.AP( DBIP, DBID, DBPW, DBName)")
        return cls( DBIP, DBName)

    # 批量插入
    def Insert(self, DBCollection,DBData):
        # 判斷如果是空的 List 就什麼都不做
        # db_size = len( DBData)
        # if db_size < 1:
        #     print( "插入筆數:", db_size)
        #     return

        collection = self.__mongoDB[ DBCollection]
        insert_result = collection.insert_one(DBData)
        return insert_result.inserted_id
        # insert_session = self.__client.start_session( causal_consistency=True)
        # try:
        #     insert_session.start_transaction( )
        #     insert_result = collection.insert_one( DBData, session=insert_session)
        #     # insert_result = collection.insert_many( DBData, session=insert_session)
        # except Exception as e:              # 例外
        #     insert_session.abort_transaction()
        #     self.setErr( e)
        # else:                               # 成功
        #     print( "插入筆數:", len( insert_result.inserted_ids))
        #     insert_session.commit_transaction( )
        # finally:
        #     insert_session.end_session( )

    def Insert_BulkWrite(self, DBCollection, BulkRequests):
        collection = self.__mongoDB[ DBCollection]

        # 事務開始
        insert_session = self.__client.start_session( causal_consistency=True)
        try:
            insert_session.start_transaction( )
            # BulkWrite 支持混合寫入操作（插入、刪除和更新），而 insertMany，如其名稱所示，僅插入文檔。
            collection.bulk_write( requests=BulkRequests, session=insert_session)
        except Exception as e:              # 例外
            self.setErr( e)
        else:
            insert_session.commit_transaction()
        finally:
            insert_session.end_session()


    def Find(self, DBCollection, DBQuery={}):
        collection = self.__mongoDB[ DBCollection]
        find_result = {}
        try:
            find_result = collection.find( DBQuery)
        except Exception as e:              # 例外
            self.setErr( sys.exc_info()[0])
        else:                               # 成功
            pass
        finally:
            return find_result

    def Count(self, DBCollection, DBQuery):
        collection = self.__mongoDB[ DBCollection]
        return collection.count_documents( DBQuery)

    def Update(self, DBCollection, DBQuery, DBData):
        collection = self.__mongoDB[ DBCollection]
        try:
            update_result = collection.update_many( DBQuery, DBData)
        except Exception as e:              # 例外
            self.setErr( sys.exc_info()[0])
        else:                               # 成功
            print( "更新筆數:", update_result.modified_count)

    def Delete(self, DBCollection, DBQuery):
        collection = self.__mongoDB[ DBCollection]
        try:
            delete_result = collection.delete_many( DBQuery)
        except Exception as e:              # 例外
            self.setErr( e)
        else:                               # 成功
            print( "刪除筆數:", delete_result.deleted_count)

    def DeleteCollection(self, DBCollection):
        collection = self.__mongoDB[ DBCollection]
        collection.drop()

# 模組測試
if __name__ == '__main__':

    # 準備日誌
    LogFile = "convert.log"
    logging.basicConfig(
        filename=LogFile,
        encoding='utf-8',
        level=logging.DEBUG,
        format='%(asctime)s [%(levelname)s]: %(message)s',
        datefmt='%Y/%m/%d %I:%M:%S',
    )
    with open(LogFile, 'w'):  # 清除日誌內容
        pass

    # 宣告資料庫
    db = MongoDbContext( "localhost", "testDb")
    table = "test"
    # queryKey = {'_id': ObjectId("64efc7c3cbe4c926355f0b66")}

    #region test寫入數據
    insert = {"112050345": "01,02,06,09,13,14,16,19,29,34,35,36,39,48,52,56,62,72,73,79",
    "112050346": "01,02,06,09,13,14,16,19,29,34,35,36,39,48,52,56,62,72,73,79"}
    _id = db.Insert( "test", insert)
    #endregion

    #region test用剛剛寫入_id查詢數據
    # queryKey = {'price':36}
    # queryKey = {'_id':ObjectId("631329283bac07676f9a2f84")}
    queryKey = {'_id':_id}
    result = db.Find("test",queryKey)
    for bingo in result:
        for key,value in bingo.items():
            print(key,value)
    #endregion



    # insert_list = [
    #     { "_id": 4, "Term": 4,   "Left": "left", "Middle": "middle", "Right": "right" },
    #     { "_id": 2, "Term": 2,   "Left": "left", "Middle": "middle", "Right": "right" },
    #     { "_id": 6, "Term": 6, "Left": "left", "Middle": "middle", "Right": "right"},
    # ]
    # db.Insert( "test_coll", insert_list)

    # 插入數據(只要【有1筆】插入失敗，就全部失敗)
    # bulk_requests = [
    #     InsertOne( { "_id": 4, "Term": 2,   "Left": "left", "Middle": "middle", "Right": "right" }),
    #     InsertOne( { "_id": 2, "Term": 2,   "Left": "left", "Middle": "middle", "Right": "right" }),
    #     InsertOne( { "_id": 6, "Term": 2, "Left": "left", "Middle": "middle", "Right": "right"}),
    # ]
    # db.Insert_BulkWrite( "test_coll", bulk_requests)

    # 搜尋資料
    # find_result = db.Find( "test_coll", { ""})                        # 失败测试
    # find_result = db.Find( "test_coll", { "Term": 0, "Left": "left"}) # 成功测试
    # for r in find_result:
    #     print( r)

    # 更新資料
    # update_values = { "$set": { "Left": "left0"}}
    # db.Update( "test_coll", { ""},                        update_values) # 失败测试
    # db.Update( "test_coll", { "Term": 0, "Left": "left"}, update_values) # 成功测试

    # 刪除資料
    # delete_result = db.Delete( "test_coll", { "Term"})    # 失败测试
    # delete_result = db.Delete( "test_coll", { "Term": 4}) # 成功测试

    # print( "db.Err():", db.Err())
    print( 'end')
