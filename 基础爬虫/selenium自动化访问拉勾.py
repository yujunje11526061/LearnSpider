#!/usr/bin/env python
# -*- coding:utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from pyquery import PyQuery


def main(totPageNum):
    global browser, wait
    inp = browser.find_element_by_xpath('//*[@id="changeCityBox"]/ul/li[3]/a')
    inp.click()
    inp = browser.find_element_by_id("search_input")
    inp.send_keys("python")
    inp = browser.find_element_by_id("search_button")
    inp.click()
    time.sleep(2)
    for i in range(totPageNum):
        doc = PyQuery(browser.page_source)
        inp = browser.find_elements_by_class_name("con_list_item")
        inp = doc(".con_list_item")
        write(i, inp)
        browser.find_element_by_class_name("pager_next").click()
        time.sleep(2)
    return

def write(page, inp):
    global wait, browser
    with open(r"C:\Users\jjff1\Desktop\xx.txt", "a", encoding="utf-8") as f:
        for item in inp.items():
            index = int(item.attr("data-index"))+1
            s = "{: <6}{: <20}{: >10}{: >10}\n".format(index+page*15, item.attr("data-positionname"), item.attr(
                "data-company"), item.attr("data-salary"))
            print(s,end="")
            f.write(s)
            browser.find_element_by_css_selector(f"#s_position_list > ul > li:nth-child({index}) > div.list_item_top > div.position > div.p_top > a > h3").click()
            wait.until(EC.new_window_is_opened)
            browser.switch_to_window(browser.window_handles[1])
            description = browser.find_element_by_css_selector("#job_detail > dd.job_bt > div")
            print(description.text)
            f.write(description.text+"\n")
            browser.execute_script("window.close()")
            browser.switch_to_window(browser.window_handles[0])
    time.sleep(2)


if __name__ == "__main__":
    browser = webdriver.Chrome()
    wait = WebDriverWait(browser, 10)
    wait.until(EC.new_window_is_opened)
    browser.get("https://lagou.com")
    # browser.implicitly_wait(1)
    main(5)
