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
from bingo_scrapy.db import SQL
from datetime import date, datetime, timedelta
import logging


class TestScrapyPipeline:

    def __init__(self):
        db = SQL({'server': 'wpdb2.hihosting.hinet.net', 'user': 'p89880749_p89880749',
                  'password': 'Jonny1070607!@#$%', 'database': 'p89880749_test'})
        pass

    def open_spider(self, spider):
        db = SQL({'server': 'wpdb2.hihosting.hinet.net', 'user': 'p89880749_p89880749',
                  'password': 'Jonny1070607!@#$%', 'database': 'p89880749_test'})
        # 若Flag為True則刪除DB資料
        delDate = date.today() - timedelta(days=spider.beforeDay)
        errDelete = db.delete(
            f"delete from Bingo where dDate >= '{delDate}'")
        if errDelete != '':
            logging.error(errDelete)
        # pdb.set_trace()  # Set a breakpoint here

        # 刪除檔案
        currentDir = os.getcwd()
        fileName = "bingo.csv"
        file = os.path.join(currentDir, fileName)
        logging.info(file)
        if os.path.exists(file):
            os.remove(file)
        # pdb.set_trace()  # Set a breakpoint here
        pass

    def close_spider(self, spider):

        # 從DB中判別是否更新到最新天數
        # 若超過時間太長用一週來更新
        # 沒超過一週用落差時間來更新
        # 更新當日資料

        # currDir = os.path.dirname(os.path.abspath(__file__))
        currentDir = os.getcwd()
        file = os.path.join(currentDir, 'bingo.csv')
        logging.info(file)
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
                    elif key == 'drawTerm':
                        newObj[key] = int(value)
                    else:
                        newObj[key] = value
                newObj['createDate'] = 'CURRENT_TIMESTAMP'
                # pdb.set_trace()  # Set a breakpoint here
                data.append(newObj)
        # pdb.set_trace()  # Set a breakpoint here
        db = SQL({'server': 'wpdb2.hihosting.hinet.net', 'user': 'p89880749_p89880749',
                  'password': 'Jonny1070607!@#$%', 'database': 'p89880749_test'})
        result = db.insert('Bingo', data)
        if result != '':
            logging.error(result)
        else:
            logging.info('Insert Success')
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
