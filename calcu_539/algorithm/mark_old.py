from abc import ABC, abstractmethod
import unittest
from unittest.mock import Mock
import itertools


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


class IConvertMark(ABC):

    @abstractmethod
    def loadStds(self) -> list[str]:
        pass

    @abstractmethod
    def ballToMark(self, ball: str) -> str:
        pass

    @abstractmethod
    def markToBalls(self, mark: str) -> list[str]:
        pass


class BeginConvertMark(IConvertMark):
    """用原始球號不分組"""

    def loadStds(self) -> list[str]:
        deferBallInfos = [
            BallGroup('01', 0), BallGroup('02', 0), BallGroup(
                '03', 0), BallGroup('04', 0), BallGroup('05', 0),
            BallGroup('06', 0), BallGroup('07', 0), BallGroup(
                '08', 0), BallGroup('09', 0), BallGroup('10', 0),
            BallGroup('11', 0), BallGroup('12', 0), BallGroup(
                '13', 0), BallGroup('14', 0), BallGroup('15', 0),
            BallGroup('16', 0), BallGroup('17', 0), BallGroup(
                '18', 0), BallGroup('19', 0), BallGroup('20', 0),
            BallGroup('21', 0), BallGroup('22', 0), BallGroup(
                '23', 0), BallGroup('24', 0), BallGroup('25', 0),
            BallGroup('26', 0), BallGroup('27', 0), BallGroup(
                '28', 0), BallGroup('29', 0), BallGroup('30', 0),
            BallGroup('31', 0), BallGroup('32', 0), BallGroup(
                '33', 0), BallGroup('34', 0), BallGroup('35', 0),
            BallGroup('36', 0), BallGroup('37', 0), BallGroup(
                '38', 0), BallGroup('39', 0)
        ]
        return deferBallInfos

    def ballToMark(self, ball: str) -> str:
        return ball
        pass

    def markToBalls(self, mark: str) -> list[str]:
        return [mark]
        pass

    pass


class ConvertMark(ABC):
    """將球號分組"""

    def __init__(self) -> None:
        pass

    def loadStds(self) -> list[str]:
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
        return deferBallInfos
        pass

    def ballToMark(self, ball: str) -> str:
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

    def markToBalls(self, mark: str) -> list[str]:
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


class ConvertOddEvenMark(ABC):
    """將球號分組"""

    def __init__(self) -> None:
        pass

    def loadStds(self) -> list[str]:
        deferBallInfos = [
            BallGroup('單一', 0), BallGroup('單二', 0), BallGroup(
                '單三', 0), BallGroup('單四', 0), BallGroup('單五', 0),
            BallGroup('雙一', 0), BallGroup('雙二', 0), BallGroup(
                '雙三', 0), BallGroup('雙四', 0), BallGroup('雙五', 0),
            BallGroup('單六', 0), BallGroup('單七', 0), BallGroup(
                '單八', 0), BallGroup('單九', 0),
            BallGroup('雙六', 0), BallGroup('雙七', 0), BallGroup(
                '雙八', 0), BallGroup('雙九', 0),
            BallGroup('零', 0),
        ]
        return deferBallInfos
        pass

    def ballToMark(self, ball: str) -> str:
        """
        依照球號排序
        """
        if any(ball == n for n in ['31', '11']):
            return '單一'
        if any(ball == n for n in ['32', '12']):
            return '單二'
        if any(ball == n for n in ['33', '13']):
            return '單三'
        if any(ball == n for n in ['34', '14']):
            return '單四'
        if any(ball == n for n in ['35', '15']):
            return '單五'

        if any(ball == n for n in ['21', '01']):
            return '雙一'
        if any(ball == n for n in ['22', '02']):
            return '雙二'
        if any(ball == n for n in ['23', '03']):
            return '雙三'
        if any(ball == n for n in ['24', '04']):
            return '雙四'
        if any(ball == n for n in ['25', '05']):
            return '雙五'

        if any(ball == n for n in ['36', '16']):
            return '單六'
        if any(ball == n for n in ['37', '17']):
            return '單七'
        if any(ball == n for n in ['38', '18']):
            return '單八'
        if any(ball == n for n in ['39', '19']):
            return '單九'

        if any(ball == n for n in ['26', '06']):
            return '雙六'
        if any(ball == n for n in ['27', '07']):
            return '雙七'
        if any(ball == n for n in ['28', '08']):
            return '雙八'
        if any(ball == n for n in ['29', '09']):
            return '雙九'

        if any(ball == n for n in ['10', '20', '30']):
            return '零'
        return ''

    def markToBalls(self, mark: str) -> list[str]:
        if mark == '單一':
            return ['31', '11']
        if mark == '單二':
            return ['32', '12']
        if mark == '單三':
            return ['33', '13']
        if mark == '單四':
            return ['34', '14']
        if mark == '單五':
            return ['35', '15']

        if mark == '雙一':
            return ['21', '01']
        if mark == '雙二':
            return ['22', '02']
        if mark == '雙三':
            return ['23', '03']
        if mark == '雙四':
            return ['24', '04']
        if mark == '雙五':
            return ['25', '05']

        if mark == '單六':
            return ['36', '16']
        if mark == '單七':
            return ['37', '17']
        if mark == '單八':
            return ['38', '18']
        if mark == '單九':
            return ['39', '19']

        if mark == '雙六':
            return ['26', '06']
        if mark == '雙七':
            return ['27', '07']
        if mark == '雙八':
            return ['28', '08']
        if mark == '雙九':
            return ['29', '09']

        if mark == '零':
            return ['10', '20', '30']
        pass


