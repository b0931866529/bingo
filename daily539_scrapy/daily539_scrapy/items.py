# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class Daily539Item(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    period = scrapy.Field()
    lotteryDate = scrapy.Field()
    drawNumberSize = scrapy.Field()
