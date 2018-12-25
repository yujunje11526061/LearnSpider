#!/usr/bin/env python
# -*- coding:utf-8 -*-

import asyncio
import aiohttp
import time
import sys

try:
    from aiohttp import ClientError
except:
    from aiohttp import ClientProxyConnectionError as ProxyConnectionError
from ProxyPool.db import RedisClient
from ProxyPool.setting import *
from ProxyPool.log import logger

'''
Build a 'Tester' for testing the availability of all the proxies. 
'''


class Tester:
    def __init__(self):
        self.redis = RedisClient()

    async def test_single_proxy(self, proxy):
        """
        Test the availability of a proxy.
        And maximize its score if available else decrease its score.
        :param proxy
        :return
        """
        conn = aiohttp.TCPConnector(verify_ssl=False)
        async with aiohttp.ClientSession(connector=conn) as session:
            try:
                if isinstance(proxy, bytes):
                    proxy = proxy.decode('utf-8')
                real_proxy = 'http://' + proxy  # url应包括协议，浏览器访问不加协议会默认用http
                logger.debug('Testing {}'.format(proxy))
                async with session.get(TEST_URL, proxy=real_proxy, timeout=15, allow_redirects=False) as response:
                    if response.status in VALID_STATUS_CODES:
                        logger.debug('Proxy {} is OK'.format(proxy))
                        self.redis.maximize(proxy)
                    else:
                        logger.warning(
                            'Failed to use proxy {} because the response code was {}'.format(proxy, response.status))
                        self.redis.decrease(proxy)
            except (ClientError, aiohttp.client_exceptions.ClientConnectorError, asyncio.TimeoutError, AttributeError) as e:
                self.redis.decrease(proxy)
                logger.warning('Failed to use proxy {} because of {}'.format(proxy, repr(e)))

    def run(self):
        """
        Run tester.
        :return:
        """
        logger.debug('Tester is running.')
        try:
            count = self.redis.count()
            logger.info('There are {} proxy (proxies) in proxy pool now.'.format(count))
            for i in range(0, count, BATCH_TEST_SIZE):
                start = i
                stop = min(i + BATCH_TEST_SIZE, count)
                # 分批测试防止内存开销过大
                logger.debug('Testing proxies with index between {} and {}.'.format(start + 1,  stop))
                test_proxies = self.redis.batch(start, stop)
                # 异步测试加快速度
                loop = asyncio.get_event_loop()
                tasks = [self.test_single_proxy(proxy) for proxy in test_proxies]
                loop.run_until_complete(asyncio.wait(tasks))
                sys.stdout.flush()
                time.sleep(5)
            logger.info('Testing finished')

        except Exception as e:
            logger.warning('Tester error {}'.format(e.args))
