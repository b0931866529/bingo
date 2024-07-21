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

        # # 沒超過一週用落差時間來更新
        # # 更新當日資料
        # # 從DB中判別是否更新到最新天數
        # rows = self.db.select(
        #     'Select MAX(dDate) As dDate From Bingo Group By dDate ORDER BY dDate DESC')
        # # 若超過時間太長用前三天來更新
        # overDate = date.today() - timedelta(days=3)
        # dbDate = overDate if len(rows) == 0 else rows[0]['dDate']
        # offset = (date.today() - dbDate).days
        # if dbDate == overDate or offset > 3:
        #     self.beforeDay = 3
        # else:
        #     self.beforeDay = offset

        # if self.beforeDay == 0:
        #     self.beforeDay += 1

        # # pdb.set_trace()  # Set a breakpoint here
        # for i in range(0, self.beforeDay + 1):
        #     crawlDate = date.today() if i == 0 else date.today() - timedelta(days=i)
        #     # pdb.set_trace()  # Set a breakpoint here
        #     # url = f'https://api.taiwanlottery.com/TLCAPIWeB/Lottery/BingoResult?openDate={crawlDate}&pageNum=1&pageSize=10'
        #     url = f'https://api.taiwanlottery.com/TLCAPIWeB/Lottery/Daily539Result?period&month=2024-06&pageNum=1&pageSize=50'
        #     logging.info(url)
        #     # pdb.set_trace()  # Set a breakpoint here
        #     self.start_urls.append(url)
        # pdb.set_trace()  # Set a breakpoint here
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


        

   
