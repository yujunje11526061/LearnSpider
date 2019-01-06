#!/usr/bin/env python
# -*- coding:utf-8 -*-

import requests
from requests.exceptions import ConnectionError
from ProxyPool.log import logger
from ProxyPool.db import RedisClient

'''
A basical function for getting webpage of agency.
'''

base_headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36',
    'Accept-Encoding': 'gzip, deflate, sdch',
    'Accept-Language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7'
}


def get_page(url, options={}):
    """
    :param url:
    :param additional entries of headers:
    :return:
    """
    headers = dict(base_headers, **options)
    logger.debug('Crawling: {}'.format(url))
    try:
        response = requests.get(url, headers=headers)
        logger.info('Finished crawling {}, status_code is {}'.format(url, response.status_code))
        if response.status_code == 200:
            return response.text
    except ConnectionError as e:
        logger.warning('Failed to crawl {} because of {}'.format(url, repr(e)))
        return None

def get_proxy():
    cli = RedisClient()
    return cli.random()

if __name__ == '__main__':
    proxy = get_proxy()
    print(type(proxy),proxy)
