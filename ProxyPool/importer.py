#!/usr/bin/env python
# -*- coding:utf-8 -*-

from ProxyPool.db import RedisClient

'''
This program provides a entrance for adding proxy manually.
'''

conn = RedisClient()

def set(proxy):
    result = conn.add(proxy)
    logger.info(proxy)
    logger.info("Adding proxy "+'succeeded.' if result else 'failed.')


def scan():
    logger.info('Please input the proxy, or input "exit" to exit')
    while True:
        proxy = input()
        if proxy == 'exit':
            break
        set(proxy)


if __name__ == '__main__':
    scan()
