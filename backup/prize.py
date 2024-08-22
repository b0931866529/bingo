from unittest.mock import Mock
import unittest
from typing import List
from bingoModel import BingoInfo, BingoProfitInfo


class Prize:
    def __init__(self, dbContext):
        self._dbContext = dbContext
        pass
    # 要提煉成多筆單

    def calcu(self, inputs: List[BingoInfo]) -> BingoProfitInfo:
        bingoProfitInfo = BingoProfitInfo()
        try:
            for input in inputs:
                result = self.__calcu(input)
                bingoProfitInfo.bingoInfos.append(result)
                bingoProfitInfo.amt += result.amt
        except:
            return BingoProfitInfo()
        return bingoProfitInfo

    def __calcu(self, input: BingoInfo) -> BingoInfo:

        rows = self._dbContext.select(
            'select Top 1 bigShowOrder from Bingo ORDER BY drawTerm')
        curBingo = rows[0]['bigShowOrder'].split(',')
        stds = [
            {'rule': 3, 'isDouble': True, 'matches': [
                {'num': 3, 'prize': 1000}, {'num': 2, 'prize': 50}]},
            {'rule': 4, 'isDouble': True, 'matches': [
                {'num': 4, 'prize': 2000}, {'num': 2, 'prize': 25}]},
            {'rule': 2, 'isDouble': True, 'matches': [
                {'num': 2, 'prize': 150}, {'num': 1, 'prize': 25}]},
            {'rule': 3, 'isDouble': False, 'matches': [
                {'num': 3, 'prize': 500}, {'num': 2, 'prize': 50}]},
        ]
        matches = []
        # calcu match list qty of ball
        for signBall in input.nums:
            if (signBall in curBingo):
                matches.append(signBall)
            # find std by rule and num
        input.matchs = matches

        rules = next(
            (std['matches'] for std in stds if std['rule'] == len(input.nums)), None)
        prize = next((rule['prize']
                     for rule in rules if rule['num'] == len(matches)), 0)
        input.amt = prize * input.double
        # if match std
        # else
        return input


class TestPrize(unittest.TestCase):
    def test_calcu_3num_1ticket_1double_IsDouble_return_2num_1ticket_50amt(self):
        """
        三星一注無加倍,中兩個號碼節日加倍,應得50元
        """
        # arrange
        mockDbContext = Mock()
        mockDbContext.select.return_value = [
            {'bigShowOrder': "01,02,03,04,05,06,07,08,09,10,11,12,13,14,15,16,17,18,19,20"}]
        prize = Prize(mockDbContext)
        # act
        input = BingoInfo()
        input.double = 1
        input.nums = ['02', '14', '55']
        inputs = [input]
        actual = prize.calcu(inputs)
        # assert

        excepted = BingoProfitInfo()
        output = BingoInfo()
        output.double = 1
        output.nums = ['02', '14', '55']
        output.matchs = ['02', '14']
        output.amt = 50
        excepted.bingoInfos = [output]
        excepted.amt = 50
        self.assertEqual(actual, excepted)

    def test_calcu_3num_1ticket_1double_IsDouble_return_3num_1ticket_1000amt(self):
        """
        三星一注無加倍,中三個號碼節日加倍,應得1000元
        """
        # arrange
        mockDbContext = Mock()
        mockDbContext.select.return_value = [
            {'bigShowOrder': "01,02,03,04,05,06,07,08,09,10,11,12,13,14,15,16,17,18,19,20"}]
        prize = Prize(mockDbContext)
        # act
        input = BingoInfo()
        input.double = 1
        input.nums = ['02', '14', '16']
        inputs = [input]
        actual = prize.calcu(inputs)
        # assert
        excepted = BingoProfitInfo()
        output = BingoInfo()
        output.double = 1
        output.nums = ['02', '14', '16']
        output.matchs = ['02', '14', '16']
        output.amt = 1000
        excepted.bingoInfos = [output]
        excepted.amt = 1000
        self.assertEqual(actual, excepted)

    def test_calcu_4num_1ticket_1double_and_3num_1ticket_1double_IsDouble_return_2num_1ticket_3num_1ticket_1025amt(self):
        """
        四星一注無加倍,三星一注無加倍,四星中二、三星中三個號碼節日加倍,應得1025元
        """
        # arrange
        mockDbContext = Mock()
        mockDbContext.select.return_value = [
            {'bigShowOrder': "01,02,03,04,05,06,07,08,09,10,11,12,13,14,15,16,17,18,19,20"}]
        prize = Prize(mockDbContext)
        # act
        input3 = BingoInfo()
        input3.double = 1
        input3.nums = ['16', '18', '19']
        input4 = BingoInfo()
        input4.double = 1
        input4.nums = ['16', '18', '39', '40']
        inputs = [input3, input4]
        actual = prize.calcu(inputs)
        # assert
        excepted = BingoProfitInfo()
        input3 = BingoInfo()
        input3.double = 1
        input3.nums = ['16', '18', '19']
        input3.matchs = ['16', '18', '19']
        input3.amt = 1000
        input4 = BingoInfo()
        input4.double = 1
        input4.nums = ['16', '18', '39', '40']
        input4.matchs = ['16', '18']
        input4.amt = 25
        excepted.bingoInfos = [input4, input3]
        excepted.amt = 1025
        self.assertEqual(actual, excepted)
        pass

    def test_calcu_0num_1ticket_1double_IsDouble_return_empty_array_0amt(self):
        """
        異常資料,無號碼,應得0元
        """
        # arrange
        mockDbContext = Mock()
        mockDbContext.select.return_value = [
            {'bigShowOrder': "01,02,03,04,05,06,07,08,09,10,11,12,13,14,15,16,17,18,19,20"}]
        prize = Prize(mockDbContext)
        # act
        input = BingoInfo()
        input.double = 1
        input.nums = []
        inputs = [input]
        actual = prize.calcu(inputs)
        # assert
        excepted = BingoProfitInfo()
        self.assertEqual(actual, excepted)
        pass


if __name__ == '__main__':
    try:
        # unittest.main(verbosity=2)
        suite = unittest.TestSuite()
        suite.addTest(TestPrize(
            'test_calcu_3num_1ticket_1double_IsDouble_return_2num_1ticket_50amt'))
        suite.addTest(TestPrize(
            'test_calcu_3num_1ticket_1double_IsDouble_return_3num_1ticket_1000amt'))
        suite.addTest(TestPrize(
            'test_calcu_4num_1ticket_1double_and_3num_1ticket_1double_IsDouble_return_2num_1ticket_3num_1ticket_1025amt'))
        suite.addTest(
            TestPrize('test_calcu_0num_1ticket_1double_IsDouble_return_empty_array_0amt'))
        runner = unittest.TextTestRunner(verbosity=2)
        runner.run(suite)

    except SystemExit:
        pass

# input:{double:number,nums:[]}[]
# calcu {amt:number,{double:number,nums:[],match:[],amt:number,cost:number}[]}
# DI db
# dict


# TDD
# input over rule
# exception
# check 1 ticket 3 match 2
# check 1 ticket 3 match 3
# check 1 ticket 3 match 3 1 ticket 4 match 2

# calcu => BingoProfitInfo
# Model提煉
