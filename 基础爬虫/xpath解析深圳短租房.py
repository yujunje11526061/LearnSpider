#!/usr/bin/env.python
# -*- coding:utf-8 -*-
import requests
from lxml import etree
import pandas as pd

r = requests.get('http://sz.xiaozhu.com/').text
s = etree.HTML(r)
price = s.xpath('//*[@id="page_list"]/ul/li/div[2]/span[1]/i/text()') # *表示通配符，表示所有标签，可以指定某个特定标签下取属性
latlng = s.xpath('//*[@id="page_list"]/ul/li/@latlng')
address = s.xpath('//*[@id="page_list"]/ul/li/div[2]/div/a/span/text()')
# print(latlng)
# print(address)
data = {'latlng':latlng, 'price':price}
df = pd.DataFrame(data, index=address).sort_values('price')

df.to_csv('C:\\Users\\jjff1\\Desktop\\pr.csv', encoding = 'utf_8_sig')
