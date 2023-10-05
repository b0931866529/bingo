# -*- coding:utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import json
import db
import bingoStatistics
from itertools import combinations
from bson import ObjectId
from datetime import datetime

# driver = webdriver.Chrome("./chromedriver")
driver = webdriver.Chrome("C:/Programs/works/Test/chromedriver.exe")


def print_dict(par_dict):
    print(json.dumps(par_dict, indent=4))


# 存放抓取號碼
bingo_no = {}


def bingo():
    global bingo_no

    # 開啟頁面
    driver.get("https://www.taiwanlottery.com.tw/lotto/bingobingo/drawing.aspx")

    # 取得頁面 title
    title = driver.title
    print("title:", title)
    driver.implicitly_wait(30)
    time.sleep(3)

    # 按鈕【顯示當日所有期數】
    submit_button = driver.find_element(by=By.ID, value="Button1")
    submit_button.click()
    # time.sleep( 3)

    len_title = len("112001219")
    len_no = len("01 03 07 10 11 17 18 20 23 31 35 42 45 50 52 55 57 70 76 79")

    t_title = ""
    for e in driver.find_elements(by=By.CLASS_NAME, value="tdA_3"):
        t = e.text
        if len(t) == len_title:
            t_title = t
        if len(t) == len_no:
            if t_title != "":
                bingo_no[t_title] = t.replace(" ", ",")

    for e in driver.find_elements(by=By.CLASS_NAME, value="tdA_4"):
        t = e.text
        if len(t) == len_title:
            t_title = t
        if len(t) == len_no:
            if t_title != "":
                bingo_no[t_title] = t.replace(" ", ",")

    bingo_no = dict(sorted(bingo_no.items()))

    time.sleep(3)
    driver.quit()


def mapBingo(dict: {}):

    return ''


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

    bingoStatistics = bingoStatistics.BingoStatistics(calcuBingo)
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
