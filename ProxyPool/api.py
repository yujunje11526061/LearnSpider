#!/usr/bin/env python
# -*- coding:utf-8 -*-

from flask import Flask, g

from ProxyPool.db import RedisClient

# 可暴露接口的白名单
__all__ = ['app']

app = Flask(__name__)


def get_conn():
    if not hasattr(g, 'redis'):
        g.redis = RedisClient()
    return g.redis


@app.route('/')
def index():
    return '<h2>Welcome to Proxy Pool Management System</h2>'


@app.route('/random')
def get_proxy():
    """
    Get a proxy
    :return: a random proxy
    """
    conn = get_conn()
    return conn.random()


@app.route('/count')
def get_counts():
    """
    Get the count of proxies
    :return: the total number of proxies
    """
    conn = get_conn()
    return str(conn.count())


if __name__ == '__main__':
    app.run(debug=True)
