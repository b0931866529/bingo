from ..items import TestScrapyItem
import scrapy
import pdb
import json
from ..settings import OPEN_DATE


class BingoSpider(scrapy.Spider):
    # https://www.taiwanlottery.com/lotto/result/bingo_bingo
    name = 'bingo'
    allowed_domains = ['www.taiwanlottery.com', 'api.taiwanlottery.com']
    start_urls = []

    def __init__(self, name=None, **kwargs):
        super().__init__(name, **kwargs)
        arrDate = OPEN_DATE.split('-')
        day = int(arrDate[2])
        for i in range(day, 25):
            date = f'{arrDate[0]}-{arrDate[1]}-{str(i).zfill(2)}'
            url = f'https://api.taiwanlottery.com/TLCAPIWeB/Lottery/BingoResult?openDate={date}&pageNum=1&pageSize=10'
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
