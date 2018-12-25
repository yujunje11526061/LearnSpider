#!/usr/bin/env python
# -*- coding:utf-8 -*-

from ProxyPool.tester import Tester
from ProxyPool.db import RedisClient
from ProxyPool.crawler import Crawler
from ProxyPool.setting import *
from ProxyPool.log import logger
import sys

'''
Build a 'Getter' for getting proxies. 
The implementation details are realized by Class 'Crawler' in module 'crawler'.
'''

class Getter():
    def __init__(self):
        self.redis = RedisClient()
        self.crawler = Crawler()
    
    def is_over_threshold(self):
        """
        Compare to the capacity of proxy pool.
        """
        if self.redis.count() >= POOL_UPPER_THRESHOLD:
            return True
        else:
            return False
    
    def run(self):
        logger.debug('Getter is running.')
        if not self.is_over_threshold():
            for callback_label in range(self.crawler.__CrawlFuncCount__):
                callback = self.crawler.__CrawlFunc__[callback_label]
                # 获取代理
                proxies = self.crawler.get_proxies(callback)
                sys.stdout.flush()
                for proxy in proxies:
                    self.redis.add(proxy)
