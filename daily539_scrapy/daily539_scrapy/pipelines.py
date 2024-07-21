# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import csv
from itemadapter import ItemAdapter
from scrapy.exporters import CsvItemExporter
import pdb
import json
import os

# from daily539_scrapy.db import SQL

from datetime import date, datetime, timedelta
import logging

class DBPipeline:

    def open_spider(self, spider):
        pdb.set_trace()
        print('DBPipeline open_spider')
        
    def close_spider(self, spider): 
       pdb.set_trace()
       print('DBPipeline close_spider')
       

    def process_item(self, item, spider):
        return item
    
class CsvPipeline:

    def __init__(self):
        self.file = open('daily539.csv', 'wb')
        self.exporter = CsvItemExporter(self.file, encoding='big5')
        self.exporter.start_exporting()
        pdb.set_trace()
        print('CsvPipeline init')

    def process_item(self, item, spider):
        self.exporter.export_item(item)
        return item
    
    def close_spider(self, spider):
        self.exporter.finish_exporting()
        self.file.close()
        pdb.set_trace()
        print('CsvPipeline close_spider')
        
class WashPipeline:

    def process_item(self, item, spider):

        item['drawNumberSize'] = '1'
        
        return item
    
    
class Daily539Pipeline:

    def __init__(self):
        # self._db = SQL({'server': 'wpdb2.hihosting.hinet.net', 'user': 'p89880749_p89880749',
        #           'password': 'Jonny1070607!@#$%', 'database': 'p89880749_test'})
        pass

    def open_spider(self, spider):
        # db = SQL({'server': 'wpdb2.hihosting.hinet.net', 'user': 'p89880749_p89880749',
        #           'password': 'Jonny1070607!@#$%', 'database': 'p89880749_test'})
        # # 若Flag為True則刪除DB資料
        # delDate = date.today() - timedelta(days=spider.beforeDay)
        # errDelete = db.delete(
        #     f"delete from Bingo where dDate >= '{delDate}'")
        # if errDelete != '':
        #     logging.error(errDelete)
        # # pdb.set_trace()  # Set a breakpoint here

        # # 刪除檔案
        # currentDir = os.getcwd()
        # fileName = "daily539.csv"
        # file = os.path.join(currentDir, fileName)
        # logging.info(file)
        # if os.path.exists(file):
        #     os.remove(file)
        # pdb.set_trace()  # Set a breakpoint here
        pass

    def close_spider(self, spider):

        pdb.set_trace()
        print('pipelines close_spider')

        # 從DB中判別是否更新到最新天數
        # 若超過時間太長用一週來更新
        # 沒超過一週用落差時間來更新
        # 更新當日資料

        # currDir = os.path.dirname(os.path.abspath(__file__))
        # currentDir = os.getcwd()
        # file = os.path.join(currentDir, 'daily539.csv')
        # logging.info(file)
        # # pdb.set_trace()  # Set a breakpoint here
        # with open(file, 'r') as f:
        #     reader = csv.DictReader(f)
        #     #pdb.set_trace()
        #     data = []
        #     for obj in reader:
        #         newObj = {}
        #         # pdb.set_trace()
        #         for key, value in obj.items():
        #             # pdb.set_trace()
        #             if key == 'lotteryDate':
        #                 date_string = obj[key].split('T')[0]
        #                 date = datetime.strptime(date_string, "%Y-%m-%d")
        #                 newObj[key] = date
        #             elif key == 'period':
        #                 newObj[key] = int(value)
        #             elif key == 'drawNumberSize':
        #                 # pdb.set_trace()  # Set a breakpoint here
        #                 # arr = list(map(lambda x:str(x),value))
        #                 result = value.replace("[","").replace("]","")
        #                 # pdb.set_trace()  # Set a breakpoint here
        #                 newObj[key] = result
                        
        #             else:
        #                 newObj[key] = value
        #         newObj['createDate'] = 'CURRENT_TIMESTAMP'
        #         # pdb.set_trace()  # Set a breakpoint here
        #         data.append(newObj)
        # # pdb.set_trace()  # Set a breakpoint here
        # db = SQL({'server': 'wpdb2.hihosting.hinet.net', 'user': 'p89880749_p89880749',
        #           'password': 'Jonny1070607!@#$%', 'database': 'p89880749_test'})
        # # pdb.set_trace()  # Set a breakpoint here
        # result = db.insert('Daily539', data)
        # # pdb.set_trace()  # Set a breakpoint here
        # if result != '':
        #     logging.error(result)
        # else:
        #     logging.info('Insert Success')
        # # pdb.set_trace()  # Set a breakpoint here
        # pass

    def process_item(self, item, spider):
        # pdb.set_trace()  # Set a breakpoint here
        # arr = []
        # for e in item['bigShowOrder']:
        #     arr.append(int(e))
        # # arr = map(lambda x: int(x), item['bigShowOrder'])
        # # # pdb.set_trace()  # Set a breakpoint here
        # item['bigShowOrder'] = arr
        # pdb.set_trace()  # Set a breakpoint here

        pdb.set_trace()
        print('pipelines process_item')



        return item
