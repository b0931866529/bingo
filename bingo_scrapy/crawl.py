# -*- coding: utf-8 -*-
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

# 如果报错可以注释掉
# import robotparser

import scrapy.spiderloader
import scrapy.statscollectors
import scrapy.logformatter
import scrapy.dupefilters
import scrapy.squeues

import scrapy.extensions.spiderstate
import scrapy.extensions.corestats
import scrapy.extensions.telnet
import scrapy.extensions.logstats
import scrapy.extensions.memusage
import scrapy.extensions.memdebug
import scrapy.extensions.feedexport
import scrapy.extensions.closespider
import scrapy.extensions.debug
import scrapy.extensions.httpcache
import scrapy.extensions.statsmailer
import scrapy.extensions.throttle

import scrapy.core.scheduler
import scrapy.core.engine
import scrapy.core.scraper
import scrapy.core.spidermw
import scrapy.core.downloader

import scrapy.downloadermiddlewares.stats
import scrapy.downloadermiddlewares.httpcache
import scrapy.downloadermiddlewares.cookies
import scrapy.downloadermiddlewares.useragent
import scrapy.downloadermiddlewares.httpproxy
import scrapy.downloadermiddlewares.ajaxcrawl
# import scrapy.downloadermiddlewares.chunked 如果报错可以注释掉
import scrapy.downloadermiddlewares.decompression
import scrapy.downloadermiddlewares.defaultheaders
import scrapy.downloadermiddlewares.downloadtimeout
import scrapy.downloadermiddlewares.httpauth
import scrapy.downloadermiddlewares.httpcompression
import scrapy.downloadermiddlewares.redirect
import scrapy.downloadermiddlewares.retry
import scrapy.downloadermiddlewares.robotstxt

import scrapy.spidermiddlewares.depth
import scrapy.spidermiddlewares.httperror
import scrapy.spidermiddlewares.offsite
import scrapy.spidermiddlewares.referer
import scrapy.spidermiddlewares.urllength

import scrapy.pipelines

import scrapy.core.downloader.handlers.http
import scrapy.core.downloader.contextfactory

# 在项目中自己导入的类库(这个是我的项目用到的)
# import scrapy.pipelines.images
# from scrapy.pipelines.images import ImagesPipeline
# from scrapy.pipelines.media import MediaPipeline
from bingo_scrapy.items import TestScrapyItem
from bingo_scrapy.pipelines import TestScrapyPipeline
from bingo_scrapy.middlewares import TestScrapyDownloaderMiddleware
from bingo_scrapy.middlewares import TestScrapySpiderMiddleware
from bingo_scrapy.spiders.bingo import BingoSpider
from bingo_scrapy.settings import OPEN_DATE
from bingo_scrapy.settings import END_DAY
from bingo_scrapy.db import SQL

from datetime import date, datetime, timedelta
import csv

from itemadapter import ItemAdapter
import pdb
import json
import os
from datetime import date, datetime, timedelta
import logging

import os
import re
import scrapy
import queue
import threading
import requests
process = CrawlerProcess(get_project_settings())
process.crawl(BingoSpider)
process.start()
