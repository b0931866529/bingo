import pandas as pd
from collections import defaultdict
from itertools import chain
import statistics
from itertools import combinations


class ValidMsg:
    def __init__(self, item, describe, isOK, errorMsg):
        self.item = item
        self.describe = describe
        self.isOK = isOK
        self.errorMsg = errorMsg


def convertMsg(r):
    return '驗證項目:{},驗證方法:{},錯誤訊息:{}'.format(r.item, r.describe, r.errorMsg)


class BingoStatistics:
    # 總共球數
    BALL_NUM = 20
    bingoData = []
    # 將要分析開獎資料給載入

    def __init__(self, bingoData: []):
        self.bingoData = bingoData

    def calcu(self, input: []):
        support = 0.0
        maxValue = 0
        median_value = 0.0
        # region concat length filter whether match count support
        setConcat = list(
            map(lambda r: set(r['balls'] + input), self.bingoData))
        arrConcat = list(map(lambda r: list(r), setConcat))
        arrTermConcat = list(
            map(lambda x, y: {'term': y['term'], 'balls': x}, arrConcat, self.bingoData))
        arrFilter = list(filter(lambda r: len(
            r['balls']) == self.BALL_NUM, arrTermConcat))
        # region valid array 0,1
        if len(arrFilter) == 0 or len(arrFilter) == 1:
            return {
                'source': input,
                'support': support,
                'maxValue': maxValue,
                'median_value': median_value,
            }
        # endregion
        support = len(arrFilter) / len(self.bingoData)
        # endregion

        # region map term array map plus time array,count max、median
        arrIntTerm = list(map(lambda r: int(r['term']), arrFilter))
        arrIntTime = []
        i = 0
        for term in arrIntTerm:
            if i != 0:
                temp = arrIntTerm[i] - arrIntTerm[i-1]
                arrIntTime.append(temp)
            i = i + 1

        maxValue = max(arrIntTime)
        median_value = statistics.median(arrIntTime)
        # endregion

        return {
            'source': input,
            'support': support,
            'maxValue': maxValue,
            'median_value': median_value,
        }


if __name__ == '__main__':
    msgs = []
    # 一樣有calcu
    # 原本calcu邏輯封裝成private後用array去接收
    # exclcude logic封裝成private

    # region maxValue計算中位數,exclude:support==0 and maxValue > 中位數,最後order support desc 前5
    # try:
    # bingoSimulation.settingSource(
    #     startegyNums, bingoNums, Lottery.BINGO_THREE)
    # assert (len(bingoSimulation.dfStartegy.columns) == 3 and len(
    #     bingoSimulation.dfActual.columns) == 5 and bingoSimulation.lottery == Lottery.BINGO_THREE)
    # msgs.append(ValidMsg('驗證回朔測試載入來源是否正常',
    #             'bingo規則為3星、策略組數3和實際號碼為5', True, ''))
    # except AssertionError:
    #     msgs.append(ValidMsg('驗證回朔測試載入來源是否正常',
    #                 'bingo規則為3星、策略組數3和實際號碼為5', False, '載入參數異常'))
    # except exception as e:
    #     msgs.append(ValidMsg('驗證回朔測試載入來源是否正常',
    #                 'bingo規則為3星、策略組數3和實際號碼為5', False, e))
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

    # region
    # bingoData = [
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
    # # input = [1,3,5,10]
    # bingoStatistics = BingoStatistics(bingoData)

    # numbers = list(range(1, 80))  # 生成 1 到 80 的数字列表
    # # 在目前數之中生成4數字為一組不重複組合
    # combinations_array = list(combinations(numbers, 3))
    # arrInput = list(map(lambda r:list(r),combinations_array))
    # arrResult = []
    # for item in arrInput:
    #     result = bingoStatistics.calcu(item)
    #     arrResult.append(result)
    # arrEffect = list(filter(lambda r:r['support'] != 0,arrResult))
    # arrApprove = list(filter(lambda r:r['support'] > 0.2 and r['maxValue'] < 5,arrEffect))
    # print('')
    # endregion
