#!/usr/bin/env python
# -*- coding:utf-8 -*-
from fake_useragent import UserAgent
from pymongo import MongoClient
import requests
import time, datetime


def getPosition(pageCount, job):
    mongo = MongoClient()
    dbname = job
    db = mongo.get_database(name=dbname)
    now = datetime.datetime.now()
    col_name = "{}年{}月{}日".format(now.year, now.month, now.day)
    # 清除该库中已有的同名集合
    try:
        db.drop_collection(col_name)
    except:
        pass
    col = db.get_collection(name=col_name)

    # 此处city代码表示杭州
    url = 'https://www.lagou.com/jobs/positionAjax.json?city=%E6%9D%AD%E5%B7%9E&needAddtionalResult=false&isSchoolJob=1'
    ua = UserAgent()
    positionCount = 0
    for pageNumber in range(1, pageCount + 1):
        headers = {
            "cookie": 'JSESSIONID=ABAAABAAADEAAFID177532A79CF19A16C2CA76A3CFD81A0; _ga=GA1.2.2028873935.1541216172; _gid=GA1.2.1557710700.1541216172; Hm_lvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1541216173; user_trace_token=20181103113613-9d0564cd-df19-11e8-84c5-525400f775ce; LGUID=20181103113613-9d0567fd-df19-11e8-84c5-525400f775ce; X_HTTP_TOKEN=ffd00611a904c728f8de685362aebb1d; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%22166d7a48a7d737-08526cd5e8eecd-9393265-2359296-166d7a48a7edc9%22%2C%22%24device_id%22%3A%22166d7a48a7d737-08526cd5e8eecd-9393265-2359296-166d7a48a7edc9%22%7D; sajssdk_2015_cross_new_user=1; LG_LOGIN_USER_ID=647598386a924448b965b5c6f29c61281a9027312995b281c6a3841a77403bf9; _putrc=CF068031FFA2A79C123F89F2B170EADC; login=true; unick=%E4%BD%99%E9%AA%8F%E6%9D%B0; showExpriedIndex=1; showExpriedCompanyHome=1; showExpriedMyPublish=1; hasDeliver=1; index_location_city=%E6%9D%AD%E5%B7%9E; LGSID=20181103130713-53710bd3-df26-11e8-85e9-5254005c3644; PRE_UTM=; PRE_HOST=; PRE_SITE=https%3A%2F%2Fwww.lagou.com%2Fjobs%2Flist_%3FlabelWords%3D%26fromSearch%3Dtrue%26suginput%3D; PRE_LAND=https%3A%2F%2Fwww.lagou.com%2Fjobs%2Flist_python%3Fcity%3D%25E6%259D%25AD%25E5%25B7%259E%26cl%3Dfalse%26fromSearch%3Dtrue%26labelWords%3D%26suginput%3D; TG-TRACK-CODE=search_code; gate_login_token=1ca5a59d592a7c38329426ba5f99d0000c8071c96a5cf3270921bbde43704fca; _gat=1; Hm_lpvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1541222494; LGRID=20181103132134-54acce2a-df28-11e8-84fc-525400f775ce; SEARCH_ID=f2a3becf71034beab71c4f6f15fc4fdb',
            "Host": "www.lagou.com",
            "Referer": "https://www.lagou.com/jobs/list_python?city=%E6%9D%AD%E5%B7%9E&cl=false&fromSearch=true&labelWords=&suginput=&isSchoolJob=1",
            "User-Agent": ua.random
        }

        data = {
            "first": "true",
            "pn": pageNumber,
            "kd": job
        }
        print('爬取关于{}职位的第{}页内容'.format(job, pageNumber))
        response = requests.post(url, headers=headers, data=data)
        if response.status_code != 200:
            print('status_code:', response.status_code)
            return
        r = response.json()['content']['positionResult']['result']
        if len(r) == 0:
            print('所有记录不足{}页，共爬取记录{}条'.format(pageCount,positionCount))
            return
        print('关于{}职位的第{}页内容爬取完毕'.format(job, pageNumber))
        positionCount += len(r)
        col.insert_many(r)
        waittime = 3
        print("等待%d秒" % waittime)
        time.sleep(waittime)

    print("共有关于{}岗位的记录{}条，并获取前{}条岗位信息".format(job,response.json()['content']['positionResult']['totalCount'], positionCount))


if __name__ == "__main__":
    pageCount = 35
    job = 'java'
    getPosition(pageCount, job)
