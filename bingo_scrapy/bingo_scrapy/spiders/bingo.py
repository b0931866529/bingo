from bingo_scrapy.items import TestScrapyItem
from bingo_scrapy.settings import OPEN_DATE
from bingo_scrapy.settings import END_DAY
from bingo_scrapy.db import SQL
import scrapy
import pdb
import json
import logging
from datetime import date, datetime, timedelta


class BingoSpider(scrapy.Spider):
    # https://www.taiwanlottery.com/lotto/result/bingo_bingo
    name = 'bingo'
    allowed_domains = ['www.taiwanlottery.com', 'api.taiwanlottery.com']
    start_urls = []
    # Flag判別是否更新到最新天數
    beforeDay = 0
    db = SQL({'server': 'wpdb2.hihosting.hinet.net', 'user': 'p89880749_p89880749',
              'password': 'Jonny1070607!@#$%', 'database': 'p89880749_test'})

    def __init__(self, name=None, **kwargs):
        # logging.info('test info log')
        super().__init__(name, **kwargs)

        # 沒超過一週用落差時間來更新
        # 更新當日資料
        # 從DB中判別是否更新到最新天數
        rows = self.db.select(
            'Select MAX(dDate) As dDate From Bingo Group By dDate ORDER BY dDate DESC')
        # 若超過時間太長用前三天來更新
        overDate = date.today() - timedelta(days=3)
        dbDate = overDate if len(rows) == 0 else rows[0]['dDate']
        offset = (date.today() - dbDate).days
        if dbDate == overDate or offset > 3:
            self.beforeDay = 3
        else:
            self.beforeDay = offset

        if self.beforeDay == 0:
            self.beforeDay += 1

        pdb.set_trace()  # Set a breakpoint here
        for i in range(0, self.beforeDay + 1):
            crawlDate = date.today() if i == 0 else date.today() - timedelta(days=i)
            pdb.set_trace()  # Set a breakpoint here
            url = f'https://api.taiwanlottery.com/TLCAPIWeB/Lottery/BingoResult?openDate={crawlDate}&pageNum=1&pageSize=10'
            logging.info(url)
            # pdb.set_trace()  # Set a breakpoint here
            self.start_urls.append(url)
        # pdb.set_trace()  # Set a breakpoint here

    def parse(self, response):
        data = json.loads(response.text)
        totalSize = data['content']['totalSize']
        pageSize = totalSize // 10
        pageMod = totalSize % 10
        if pageMod != 0:
            pageSize += 1

        # yield scrapy.Request(url='https://api.taiwanlottery.com/TLCAPIWeB/Lottery/BingoResult?openDate=2024-01-23&pageNum=2&pageSize=10', callback=self.parse_page)
        # create url
        # 拆解url原始和參數
        # 參數組成字典
        arrUrl = response.url.split('?')
        sourceUrl = arrUrl[0]
        params = arrUrl[1].split('&')
        paramsDict = {}
        for param in params:
            paramArr = param.split('=')
            paramsDict[paramArr[0]] = paramArr[1]

        # pdb.set_trace()  # Set a breakpoint here

        for i in range(1, pageSize):
            link = f'{sourceUrl}?openDate={paramsDict["openDate"]}&pageNum={str(i)}&pageSize=10'
            # pdb.set_trace()  # Set a breakpoint here
            yield scrapy.Request(url=link, callback=self.parse_page)

    def parse_page(self, response):
        print(self.crawler.stats.get_stats())
        # pdb.set_trace()  # Set a breakpoint here
        data = json.loads(response.text)
        # pdb.set_trace()  # Set a breakpoint here
        item = TestScrapyItem()
        for result in data['content']['bingoQueryResult']:
            item['drawTerm'] = result['drawTerm']
            item['dDate'] = result['dDate']
            item['bigShowOrder'] = result['bigShowOrder']
            # pdb.set_trace()
            yield item
        # pass
