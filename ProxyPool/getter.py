#!/usr/bin/env python
# -*- coding:utf-8 -*-

from ProxyPool.tester import Tester
from ProxyPool.db import RedisClient
from ProxyPool.crawler import Crawler
from ProxyPool.setting import *
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
        判断是否达到了代理池限制
        """
        if self.redis.count() >= POOL_UPPER_THRESHOLD:
            return True
        else:
            return False
    
    def run(self):
        print('获取器开始执行')
        if not self.is_over_threshold():
            for callback_label in range(self.crawler.__CrawlFuncCount__):
                callback = self.crawler.__CrawlFunc__[callback_label]
                # 获取代理
                proxies = self.crawler.get_proxies(callback)
                sys.stdout.flush()
                for proxy in proxies:
                    self.redis.add(proxy)
