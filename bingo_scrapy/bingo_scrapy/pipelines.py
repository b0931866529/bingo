# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import pdb
import json


class TestScrapyPipeline:
    def open_spider(self, spider):
        # self.file = open('setting.json', 'w')
        # pdb.set_trace()  # Set a breakpoint here
        pass

    def close_spider(self, spider):
        pass

    def process_item(self, item, spider):
        return item
