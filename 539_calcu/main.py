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

    inputs = [['02', '03', '15', '24', '37'], ['11', '16',
                                               '25', '28', '30'], ['01', '11', '21', '33', '34']]

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

    print('timesBalls')

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
    print('deferBalls')

    # sorted_quotes = sorted(quotes, key=lambda q: q.quote_id)
    # sorted_numbers = sorted(numbers, reverse=True)
    timesBallInfoAscs = sorted(timesBallInfos, key=lambda x: x.times)
    deferBallInfoDescs = sorted(
        deferBallInfos, key=lambda x: x.times, reverse=True)
    print('sort')
    timesBallAscs = list(map(lambda x: x.sort, timesBallInfoAscs))
    deferBallDescs = list(map(lambda x: x.sort, deferBallInfoDescs))

    takeGroup = 4
    resultGroups = []
    for times, defer in zip(timesBallAscs, deferBallDescs):
        if any(times == x for x in resultGroups) == False and len(resultGroups) < takeGroup:
            resultGroups.append(times)
        if any(defer == x for x in resultGroups) == False and len(resultGroups) < takeGroup:
            resultGroups.append(defer)
            break
        pass
    print("take")

    ball2Ds = list(map(lambda x: markToBalls(x), resultGroups))

    # 組合
    # 使用列表推导式生成新的列表
    # signballs = [[i, j] for ele in row for row in ball2Ds]
    # print(result)
    print('compose')

    # 撈取要計算的期數
    # curSQL = "select drawTerm,bigShowOrder from Bingo WHERE dDate = \'2024-06-28\' ORDER BY drawTerm DESC"
    # dbContext = MSSQLDbContext({'server': 'wpdb2.hihosting.hinet.net', 'user': 'p89880749_p89880749',
    #                             'password': 'Jonny1070607!@#$%', 'database': 'p89880749_test'})
    # rows = dbContext.select(curSQL)
    # print(rows)
    # prize = Prize(dbContext)
    # signs = ['13', '23', '79']
    # # loop計算是否命中
    # results = []
    # for row in rows:
    #     curBingo = row['bigShowOrder'].split(',')
    #     arr = curBingo + signs
    #     isMatch = (len(set(arr)) == 20)
    #     if isMatch:
    #         results.append(row['drawTerm'])
    # overs = []
    # for index, item in enumerate(results):
    #     if index == 0:
    #         overs.append({'drawTerm': item, 'over': item})
    #     else:
    #         overs.append({'drawTerm': item, 'over': item - results[index-1]})
    # print('')
    pass
