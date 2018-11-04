#!/usr/bin/env.python
# -*- coding:utf-8 -*-
'''
为了识别 Unicode 文件，Microsoft 建议所有的 Unicode 文件应该以 ZERO WIDTH NOBREAK SPACE字符开头。
这作为一个”特征符”或”字节顺序标记（byte-order mark，BOM）”来识别文件中使用的编码和字节顺序

As UTF-8 is an 8-bit encoding no BOM is required and anyU+FEFF character in the decoded Unicode string
 (even if it’s the firstcharacter) is treated as a ZERO WIDTH NO-BREAK SPACE.

UTF-8以字节为编码单元，它的字节顺序在所有系统中都是一样的，没有字节序的问题，也因此它实际上并不需要BOM(“ByteOrder Mark”), 但是UTF-8 with BOM即utf-8-sig需要提供BOM（"ByteOrder
 Mark"）。

Python 'utf-8-sig' Codec
This work similar to UTF-8 with the following changes:

* On encoding/writing a UTF-8 encoded BOM will be prepended/written as the
  first three bytes.

* On decoding/reading if the first three bytes are a UTF-8 encoded BOM, these
  bytes will be skipped.
'''

import requests
from bs4 import BeautifulSoup  # 用美丽汤解析
import pandas as pd

url1 = 'https://book.douban.com/subject/2130190/comments' # 短评
url2 = 'https://book.douban.com/subject/2130190/reviews'  # 长评
path = 'C:\\Users\\jjff1\\Desktop\\'
name = 'comment'
type = '.csv'

r = requests.get(url1).text
soup = BeautifulSoup(r, 'lxml')
pattern = soup.find_all('p', 'comment-content')
comment = []
for item in pattern:
    print(item.text)
    comment.append(item.text)

df = pd.DataFrame(comment)
df.to_csv(path+name+type, encoding = 'utf_8_sig')

