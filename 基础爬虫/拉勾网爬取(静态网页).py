#!/usr/bin/env python
# -*- coding:utf-8 -*-
import requests, time
import pandas as pd
from lxml import etree
from fake_useragent import UserAgent
import datetime


def getPosition(pageCount, job, city):
    ua = UserAgent()
    salary = []
    company = []
    positionName = []
    companyDescription = []
    companyTag = []
    companyPage = []
    companyCategory = []
    releaseTime = []
    district = []
    condition = []
    for pageNumber in range(1, pageCount + 1):
        url = "https://www.lagou.com/zhaopin/{}/{}?city={}".format(job, pageNumber, city)
        headers = {
            "Cookie": "JSESSIONID=ABAAABAAADEAAFID177532A79CF19A16C2CA76A3CFD81A0; _ga=GA1.2.2028873935.1541216172; _gid=GA1.2.1557710700.1541216172; Hm_lvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1541216173; user_trace_token=20181103113613-9d0564cd-df19-11e8-84c5-525400f775ce; LGUID=20181103113613-9d0567fd-df19-11e8-84c5-525400f775ce; X_HTTP_TOKEN=ffd00611a904c728f8de685362aebb1d; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%22166d7a48a7d737-08526cd5e8eecd-9393265-2359296-166d7a48a7edc9%22%2C%22%24device_id%22%3A%22166d7a48a7d737-08526cd5e8eecd-9393265-2359296-166d7a48a7edc9%22%7D; sajssdk_2015_cross_new_user=1; LG_LOGIN_USER_ID=647598386a924448b965b5c6f29c61281a9027312995b281c6a3841a77403bf9; _putrc=CF068031FFA2A79C123F89F2B170EADC; login=true; unick=%E4%BD%99%E9%AA%8F%E6%9D%B0; showExpriedIndex=1; showExpriedCompanyHome=1; showExpriedMyPublish=1; hasDeliver=1; index_location_city=%E6%9D%AD%E5%B7%9E; LGSID=20181103154722-b3013286-df3c-11e8-85ec-5254005c3644; PRE_UTM=; PRE_HOST=; PRE_SITE=https%3A%2F%2Fwww.lagou.com%2Fjobs%2Flist_python%3Fcity%3D%25E6%259D%25AD%25E5%25B7%259E%26cl%3Dfalse%26fromSearch%3Dtrue%26labelWords%3D%26suginput%3D%26isSchoolJob%3D1; PRE_LAND=https%3A%2F%2Fwww.lagou.com%2Fjobs%2Flist_java%3Fcity%3D%25E6%259D%25AD%25E5%25B7%259E%26cl%3Dfalse%26fromSearch%3Dtrue%26labelWords%3D%26suginput%3D%26isSchoolJob%3D1; gate_login_token=945bc0435b60788fe37ec10f2cd174faee4da727b32398bbf5af6d5016cd56b5; _gat=1; TG-TRACK-CODE=search_code; SEARCH_ID=c1d5289856d843df994236b692a29629; Hm_lpvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1541232570; LGRID=20181103160930-ca531add-df3f-11e8-85ec-5254005c3644",
            "Host": "www.lagou.com",
            "Origin": "https://www.lagou.com",
            "Referer": "https://www.lagou.com/zhaopin/Java/1/",
            "User-Agent": ua.random
        }
        print("开始爬取{}岗位的第{}页记录".format(job, pageNumber))
        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            break
        r = etree.HTML(response.text)
        salary.extend(r.xpath('//*[@id="s_position_list"]/ul/li/@data-salary'))
        company.extend(r.xpath('//*[@id="s_position_list"]/ul/li/@data-company'))
        positionName.extend(r.xpath('//*[@id="s_position_list"]/ul/li/@data-positionname'))
        companyDescription.extend(r.xpath('//*[@id="s_position_list"]/ul/li/div[2]/div[2]/text()'))
        companyPage.extend(r.xpath('//*[@id="s_position_list"]/ul/li/div[1]/div[3]/a/@href'))
        companyCategory.extend(r.xpath('//*[@id="s_position_list"]/ul/li/div[1]/div[2]/div[2]/text()'))
        releaseTime.extend(r.xpath('//*[@id="s_position_list"]/ul/li/div[1]/div[1]/div[1]/span/text()'))
        district.extend(r.xpath('//*[@id="s_position_list"]/ul/li/div[1]/div[1]/div[1]/a/span/em/text()'))
        condition.extend(r.xpath('//*[@id="s_position_list"]/ul/li/div[1]/div[1]/div[2]/div/text()'))
        print("{}岗位的第{}页记录爬取完毕".format(job, pageNumber))
        waitTime = 3
        print('等待%d秒' % waitTime)
        time.sleep(waitTime)
    print("爬取完毕，共计得到记录{}条".format(len(salary)))
    condition = list(map(lambda x:x.strip("\n "), condition[2::3]))
    companyCategory = list(map(lambda x:x.strip("\n "), companyCategory))
    data = {
        # "positionName": positionName,
        "salary": salary,
        "district": district,
        "condition": condition,
        "company": company,
        "companyCategory": companyCategory,
        "companyDescription": companyDescription,
        "companyPage": companyPage,
        "releaseTime": releaseTime
    }
    df = pd.DataFrame(data, index=positionName).sort_values(['district', 'releaseTime'])
    return df


if __name__ == "__main__":
    pageCount = 30
    job = 'Python'
    city = '杭州'
    df = getPosition(pageCount, job, city)
    now = datetime.datetime.now()
    path = r"C:\Users\jjff1\Desktop\{:0>4}.{:0>2}.{:0>2}{}{}岗位招聘信息.csv".format(now.year,now.month,now.day,city,job)
    df.to_csv(path, encoding='utf_8_sig')
