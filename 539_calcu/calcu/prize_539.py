
class FiveThreeNineSign:
    """
    產出要簽注獎號策略:
    1.冷門球號開始 order by
    2.冷門球號過濾離群值
    3.變異數在某個區間表示夠離散要回補
    4.冷門球號做乘積組合(目前是笛卡爾乘積、但可能用指數)
    5.過濾關聯式和冷門組合球號命中
    6.過濾組合太多規則不明確不簽
    7.過濾變異數下注範圍
    """
    @property
    def strategy(self):
        return self._strategy

    @strategy.setter
    def strategy(self, value):
        self._strategy = value

    @property
    def frtTake(self):
        return self._frtTake

    @frtTake.setter
    def frtTake(self, value):
        self._frtTake = value

    @property
    def min_support(self):
        return self._min_support

    @min_support.setter
    def min_support(self, value):
        self._min_support = value

    @property
    def min_threshold(self):
        return self._min_threshold

    @min_threshold.setter
    def min_threshold(self, value):
        self._min_threshold = value

    @property
    def hot_limit(self):
        return self._hot_limit

    @hot_limit.setter
    def hot_limit(self, value):
        self._hot_limit = value

    def __init__(self, exportFile: ExportFile, convert: ConvertMark, relationCalcu: RelationTerm, isToCsv=False) -> None:
        self._exportFile = exportFile
        self._convert = convert
        self._isToCsv = isToCsv
        self._relationCalcu = relationCalcu
        self._frtTake = 12
        self._min_support = 0.1
        self._min_threshold = 0.7
        self._hot_limit = 13
        pass

    def _getState(self, row: pd.Series):
        if np.isnan(row['varBef'].values[0]):
            return 'cold'
        if row['varBef'].values[0] < 13.65:
            return 'cold'
        if len(row['markOutlierBefs'][0]) < 2:
            return 'cold'
        return 'hot'
        pass

    def sign(self, dfDefer: DataFrame, dfTimes: DataFrame) -> DataFrame:

        dfSign = pd.concat([dfDefer, dfTimes], axis=1, keys=['defer', 'times'])

        # region 刪除不需要計算column
        dfSign.drop(columns=[('defer', '零'), ('defer', '小一'), ('defer', '大一'), ('defer', '小二'), ('defer', '大二'),
                             ('defer', '小三'), ('defer',
                                               '大三'), ('defer', '小四'), ('defer', '大四'),
                             ('defer', '小五'), ('defer',
                                               '大五'), ('defer', '小六'), ('defer', '大六'),
                             ('defer', '小七'), ('defer',
                                               '大七'), ('defer', '小八'), ('defer', '大八'),
                             ('defer', '小九'), ('defer',
                                               '大九'), ('defer', 'std'), ('defer', 'num'),
                             ('times', 'std'), ('times', 'var'),
                             ], axis=1, inplace=True)
        # endregion

        dfSign = dfSign.reset_index(drop=False)
        # 判別期數若<10期直接輸出空array
        # 若>10期先判別標準差是高於10還是低於10,衍生欄位先呈現True、False
        # 後續再加上>10冷門求號 輸出4個
        # 後續再加上<10熱門求號 輸出4個

        # region 衍生欄位冷熱門球號、簽注分類、簽注球號計算方式

        # 這二個欄位是用來判斷是否簽注
        dfSign['varBef'] = dfSign[('defer', 'var')].shift(1).astype(float)
        dfSign['markOutlierBefs'] = dfSign[('defer', 'markOutliers')].shift(1)
        dfSign['state'] = dfSign.apply(lambda x: self._getState(x), axis=1)

        dfSign['balls'] = dfSign.apply(
            lambda row: self._convertRowAsc(row), axis=1)

        dfSign['ballBefs'] = dfSign['balls'].shift(1)

        dfSign['signMark'] = dfSign.apply(
            lambda row: self._getSign(row), axis=1)
        dfSign['signFrtBall2Ds'] = dfSign.apply(
            lambda row: self._getBalls(row), axis=1)

        # 要修改增加關聯式過濾規則
        # dfSign['relation2Ds'] = dfSign.apply(
        #     lambda row: self._getRelation(row), axis=1)

        # 將有吻合關聯式才簽牌,只要其中之一有命中就算
        dfSign['signBall2Ds'] = dfSign.apply(
            lambda row: self._excludeSign(row), axis=1)

        # endregion

        # region 衍生欄位關聯式規則
        # endregion

        if self._isToCsv:
            self._exportFile.exportCsv(
                dfSign, 'C:/Programs/bingo/bingo_scrapy/539_calcu', 'sign.csv')
        return dfSign
        pass

    def _excludeSign(self, row: pd.Series):
        if row['state'].tolist()[0] == 'cold':
            return []
        return row['signFrtBall2Ds'].tolist()[0]
        # 目前暫定不做relation直接將冷門球號簽注
        sign2Ds = []
        signFrtBall2Ds = row['signFrtBall2Ds'].tolist()[0]
        relation2Ds = row['relation2Ds'].tolist()[0]
        if len(signFrtBall2Ds) == 0 or row['state'].tolist()[0] == 'cold':
            return sign2Ds
        for signBall2D in signFrtBall2Ds:
            for relation2D in relation2Ds:
                # test 完全命中
                # if len(set(relation2D + signBall2D)) == 2 or len(set(relation2D + signBall2D)) == 3:
                if len(set(relation2D + signBall2D)) == 2:
                    sign2Ds.append(signBall2D)
                    break
        # 球號太少組合無法精準判別
        # if len(sign2Ds) >= 40:
        #     return []
        return sign2Ds
        pass

    def _getRelation(self, row: pd.Series):
        if int(row['index']) < self._frtTake:
            return []

        self._relationCalcu.min_support = self._min_support  # 最小支持度
        self._relationCalcu.min_threshold = self._min_threshold  # 最小信賴度
        self._relationCalcu.frt = int(row['index']) - self._frtTake  # 開始期數
        self._relationCalcu._end = int(row['index'])  # 結束期數
        results = self._relationCalcu.calcu()
        # 離群值過濾
        ballOutliers = [self._convert.markToBalls(
            c) for c in row[('defer', 'markOutliers')]]
        excludeOutliers = []
        for ele in results:
            if any(set(ele + c) == 2 or set(ele + c) == 3 for c in ballOutliers):
                continue
            excludeOutliers.append(ele)

        return excludeOutliers
        pass

    def _getBalls(self, row: pd.Series):
        marks = row['signMark'].tolist()[0]
        if marks == None or len(marks) == 0:
            return []

        ball2DResults = []
        # isProduct = True
        # # 判別是否笛卡爾乘積
        # if self._strategy == StrategyPrize.Relation_Five_Compose:
        ball2Ds = []
        for mark in marks:
            ball2Ds.append(self._convert.markToBalls(mark))

        # 合并所有列表
        combined_list = ball2Ds[0] + ball2Ds[1] + \
            ball2Ds[2] + ball2Ds[3] + ball2Ds[4] + ball2Ds[5]

        # 生成两个元素为一组的组合
        tpCombinations = list(itertools.product(combined_list, repeat=2))
        combinations = [list(tp) for tp in tpCombinations]

        for arr in combinations:
            if any(len(set(arr + ele)) == 2 for ele in ball2DResults) == False and arr[0] != arr[1]:
                ball2DResults.append(arr)

        # 驗證是否有重複組合,若有print
        excepted = math.comb(len(combined_list), 2)
        if excepted != len(ball2DResults):
            print('有重複組合')

        return ball2DResults
        pass

    def _getSign(self, row: pd.Series):
        if int(row['index']) < self._frtTake:
            return []
        arr = row['ballBefs'].tolist()[0]
        take = 6
        if str(row['state'].tolist()[0]) == 'hot':
            arr.reverse()
            arrHot = []
            # 離群值移除
            for ele in arr:
                if any(ele == c for c in row['markOutlierBefs']):
                    continue
                arrHot.append(ele)
            return arrHot[0:take]
        pass

    def _convertRowAsc(self, row: pd.Series):
        rowBallGroups = [BallGroup('小一', row['times']['小一']), BallGroup('大一', row['times']['大一']),
                         BallGroup('小二', row['times']['小二']), BallGroup(
                             '大二', row['times']['大二']),
                         BallGroup('小三', row['times']['小三']), BallGroup(
                             '大三', row['times']['大三']),
                         BallGroup('小四', row['times']['小四']), BallGroup(
                             '大四', row['times']['大四']),
                         BallGroup('小五', row['times']['小五']), BallGroup(
                             '大五', row['times']['大五']),
                         BallGroup('小六', row['times']['小六']), BallGroup(
                             '大六', row['times']['大六']),
                         BallGroup('小七', row['times']['小七']), BallGroup(
                             '大七', row['times']['大七']),
                         BallGroup('小八', row['times']['小八']), BallGroup(
                             '大八', row['times']['大八']),
                         BallGroup('小九', row['times']['小九']), BallGroup(
                             '大九', row['times']['大九']),
                         ]
        rowBallGroups = sorted(rowBallGroups, key=lambda q: q.times)
        marks = list(map(lambda x: x.sort, rowBallGroups))
        return marks
        pass


