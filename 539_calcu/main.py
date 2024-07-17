from mlxtend.frequent_patterns import apriori, association_rules
from mlxtend.preprocessing import TransactionEncoder
import pandas as pd
import numpy as np
# from bingoModel import BingoInfo
# from prize import Prize
# from db import MSSQLDbContext


class BallGroup:
    """
    球號分組資訊
    times單位可為拖期或次數
    """

    def __init__(self, sort: str, times: int):
        self._sort = sort
        self._times = times

    @property
    def sort(self) -> str:
        return self._sort

    @sort.setter
    def sort(self, value: str):
        self._sort = value

    @property
    def times(self) -> int:
        return self._times

    @times.setter
    def times(self, value: int):
        self._times = value

    pass


if __name__ == '__main__':

    def ballToMark(ball: str) -> str:
        """
        依照球號排序
        """
        if any(ball == n for n in ['01', '11']):
            return '小一'
        if any(ball == n for n in ['02', '12']):
            return '小二'
        if any(ball == n for n in ['03', '13']):
            return '小三'
        if any(ball == n for n in ['04', '14']):
            return '小四'
        if any(ball == n for n in ['05', '15']):
            return '小五'

        if any(ball == n for n in ['21', '31']):
            return '大一'
        if any(ball == n for n in ['22', '32']):
            return '大二'
        if any(ball == n for n in ['23', '33']):
            return '大三'
        if any(ball == n for n in ['24', '34']):
            return '大四'
        if any(ball == n for n in ['25', '35']):
            return '大五'

        if any(ball == n for n in ['06', '16']):
            return '小六'
        if any(ball == n for n in ['07', '17']):
            return '小七'
        if any(ball == n for n in ['08', '18']):
            return '小八'
        if any(ball == n for n in ['09', '19']):
            return '小九'

        if any(ball == n for n in ['26', '36']):
            return '大六'
        if any(ball == n for n in ['27', '37']):
            return '大七'
        if any(ball == n for n in ['28', '38']):
            return '大八'
        if any(ball == n for n in ['29', '39']):
            return '大九'

        if any(ball == n for n in ['10', '20', '30']):
            return '零'
        return ''

    def markToBalls(mark: str) -> list[str]:
        if mark == '小一':
            return ['01', '11']
        if mark == '小二':
            return ['02', '12']
        if mark == '小三':
            return ['03', '13']
        if mark == '小四':
            return ['04', '14']
        if mark == '小五':
            return ['05', '15']

        if mark == '大一':
            return ['21', '31']
        if mark == '大二':
            return ['22', '32']
        if mark == '大三':
            return ['23', '33']
        if mark == '大四':
            return ['24', '34']
        if mark == '大五':
            return ['25', '35']

        if mark == '小六':
            return ['06', '16']
        if mark == '小七':
            return ['07', '17']
        if mark == '小八':
            return ['08', '18']
        if mark == '小九':
            return ['09', '19']

        if mark == '大六':
            return ['26', '36']
        if mark == '大七':
            return ['27', '37']
        if mark == '大八':
            return ['28', '38']
        if mark == '大九':
            return ['29', '39']

        if mark == '零':
            return ['10', '20', '30']
        pass

    firstAna = 5
    endAna = 20
    # region db來源,未來抽換先用hard code,先用30期模擬

    sources = [
        # 2024/07/06-2024/07/02
        {'bigShowOrder': "04,21,24,33,35"}, {'bigShowOrder': "17,18,23,24,28"}, {
            'bigShowOrder': "09,12,15,26,33"}, {'bigShowOrder': "04,20,25,33,34"}, {'bigShowOrder': "03,15,16,20,22"},
        # 2024/07/01-2024/06/26
        {'bigShowOrder': "08,11,17,19,23"}, {'bigShowOrder': "02,17,26,33,35"}, {
            'bigShowOrder': "12,16,25,27,39"}, {'bigShowOrder': "15,18,27,28,31"}, {'bigShowOrder': "02,21,37,38,39"},

        # 2024/06/25-2024/06/20
        {'bigShowOrder': "25,26,32,36,37"}, {'bigShowOrder': "03,13,17,32,39"}, {
            'bigShowOrder': "01,21,22,25,27"}, {'bigShowOrder': "10,12,15,16,23"}, {'bigShowOrder': "12,13,16,20,32"},
        # 2024/06/19-2024/06/14
        {'bigShowOrder': "02,10,11,14,22"}, {'bigShowOrder': "02,09,15,29,38"}, {
            'bigShowOrder': "02,08,26,32,34"}, {'bigShowOrder': "05,08,35,36,37"}, {'bigShowOrder': "01,02,17,20,37"},
        # 2024/06/13-2024/06/08
        {'bigShowOrder': "03,12,17,30,38"}, {'bigShowOrder': "14,19,20,29,32"}, {
            'bigShowOrder': "03,13,26,32,34"}, {'bigShowOrder': "18,19,30,33,38"}, {'bigShowOrder': "11,19,24,31,32"},
        # 2024/06/07-2024/06/03
        {'bigShowOrder': "01,04,27,34,35"}, {'bigShowOrder': "03,11,20,21,36"}, {
            'bigShowOrder': "03,04,06,14,20"}, {'bigShowOrder': "07,11,17,23,25"}, {'bigShowOrder': "06,10,21,24,31"},
        # 2024/06/01-2024/05/28
        {'bigShowOrder': "04,20,24,28,38"}, {'bigShowOrder': "08,12,13,23,36"}, {
            'bigShowOrder': "02,09,32,36,37"}, {'bigShowOrder': "01,07,09,20,32"}, {'bigShowOrder': "16,23,29,36,39"},
        # 2024/05/27-2024/05/22
        {'bigShowOrder': "05,13,14,17,24"}, {'bigShowOrder': "01,15,32,34,38"}, {
            'bigShowOrder': "05,16,22,26,39"}, {'bigShowOrder': "14,23,26,27,34"}, {'bigShowOrder': "11,13,15,23,29"},
        # 2024/05/21-2024/05/16
        {'bigShowOrder': "01,03,16,24,31"}, {'bigShowOrder': "03,05,28,32,34"}, {
            'bigShowOrder': "05,10,11,32,37"}, {'bigShowOrder': "14,19,27,30,38"}, {'bigShowOrder': "09,10,21,33,35"},
        # 2024/05/15-2024/05/10
        {'bigShowOrder': "04,06,14,26,33"}, {'bigShowOrder': "07,11,18,20,22"}, {
            'bigShowOrder': "04,14,33,36,37"}, {'bigShowOrder': "01,07,11,15,29"}, {'bigShowOrder': "01,12,31,38,39"},
    ]
    results = list(map(lambda x: x['bigShowOrder'].split(','), sources))
    inputs = results[firstAna:endAna]
    # endregion

    min_support = 0.15
    min_threshold = 0.15

    # region 關聯式規則array,透過調整min_support、min_threshold來取得數量多寡

    mark2Ds = list(map(lambda arr: list(
        map(lambda ele: ballToMark(ele), arr)), inputs))
    te = TransactionEncoder()
    te_ary = te.fit(mark2Ds).transform(mark2Ds)
    df = pd.DataFrame(te_ary, columns=te.columns_)
    # 使用apriori找出频繁项集
    frequent_itemsets = apriori(df, min_support=min_support, use_colnames=True)
    # 生成关联规则
    rules = association_rules(
        frequent_itemsets, metric="confidence", min_threshold=min_threshold)
    # print(rules[['antecedents', 'consequents', 'support', 'confidence']])
    # column + column
    # column to rows
    rules['relationshipAnt'] = rules['antecedents'].apply(
        lambda x: str(list(x)[0]))
    rules['relationshipCon'] = rules['consequents'].apply(
        lambda x: str(list(x)[0]))
    # print(rules[['relationshipAnt', 'relationshipCon']])
    relationShips = []
    for item1, item2 in zip(rules['relationshipAnt'], rules['relationshipCon']):
        arr = [item1, item2]
        # arr判別是否有重複
        # any(times == x for x in resultGroups)
        if any(len(set(arr+relation)) == 2 for relation in relationShips) == False:
            relationShips.append(arr)
        pass
    # print(relationShips)
    # print('relationship')
    # endregion

    deferTake = 3
    timeTake = 6
    # region 拖期和次數array,透過設定離群值、前幾元素來取得數量多寡

    deferBallInfos = [
        BallGroup('小一', 0), BallGroup('小二', 0), BallGroup(
            '小三', 0), BallGroup('小四', 0), BallGroup('小五', 0),
        BallGroup('大一', 0), BallGroup('大二', 0), BallGroup(
            '大三', 0), BallGroup('大四', 0), BallGroup('大五', 0),
        BallGroup('小六', 0), BallGroup('小七', 0), BallGroup(
            '小八', 0), BallGroup('小九', 0),
        BallGroup('大六', 0), BallGroup('大七', 0), BallGroup(
            '大八', 0), BallGroup('大九', 0),
        BallGroup('零', 0),
    ]

    timesBallInfos = [BallGroup('小一', 0), BallGroup('小二', 0), BallGroup(
        '小三', 0), BallGroup('小四', 0), BallGroup('小五', 0),
        BallGroup('大一', 0), BallGroup('大二', 0), BallGroup(
        '大三', 0), BallGroup('大四', 0), BallGroup('大五', 0),
        BallGroup('小六', 0), BallGroup('小七', 0), BallGroup(
        '小八', 0), BallGroup('小九', 0),
        BallGroup('大六', 0), BallGroup('大七', 0), BallGroup(
        '大八', 0), BallGroup('大九', 0),
        BallGroup('零', 0),
    ]

    for arr in inputs:
        for ele in arr:
            mark = ballToMark(ele)
            timesBall = next(
                (x for x in timesBallInfos if x.sort == mark), None)
            timesBall.times += 1
            pass

    # print('timesBalls')

    for deferBall in deferBallInfos:
        isSearch = False
        for idx, arr in enumerate(inputs):
            if isSearch == True:
                break
            for ele in arr:
                mark = ballToMark(ele)
                if deferBall.sort == mark:
                    deferBall.times += idx
                    isSearch = True
                    break
        if isSearch == False:
            deferBall.times += len(inputs)
    # print('deferBalls')

    # sorted_quotes = sorted(quotes, key=lambda q: q.quote_id)
    # sorted_numbers = sorted(numbers, reverse=True)
    timesBallInfoAscs = sorted(timesBallInfos, key=lambda x: x.times)

    # 計算四分位距算出上下界
    timesBalls = list(map(lambda x: x.times, timesBallInfoAscs))
    # 計算第一四分位數（Q1）和第三四分位數（Q3）
    Q1 = np.percentile(timesBalls, 25)
    Q3 = np.percentile(timesBalls, 75)

    # 計算四分位距（IQR）
    IQR = Q3 - Q1

    # 計算上界和下界
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR

    # 拖號倒過來讓熱門再前
    # deferBallInfoDescs = sorted(
    #     deferBallInfos, key=lambda x: x.times, reverse=True)
    deferBallInfoAscs = sorted(
        deferBallInfos, key=lambda x: x.times)
    # print('sort')
    timesBallAscs = list(map(lambda x: x.sort, timesBallInfoAscs))
    deferBallAscs = list(map(lambda x: x.sort, deferBallInfoAscs))

    deferBallAscs = deferBallAscs[:deferTake]
    timesBallAscs = timesBallAscs[:timeTake]
    # endregion

    compose = 5
    # region 策略透過關聯式規則其中之一吻合拖期和次數前幾次來設定此規則是否成立
    print('關聯式規則')
    print(relationShips)
    print('拖期')
    print(deferBallAscs)
    print('次數')
    print(timesBallAscs)

    resultMarks = []
    for relation in relationShips:
        isExist = any(relation[0] == x for x in deferBallAscs) or any(relation[1] == x for x in deferBallAscs) or any(
            relation[0] == x for x in timesBallAscs) or any(
            relation[1] == x for x in timesBallAscs)
        isOver = len(resultMarks) < compose
        if isExist and isOver:
            resultMarks.append(relation)

    print('組合結果')
    print(resultMarks)

    # endregion

    firstSign = 0
    endSign = 4
    # region 對獎
    actuals = results[firstSign:endSign]
    actualMarks = list(map(lambda arr: list(
        map(lambda ele: ballToMark(ele), arr)), actuals))
    print('實際開出')
    print(actualMarks)
    for idx, mark in enumerate(actualMarks):
        for x in resultMarks:
            if len(set(mark+x)) == 5:
                joinedMark = ','.join(x)
                print('第'+str(idx)+'期:'+joinedMark)

    # endregion

    pass
