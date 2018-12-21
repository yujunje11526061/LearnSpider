#!/usr/bin/env python
# -*- coding:utf-8 -*-
'''
selenium中经常会有人遇到的坑：
selenium.common.exceptions.StaleElementReferenceException: Message: Element not found in the cache - perhaps the page has changed since it was looked up

我循环去点击一列链接，但是只能点到第一个，第二个就失败了，为什么？”。原因就在这里：你点击第二个时已经是新页面，当然找不到之前页面的元素。这时，他会问“可是明明元素就在那里，没有变，甚至我是回退回来的，页面都没有变，怎么会说是新页面？这个就需要明白页面长得一样不代表就是同一张页面，就像两个人长得一样不一定是同一个人，他们的身份证号不同。页面，甚至页面上的元素都是有自己的身份证号（id）的。

'''
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from pyquery import PyQuery

uid = input("请输入账号：")
password = input("请输入密码：")

browser = webdriver.Chrome()
wait = WebDriverWait(browser,10)

browser.get("https://mail.zju.edu.cn/coremail/index.jsp")

user = wait.until(EC.presence_of_element_located((By.ID, 'uid')))
psw = wait.until(EC.presence_of_element_located((By.ID, 'password')))
submit = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "body > div.main > div.aside > div.loginArea.normalForm > div.content-wrapper > div.formLogin > form > div:nth-child(15) > button")))

user.clear()
psw.clear()
user.send_keys(uid)
psw.send_keys(password)
submit.click()