class FiveThreeNinePrize:
    """檢驗簽注號碼是否命中,並統計當期簽注和命中數量、是否簽注和命中"""

    def __init__(self, exportFile: ExportFile, convert: ConvertMark, isToCsv=False) -> None:
        self._convert = convert
        self._exportFile = exportFile
        self._isToCsv = isToCsv
        pass

    def _varToQ(self, row: pd.Series):
        Q1 = 7.27
        Q2 = 10.48
        Q3 = 13.65
        if np.isnan(row[('varBef', '')]) or row[('varBef', '')] < Q1:
            return 'Q1'
        elif row[('varBef', '')] >= Q1 and row[('varBef', '')] < Q2:
            return 'Q2'
        elif row[('varBef', '')] >= Q2 and row[('varBef', '')] < Q3:
            return 'Q3'
        elif row[('varBef', '')] > Q3:
            return 'Q4'

    def _toOutlierQty(self, row: pd.Series):
        if row[('markOutlierBefs', '')] == None:
            return 0
        return len(row[('markOutlierBefs', '')])
        pass

    def prize(self, inputs: List[str], dfSign: DataFrame) -> DataFrame:

        dfPrize = pd.DataFrame(inputs, columns=['1', '2', '3', '4', '5'])
        dfPrize['一'] = dfPrize['1'].apply(
            lambda ele: self._convert.ballToMark(ele))
        dfPrize['二'] = dfPrize['2'].apply(
            lambda ele: self._convert.ballToMark(ele))
        dfPrize['三'] = dfPrize['3'].apply(
            lambda ele: self._convert.ballToMark(ele))
        dfPrize['四'] = dfPrize['4'].apply(
            lambda ele: self._convert.ballToMark(ele))
        dfPrize['五'] = dfPrize['5'].apply(
            lambda ele: self._convert.ballToMark(ele))
        dfPrize['stdBalls'] = dfPrize.apply(
            lambda row: [row['1'], row['2'], row['3'], row['4'], row['5']], axis=1)
        dfPrize['stdMarks'] = dfPrize.apply(
            lambda row: [row['一'], row['二'], row['三'], row['四'], row['五']], axis=1)
        dfPrize = pd.concat([dfSign, dfPrize], axis=1)
        dfPrize.drop(columns=['1', '2', '3', '4', '5', '一', '二',
                     '三', '四', '五', 'stdMarks'], axis=1, inplace=True)
        dfPrize['matchQty'] = dfPrize.apply(
            lambda row: self._match(row), axis=1)
        dfPrize['signQty'] = dfPrize.apply(
            lambda arr: self._calcuQty(arr), axis=1)

        dfPrize['actualProfit'] = dfPrize['matchQty'] * \
            1500 - dfPrize['signQty'] * 25
        dfPrize['outlierQty'] = dfPrize.apply(
            lambda arr: self._toOutlierQty(arr), axis=1)

        # 統計用:是否有簽注、是否都無命中
        dfPrize['isSign'] = dfPrize['signQty'] != 0
        dfPrize['isMatch'] = dfPrize.apply(
            lambda row: row['signQty'] != 0 and row['matchQty'] != 0, axis=1)

        # 變異數四分位距
       # Q1 = np.quantile(npArr, 0.25) #7.27
        # Q2 = np.quantile(npArr, 0.5) #10.48
        # Q3 = np.quantile(npArr, 0.75)#13.65
        dfPrize['varQ'] = dfPrize.apply(lambda row: self._varToQ(row), axis=1)

        # column 只留下matchQty、signQty、stdBalls、index (中獎、簽注數量、索引)
        dfPrize.drop(columns=[
            ('times', '小一'),  ('times', '小二'), ('times', '小三'), ('times', '小四'),
            ('times', '小五'),  ('times', '小六'), ('times',
                                                '小七'), ('times', '小八'), ('times', '小九'),
            ('times', '大一'),  ('times', '大二'), ('times', '大三'), ('times', '大四'),
            ('times', '大五'),  ('times', '大六'), ('times',
                                                '大七'), ('times', '大八'), ('times', '大九'),
            ('times', '零'),  ('balls', ''), ('signMark', ''), ('signFrtBall2Ds', ''),
            ('signBall2Ds', ''), ('signFrtBall2Ds', ''), ('times', 'num')], axis=1, inplace=True)

        if self._isToCsv:
            self._exportFile.exportCsv(
                dfPrize, 'C:/Programs/bingo/bingo_scrapy/539_calcu', 'prize.csv')
        return dfPrize
        pass

    def _calcuQty(self, row: pd.Series):
        if len(row[('signBall2Ds', '')]) == 0:
            return 0
        return len(row[('signBall2Ds', '')])
        pass

    def _match(self, row: pd.Series):
        if len(row[('signBall2Ds', '')]) == 0:
            return 0
        stdBalls = row['stdBalls']
        match = 0
        for balls in row[('signBall2Ds', '')]:
            if len(set(stdBalls + balls)) == 5:
                match += 1
        return match

    pass


