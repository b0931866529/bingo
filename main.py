# -*- coding:utf-8 -*-
from selenium import webdriver

import time
import json
import db
import bingoStatistics
from itertools import combinations
from bson import ObjectId
from datetime import datetime
from selenium.webdriver.common.by import By


# 整合計算來源演算法進行回朔test
if __name__ == '__main__':
    # region 來源從網站
    # bingo()
    # dbContext = db.MongoDbContext("localhost", "testDb")
    # table = "test"
    # currentDate = datetime.now()
    # bingo_no['currentDate'] = currentDate
    # _id = dbContext.Insert(table, bingo_no)
    # queryKey = {'_id': _id}
    # result = dbContext.Find(table, queryKey)
    # bingo = result[0]
    # endregion

    # region 來源網站已經寫入DB從DB
    dbContext = db.MongoDbContext("localhost", "testDb")
    table = "test"
    # 此處GUID值自行抽換
    queryKey = {'_id': ObjectId("650ab98f43f4ffce3f8136eb")}
    result = dbContext.Find(table, queryKey)
    bingo = result[0]
    # endregion
    print('')
    # region 將bingo => term,ball 型別

    # example:calcuBingo = [
    #     {'term':'1','balls':[1,2,9,11,12,13,15,18,23,25,30,32,35,36,48,53,59,61,67,80,15]},
    #     {'term':'2','balls':[1,2,3,6,9,11,12,14,22,26,28,33,40,43,44,45,49,50,54,69,49]},
    #     {'term':'3','balls':[10,13,31,38,43,47,48,49,52,53,56,60,64,66,72,73,76,77,79,80,77]},
    # ]
    del bingo['_id']
    del bingo['currentDate']
    intKeys = map(lambda r: int(r), bingo)
    term = min(intKeys) - 1
    i = 1
    calcuBingo = []
    for key, value in bingo.items():
        strBalls = value.split(',')
        balls = list(map(lambda r: int(r), strBalls))
        ball = {'term': i, 'balls': balls}
        calcuBingo.append(ball)
        i = i + 1
    # calcuBingo = list(map(mapBingo,bingo))

    # endregion
    mapBingoLen = len(calcuBingo)
    strategyBingos = list(filter(lambda r: int(r['term']) < 100, calcuBingo))
    actualBingos = list(filter(lambda r: int(r['term']) >= 100, calcuBingo))

    bingoStatistics = bingoStatistics.BingoStatistics(strategyBingos)
    numbers = list(range(1, 80))  # 生成 1 到 80 的数字列表
    # 在目前數之中生成4數字為一組不重複組合
    combinations_array = list(combinations(numbers, 3))
    arrInput = list(map(lambda r: list(r), combinations_array))
    arrResult = []
    for item in arrInput:
        result = bingoStatistics.calcu(item)
        arrResult.append(result)
    arrEffect = list(filter(lambda r: r['support'] != 0, arrResult))
    arrApprove = list(
        filter(lambda r: r['support'] > 0.05 and r['maxValue'] < 20, arrEffect))

    for item in arrEffect:
        print(item)
