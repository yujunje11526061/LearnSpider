#!/usr/bin/env python
# -*- coding:utf-8 -*-

import redis
from ProxyPool.error import PoolEmptyError
from ProxyPool.setting import REDIS_HOST, REDIS_PORT, REDIS_PASSWORD, REDIS_KEY
from ProxyPool.setting import MAX_SCORE, MIN_SCORE, INITIAL_SCORE
from ProxyPool.log import logger
from random import choice
import re


class RedisClient(object):
    def __init__(self, host=REDIS_HOST, port=REDIS_PORT, password=REDIS_PASSWORD):
        """
        Connect to redis server.
        :param host: Redis IP
        :param port: Redis port
        :param password: Redis password
        """
        self.db = redis.StrictRedis(host=host, port=port, password=password, decode_responses=True)

    def add(self, proxy, score=INITIAL_SCORE):
        """
        Add a proxy
        :param proxy
        :param score
        :return: adding result
        """
        if not re.match('\d+\.\d+\.\d+\.\d+\:\d+', proxy):
            logger.debug('Illegal proxy {} is deprecated'.format(proxy))
            return
        if not self.db.zscore(REDIS_KEY, proxy):
            return self.db.zadd(REDIS_KEY, {proxy: score})

    def random(self):
        """
        Choose a proxy in random, and anyone with MAX_SCORE is preferenced.
        if no proxy has MAX_SCORE, use the one with the highest score, else raise PoolEmptyError.
        :return: a random proxy.
        """
        result = self.db.zrangebyscore(REDIS_KEY, MAX_SCORE, MAX_SCORE)
        if len(result):
            return choice(result)
        else:
            result = self.db.zrevrange(REDIS_KEY, 0, 100)
            if len(result):
                return choice(result)
            else:
                raise PoolEmptyError

    def decrease(self, proxy):
        """
        Decrease the score of proxy by 1
        Any proxy with score lower than MIN_SCORE will be removed.
        :param proxy
        :return: the modified score of proxy
        """
        score = self.db.zscore(REDIS_KEY, proxy)
        if score and score > MIN_SCORE:
            logger.debug('Proxy {} with score {} - 1.'.format(proxy, int(score)))
            return self.db.zincrby(REDIS_KEY, -1, proxy)
        else:
            logger.debug('Proxy {} with score {} is removed.'.format(proxy, int(score)))
            return self.db.zrem(REDIS_KEY, proxy)

    def exists(self, proxy):
        """
        判断是否存在
        :param proxy: 代理
        :return: 是否存在
        """
        return not self.db.zscore(REDIS_KEY, proxy) == None

    def maximize(self, proxy):
        """
        Maximize the score of proxy
        :param proxy
        :return
        """
        logger.debug('Set proxy {} by maximum score {}'.format(proxy, MAX_SCORE))
        return self.db.zadd(REDIS_KEY, {proxy: MAX_SCORE})

    def count(self):
        """
        Count the number of proxy in proxy pool.
        :return: total number
        """
        return self.db.zcard(REDIS_KEY)

    def all(self):
        """
        List all the proxies.
        :return: a list
        """
        return self.db.zrangebyscore(REDIS_KEY, MIN_SCORE, MAX_SCORE)

    def batch(self, start, stop):
        """
        Get proxy by batch.
        :param start: the start index of proxy
        :param stop: the end index of proxy
        :return: a list of this batch
        """
        return self.db.zrevrange(REDIS_KEY, start, stop - 1)


if __name__ == '__main__':
    conn = RedisClient()
    result_1 = conn.batch(680, 688)
    result_2 = conn.db.zrangebyscore(REDIS_KEY, MAX_SCORE, MAX_SCORE)
    logger.info('There are {} proxies with MAX_SCORE'.format(len(result_2)))