class TestFiveThreeNinePrize(unittest.TestCase):

    def test_prize(self):
        """獎號計算"""
        # arrange
        exportFileMock = Mock()
        convertMark = ConvertMark()
        fiveThreeNinePrize = FiveThreeNinePrize(
            exportFile=exportFileMock, convert=convertMark)

        # act
        sources = [
            {'bigShowOrder': "04,14,33,36,37"}, {'bigShowOrder': "01,07,11,15,29"}, {
                'bigShowOrder': "01,12,31,38,39"},
        ]
        results = list(
            map(lambda x: x['bigShowOrder'].split(','), sources))
        results.reverse()
        inputs = results
        signColumns = [('signBall2Ds', '')]
        sign2Ds = [
            [[]],
            [[['01', '02'], ['03', '04'], ['11', '14']]],
            [[['01', '02'], ['36', '37']]]
        ]
        dfSign = DataFrame(sign2Ds, columns=signColumns)
        dfPrize = fiveThreeNinePrize.prize(inputs, dfSign)

        # assert
        signQty = dfPrize['signQty'].sum()
        matchQty = dfPrize['matchQty'].sum()
        exceptedSignQty = 5
        exceptedMatchQty = 1
        # signQty、matchQty
        self.assertEqual(signQty, exceptedSignQty)
        self.assertEqual(matchQty, exceptedMatchQty)
        pass
