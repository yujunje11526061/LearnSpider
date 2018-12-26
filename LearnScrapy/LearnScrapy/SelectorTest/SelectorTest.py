#!/usr/bin/env python
# -*- coding:utf-8 -*-

from scrapy import Selector, crawler
from pyquery import PyQuery
from scrapy.http import Request, Response

with open('forTest.html', encoding='utf-8') as f:
    text = f.read()

sel = Selector(text = text)
pqSel = PyQuery(text)  # PyQuery继承自list

# scrapy自带的css选择器和xpath选择器，每次选择返回的都是选择器列表，要从列表中取
# scrapy产生的response对象自带css方法和xpath方法，可以方便地直接进行解析。
# Response类和Resquest类提供了很多内置属性及方法，源码在scrapy.http目录下

#---------------------------------------------------------------
# 用css选择器, 主要由按照class获取，按id获取(唯一性)，按标签获取，通配符*
cssResult = []
cssResult.append(sel.css(".top").css("div>div::text").extract()[0])  # ::text 脱壳取文本，::attr(href) 取href属性
# cssResult.append(sel.css(".top>div>div").extract()[0])  如果中间没啥别的处理，可以把多个query合起来写
cssResult.append(sel.css("#li_a_div::text").extract_first())
print("css选择器得到的对象是SelectorList对象，SelectorList是list的子类吗？", issubclass(sel.css(".top").css("div>div").__class__, list), end='\n\n')  # 输出True

#---------------------------------------------------------------
# 用xpath选择器，类似文档路径的写法，用'/'，'.'，'..'，'//'表示当前节点下所有满足后面条件的节点, '@'取属性
xpathResult = []
xpathResult.append(sel.xpath("/html/body/ul/li[2]/div/div/text()").extract()[0])
xpathResult.append(sel.xpath('//*[@id="li_a_div"]/text()').extract()[0])
print("xpath选择器得到的对象是SelectorList对象，SelectorList是list的子类吗？", issubclass(sel.xpath('//*[@id="li_a_div"]/text()').__class__, list), end='\n\n')  # 输出True

#---------------------------------------------------------------
# pyquery选择器，类似css选择器的语法。每一步得到一个新的PyQuery对象，可以用items()方法取得生成器，用text()方法取文本，用attr()方法取属性，没有属性会自动处理成None
pyqueryResult = []
pyqueryResult.append(pqSel(".top>div>div").text())
pyqueryResult.append(pqSel("#li_a_div").text())
item = pqSel("li") # item依然是一个PyQuery对象,可以继续用item('标签名')这样的方法挖下去
print('item = pqSel("li"), item的类型是:', type(item),"\nitem和pqSel都属于一个类吗?", item.__class__ is pqSel.__class__, end = '\n\n') # 输出True
# 对item.items()取生成器，从而可以分别处理每个内容
print("打印item下的文本内容：", list(map(lambda x:x.text(), item.items())), end= '\n\n')


print("{}\n{}\n{}".format(cssResult,xpathResult,pyqueryResult))
'''
输出结果
['li的div的div', 'li的a的div']
['li的div的div', 'li的a的div']
['li的div的div', 'li的a的div']

可见，css选择器需要手动脱壳来处理掉标签。xpath选择器适用于结构清晰的页面，但也要脱壳。每一步得到的是SelectorList对象，是list的子类，可以按列表的方法取、切片等。
pyquery选择器类似css选择器，attr()取属性，text()取文本方便。每一步得到的是新的PyQuery对象。包含多个子节点时先用items()方法取生成器。
'''