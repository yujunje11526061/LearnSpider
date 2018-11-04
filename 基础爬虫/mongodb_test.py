#!/usr/bin/env python
# -*- coding:utf-8 -*-
from pymongo import MongoClient
# client = MongoClient("mongodb://username:password@host:port/dbname")   用特定账号登陆特定主机上的某个数据库。无参数则连接到本地主机的默认端口
client = MongoClient()
db = client.test   #连接test数据库，没有则自动创建
my_set = db.set   #使用set集合，没有则自动创建
my_set.insert({'name':'Vinie','age':24})   #插入一条数据