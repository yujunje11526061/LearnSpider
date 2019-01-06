#!/usr/bin/env python
# -*- coding:utf-8 -*-
from scrapy import cmdline
spiderNeedToRun = "spider_city_58"
exe = "scrapy crawl "+ spiderNeedToRun
cmdline.execute(exe.split())
# 字符串组成的列表传进去可以被正常
# 执行，传原始指令的字符串形式可能会因为环境不同而无法运行。或者直接在命令行的项目目录下输入scrapy crawl 爬虫名