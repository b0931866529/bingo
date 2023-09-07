# -*- coding:utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.by import By
import time,json
import db
import bingoStatistics
from itertools import combinations
from bson import ObjectId

# driver = webdriver.Chrome("./chromedriver")
driver = webdriver.Chrome("C:/Programs/works/Test/chromedriver.exe")
def print_dict( par_dict):
    print(json.dumps(par_dict, indent=4))

# 存放抓取號碼
bingo_no = { }

def bingo():
    global bingo_no

    # 開啟頁面
    driver.get("https://www.taiwanlottery.com.tw/lotto/bingobingo/drawing.aspx")

    # 取得頁面 title
    title = driver.title
    print( "title:", title)
    driver.implicitly_wait(3)
    time.sleep( 3)

    # 按鈕【顯示當日所有期數】
    submit_button = driver.find_element(by=By.ID, value="Button1")
    submit_button.click( )
    # time.sleep( 3)

    len_title = len( "112001219")
    len_no = len( "01 03 07 10 11 17 18 20 23 31 35 42 45 50 52 55 57 70 76 79")

    t_title = ""
    for e in driver.find_elements(by=By.CLASS_NAME, value="tdA_3"):
        t = e.text
        if len(t) == len_title:
            t_title = t
        if len(t) == len_no:
            if t_title != "":
                bingo_no[t_title] = t.replace( " ", ",")

    for e in driver.find_elements(by=By.CLASS_NAME, value="tdA_4"):
        t = e.text
        if len(t) == len_title:
            t_title = t
        if len(t) == len_no:
            if t_title != "":
                bingo_no[ t_title] = t.replace( " ", ",")

    bingo_no = dict(sorted(bingo_no.items()))

    time.sleep(3)
    driver.quit()

if __name__ == '__main__':
    #region 來源從網站
    # bingo()
    # dbContext = db.MongoDbContext( "localhost", "testDb")
    # table = "test"
    # _id = dbContext.Insert(table, bingo_no)
    # result = dbContext.Find(table,queryKey)
    # bingo = result[0]
    #endregion
    #region 來源網站已經寫入DB從DB
    dbContext = db.MongoDbContext( "localhost", "testDb")
    table = "test"
    #此處GUID值自行抽換
    queryKey = {'_id': ObjectId("64f9484d5ef7ddaeed310413")}
    result = dbContext.Find(table,queryKey)
    bingo = result[0]
    #endregion

    #region 將bingo => term,ball 型別

    # example:calcuBingo = [
    #     {'term':'1','balls':[1,2,9,11,12,13,15,18,23,25,30,32,35,36,48,53,59,61,67,80,15]},
    #     {'term':'2','balls':[1,2,3,6,9,11,12,14,22,26,28,33,40,43,44,45,49,50,54,69,49]},
    #     {'term':'3','balls':[10,13,31,38,43,47,48,49,52,53,56,60,64,66,72,73,76,77,79,80,77]},
    #     {'term':'4','balls':[10,12,16,19,24,26,30,35,41,47,49,54,55,58,59,66,69,75,77,78,30]},
    #     {'term':'5','balls':[20,21,25,28,30,33,35,36,42,43,47,48,61,66,68,69,73,75,76,80,47]},
    #     {'term':'6','balls':[2,9,11,13,16,21,24,31,32,36,38,39,42,45,55,57,63,64,73,79,63]},
    #     {'term':'7','balls':[6,11,16,17,24,25,26,32,43,46,51,59,61,64,65,66,69,71,75,79,32]},
    #     {'term':'8','balls':[1,6,9,10,12,15,24,26,27,29,41,43,51,53,55,65,69,73,77,79,73]},
    #     {'term':'9','balls':[1,2,12,14,22,23,25,29,38,41,46,47,48,50,60,62,70,76,77,80,25]},
    #     {'term':'10','balls':[1,6,11,20,22,24,28,31,40,42,48,56,57,58,60,64,67,69,70,74,28]},
    #     {'term':'11','balls':[6,14,17,18,21,25,27,31,33,35,41,46,48,51,52,53,67,72,79,80,25]},
    #     {'term':'12','balls':[5,13,16,17,20,21,27,28,30,34,39,43,44,46,51,57,58,62,67,70,57]},
    #     {'term':'13','balls':[2,6,6,9,13,15,18,27,30,35,39,43,48,55,58,60,66,67,68,70,18]},
    #     {'term':'14','balls':[2,5,7,8,15,17,41,43,46,47,50,54,57,63,65,68,69,71,72,76,54]},
    #     {'term':'15','balls':[6,11,14,17,19,22,23,38,39,40,44,45,51,53,56,59,64,71,73,74,56]},
    #     {'term':'16','balls':[3,6,14,29,33,34,41,43,47,58,59,62,64,66,68,70,72,74,78,79,6]},
    #     {'term':'17','balls':[1,3,7,13,16,28,29,30,32,38,40,44,45,48,53,66,69,71,74,76,45]},
    #     {'term':'18','balls':[1,3,6,11,16,18,22,24,26,30,32,33,45,48,51,52,66,73,78,79,32]},
    #     {'term':'19','balls':[3,6,8,13,17,19,26,29,32,45,48,50,51,53,56,62,67,74,77,79,6]},
    #     {'term':'20','balls':[1,6,8,11,12,14,22,28,34,40,41,42,62,63,64,66,71,72,77,79,42]},
    # ]


    # calcuBingo = []

    #endregion

    bingoStatistics = bingoStatistics.BingoStatistics(calcuBingo)
    numbers = list(range(1, 80))  # 生成 1 到 80 的数字列表
    # 在目前數之中生成4數字為一組不重複組合
    combinations_array = list(combinations(numbers, 3))
    arrInput = list(map(lambda r:list(r),combinations_array))
    arrResult = []
    for item in arrInput:
        result = bingoStatistics.calcu(item)
        arrResult.append(result)
    arrEffect = list(filter(lambda r:r['support'] != 0,arrResult))
    arrApprove = list(filter(lambda r:r['support'] > 0.2 and r['maxValue'] < 5,arrEffect))

    for item in arrEffect:
        print(item)