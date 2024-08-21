from ..items import Daily539Item
from ..settings import OPEN_DATE
from ..settings import END_DAY
from ..db import SQL
import scrapy
import pdb
import json
import logging
from datetime import date, datetime, timedelta


class Daily539Spider(scrapy.Spider):
    # https://www.taiwanlottery.com/lotto/result/bingo_bingo
    name = 'daily539'
    allowed_domains = ['www.taiwanlottery.com', 'api.taiwanlottery.com']
    start_urls = []
    # Flag判別是否更新到最新天數
    beforeDay = 0
    db = SQL({'server': 'wpdb2.hihosting.hinet.net', 'user': 'p89880749_p89880749',
              'password': 'Jonny1070607!@#$%', 'database': 'p89880749_test'})

    def __init__(self, name=None, **kwargs):
        # logging.info('test info log')
        super().__init__(name, **kwargs)

        url = 'https://api.taiwanlottery.com/TLCAPIWeB/Lottery/Daily539Result?period&month=2023-01&pageNum=1&pageSize=50'
        self.start_urls.append(url)

    def parse(self, response):
        data = json.loads(response.text)
        totalSize = data['content']['totalSize']

        item = Daily539Item()
        for result in data['content']['daily539Res']:
            item['period'] = result['period']
            item['lotteryDate'] = result['lotteryDate']
            # drawNumberSize = ','.join(result['drawNumberSize'])
            item['drawNumberSize'] = result['drawNumberSize']
            # logging.info(item)
            # pdb.set_trace()
            yield item

        pdb.set_trace()
        print('finish scrapy')
