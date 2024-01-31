import numpy as np
import pandas as pd
from enum import Enum
import bingo_scrapy.bingo_scrapy.db as db
from bson import ObjectId
from datetime import datetime

import sys
print(sys.executable)
print(sys.executable)


class ValidMsg:
    def __init__(self, item, describe, isOK, errorMsg):
        self.item = item
        self.describe = describe
        self.isOK = isOK
        self.errorMsg = errorMsg


class StrategyParam:
    def __init__(self, support, maxValue):
        self.support = support
        self.maxValue = maxValue


class Lottery(Enum):
    BINGO = 0
    THREE_STAR = 1
    BINGO_THREE = 500

# 錯誤訊息結構轉成string


def convertMsg(r):
    return '驗證項目:{},驗證方法:{},錯誤訊息:{}'.format(r.item, r.describe, r.errorMsg)


class BingoSimulation:
    # 載入輸入、期望array
    def __init__(self):
        self.income = 0
        self.profit = 0
        # 成本為總期數 * 每個策略組數都投入
        self.cost = 0

    # 設定策略號碼、實際號碼、號碼玩法
    def settingSource(self, startegyNums: [], actualNums: [], lottery: Enum):

        # region dfActual dic of array to key of dict
        dictActual = {}
        for ele in actualNums:
            dictActual[str(ele['term'])] = ele['balls']
        self.dfActual = pd.DataFrame(dictActual)

        # endregion

        # region dfStartegy append index column
        dicStartegy = {}
        i = 0
        for ele in startegyNums:
            idxName = 'strategy{}'.format(str(i))
            dicStartegy[idxName] = ele
            i = i + 1
        self.dfStartegy = pd.DataFrame(dicStartegy)

        # endregion

        self.lottery = lottery
        return ''

    # 設定策略參數:過濾support、maxValue,median_value order desc是否進行加倍
    # def settingStrategy(strategyParam: StrategyParam):
        self.strategyParam = strategyParam
        return ''

    # 計算成本、報酬、期數
    def calcu(self):
        idx = 0
        for iStrategy in range(0, len(self.dfStartegy.columns)):
            strategyIdx = 'strategy{}'.format(str(iStrategy))
            input = self.dfStartegy[strategyIdx].tolist()
            for iActual in range(1, len(self.dfActual.columns) + 1):
                item = self.dfActual[str(iActual)].tolist()
                matches = set(item + input)
                if len(matches) == 20:
                    self.income += 500
                self.cost += 25
                idx += 1

        self.profit = self.income - self.cost


if __name__ == '__main__':
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

    msgs = []
    strategy = [[3, 42, 74], [3, 48, 60], [
        3, 51, 66], [7, 20, 25], [9, 18, 25]]
    bingoSimulation = BingoSimulation()
    bingoSimulation.settingSource(strategy, calcuBingo, Lottery.BINGO_THREE)
    bingoSimulation.calcu()
    print('')
    # region 驗證回朔測試載入來源是否正常
    startegyNums = [[10, 16, 19], [2, 4, 80], [11, 30, 45]]
    bingoNums = [
        {'term': '1', 'balls': [1, 2, 9, 11, 12,
                                13, 15, 18, 23, 25,
                                30, 32, 35, 36, 48,
                                53, 59, 61, 67, 80]},
        {'term': '2', 'balls': [1, 2, 3, 6, 9,
                                12, 14, 22, 26, 28,
                                33, 40, 43, 44, 45,
                                49, 50, 54, 69, 49]},
        {'term': '3', 'balls': [10, 13, 31, 38, 43,
                                47, 48, 49, 52, 53,
                                56, 60, 64, 66, 72,
                                73, 76, 77, 79, 80]},
        {'term': '4', 'balls': [10, 12, 16, 19, 24,
                                26, 30, 35, 41, 47,
                                49, 54, 55, 58, 59,
                                66, 69, 75, 77, 78]},

        {'term': '5', 'balls': [20, 21, 25, 28, 30,
                                33, 35, 36, 42, 43,
                                47, 48, 61, 66, 68,
                                69, 73, 75, 76, 80]},
    ]
    try:
        bingoSimulation.settingSource(
            startegyNums, bingoNums, Lottery.BINGO_THREE)
        assert (len(bingoSimulation.dfStartegy.columns) == 3 and len(
            bingoSimulation.dfActual.columns) == 5 and bingoSimulation.lottery == Lottery.BINGO_THREE)
        msgs.append(ValidMsg('驗證回朔測試載入來源是否正常',
                    'bingo規則為3星、策略組數3和實際號碼為5', True, ''))
    except AssertionError:
        msgs.append(ValidMsg('驗證回朔測試載入來源是否正常',
                    'bingo規則為3星、策略組數3和實際號碼為5', False, '載入參數異常'))
    except exception as e:
        msgs.append(ValidMsg('驗證回朔測試載入來源是否正常',
                    'bingo規則為3星、策略組數3和實際號碼為5', False, e))
    # endregion

    # region 驗證回朔設定策略參數是否正常
    # bingoSimulation.settingStrategy(StrategyParam(0.15,10))
    # try:
    #   exceptStrategyParam = StrategyParam(0.15,10)
    #   assert (exceptStrategyParam.support == bingoSimulation.strategyParam.support and exceptStrategyParam.maxValue == bingoSimulation.strategyParam.maxValue)
    #   msgs.append(ValidMsg('驗證回朔設定策略參數是否正常','比對策略參數支持度和最大值',True,''))
    # except AssertionError:
    #   msgs.append(ValidMsg('驗證回朔設定策略參數是否正常','比對策略參數支持度和最大值',False,''))
    # endregion

    # region 驗證回朔計算成本和利潤是否符合
    validCalcu = ValidMsg(
        '驗證回朔計算成本和利潤是否符合', '總共5期、策略3組3星,中一次,成本應為25*3*5=375,收益為1*500=500,損益為500-375=125', True, '')
    try:
        bingoSimulation.calcu()
        assert bingoSimulation.cost == 375 and bingoSimulation.income == 500 and bingoSimulation.profit == 125
        msgs.append(validCalcu)
    except AssertionError:
        validCalcu.isOK = False
        validCalcu.errorMsg = '計算結果不符合預期'
        msgs.append(validCalcu)
    except Exception as e:
        validCalcu.isOK = False
        validCalcu.errorMsg = e
        msgs.append(validCalcu)
    # endregion

# region return msg
    errors = list(filter(lambda r: r.isOK == False, msgs))
    if len(errors) == 0:
        print('驗證無異常')
        okMsgs = list(map(convertMsg, errors))
        okMsg = "\n".join(okMsgs)
        print(okMsg)
    else:
        errMsgs = list(map(convertMsg, errors))
        errMsg = "\n".join(errMsgs)
        print(errMsg)
# endregion
