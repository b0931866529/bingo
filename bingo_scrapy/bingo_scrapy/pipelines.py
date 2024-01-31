# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import csv
from itemadapter import ItemAdapter
import pdb
import json
import os
from bingo_scrapy.db import MongoDbContext
from datetime import datetime


class TestScrapyPipeline:

    def __init__(self):
        self.db = MongoDbContext("localhost", "LotteryTicket")
        self.table = "Bingo"

    def open_spider(self, spider):
        queryKey = {'dDate': {'$gte': datetime(2024, 1, 1)}}
        self.db.Delete(self.table, queryKey)
        # self.file = open('setting.json', 'w')
        # 刪除檔案
        currentDir = os.getcwd()
        fileName = "bingo.csv"
        file = os.path.join(currentDir, fileName)
        if os.path.exists(file):
            os.remove(file)
        # pdb.set_trace()  # Set a breakpoint here
        pass

    def close_spider(self, spider):
        currDir = os.path.dirname(os.path.abspath(__file__))
        file = os.path.join(currDir, 'bingo.csv')
        # pdb.set_trace()  # Set a breakpoint here
        with open(file, 'r') as f:
            reader = csv.DictReader(f)
            data = []
            for obj in reader:
                newObj = {}
                for key, value in obj.items():
                    if key == 'dDate':
                        date_string = obj[key].split('T')[0]
                        date = datetime.strptime(date_string, "%Y-%m-%d")
                        newObj[key] = date
                    elif key == 'bigShowOrder':
                        arr = []
                        for e in value.split(','):
                            arr.append(int(e))
                        newObj[key] = arr
                    else:
                        newObj[key] = value
                data.append(newObj)
        self.db.Insert(self.table, data)
        # pdb.set_trace()  # Set a breakpoint here
        pass

    def process_item(self, item, spider):
        # pdb.set_trace()  # Set a breakpoint here
        # arr = []
        # for e in item['bigShowOrder']:
        #     arr.append(int(e))
        # # arr = map(lambda x: int(x), item['bigShowOrder'])
        # # # pdb.set_trace()  # Set a breakpoint here
        # item['bigShowOrder'] = arr
        # pdb.set_trace()  # Set a breakpoint here
        return item
