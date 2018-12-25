#!/usr/bin/env python
# -*- coding:utf-8 -*-

import time
from multiprocessing import Process
from ProxyPool.api import app
from ProxyPool.getter import Getter
from ProxyPool.tester import Tester
from ProxyPool.log import logger
from ProxyPool.setting import *


class Scheduler():
    def schedule_tester(self, cycle=TESTER_CYCLE):
        """
        Test proxies periodically
        """
        tester = Tester()
        while True:
            logger.info('Tester begins to run.')
            tester.run()
            time.sleep(cycle)
    
    def schedule_getter(self, cycle=GETTER_CYCLE):
        """
        Get proxies periodically
        """
        getter = Getter()
        while True:
            logger.info('Getter begins to run.')
            getter.run()
            time.sleep(cycle)
    
    def schedule_api(self):
        """
        Providing API
        """
        app.run(API_HOST, API_PORT, debug=True)
    
    def run(self):
        logger.info('Proxy pool management system begins to run.')
        
        if TESTER_ENABLED:
            tester_process = Process(target=self.schedule_tester)
            tester_process.start()
        
        if GETTER_ENABLED:
            getter_process = Process(target=self.schedule_getter)
            getter_process.start()
        
        if API_ENABLED:
            api_process = Process(target=self.schedule_api)
            api_process.start()
