#!/usr/bin/env python
# -*- coding:utf-8 -*-

import logging

logger = logging.getLogger('getProxies')
logger.setLevel(logging.DEBUG)

formatter = logging.Formatter(fmt='%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s')

std = logging.StreamHandler()
std.setLevel(logging.DEBUG)
std.setFormatter(formatter)

file = logging.FileHandler('getProxies.log')
file.setLevel(logging.INFO)
file.setFormatter(formatter)

logger.addHandler(std)
logger.addHandler(file)