class TestConvertOddEvenMark(unittest.TestCase):

    def test_ballToMark(self):
        """球號轉換"""
        # arrange
        convert = ConvertOddEvenMark()
        # act
        inputs = ['11', '32', '21', '28', '29']
        marks = [convert.ballToMark(ele) for ele in inputs]
        # assert
        excepteds = ['單一', '單二', '雙一', '雙九', '雙八']
        self.assertCountEqual(marks, excepteds)
        pass

    def test_markToBalls(self):
        """分類轉球號"""
        # arrange
        convert = ConvertOddEvenMark()
        # act
        inputs = ['單一', '單二', '雙一', '雙九', '雙八']
        ball2Ds = [convert.markToBalls(ele) for ele in inputs]
        balls = list(itertools.chain.from_iterable(ball2Ds))
        # assert
        excepted2Ds = [['11', '31'], ['12', '32'],  [
            '01', '21'], ['09', '29'], ['08', '28']]
        excepteds = list(itertools.chain.from_iterable(excepted2Ds))
        self.assertCountEqual(balls, excepteds)
        pass


class TestConvertMark(unittest.TestCase):
    def test_ballToMark(self):
        """球號轉換"""
        # arrange
        convert = ConvertMark()
        # act
        inputs = ['01', '12', '31', '38', '39']
        marks = [convert.ballToMark(ele) for ele in inputs]
        # assert
        excepteds = ['小一', '小二', '大一', '大九', '大八']
        self.assertCountEqual(marks, excepteds)
        pass

    def test_markToBalls(self):
        """分類轉球號"""
        # arrange
        convert = ConvertMark()
        # act
        inputs = ['小一', '小二', '大一', '大九', '大八']
        ball2Ds = [convert.markToBalls(ele) for ele in inputs]
        # assert
        excepted2Ds = [['02', '12'], ['01', '11'],  [
            '21', '31'], ['29', '39'], ['28', '38']]
        self.assertCountEqual(ball2Ds, excepted2Ds)
        pass


if __name__ == '__main__':
    try:
        suite = unittest.TestSuite()
        suite.addTest(TestConvertMark('test_ballToMark'))
        suite.addTest(TestConvertMark('test_markToBalls'))
        suite.addTest(TestConvertOddEvenMark('test_ballToMark'))
        suite.addTest(TestConvertOddEvenMark('test_markToBalls'))

        runner = unittest.TextTestRunner(verbosity=2)
        runner.run(suite)
    except SystemExit:
        pass
