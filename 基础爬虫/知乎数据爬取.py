# #!/usr/bin/env.python
# # -*- coding:utf-8 -*-
import requests, time
import pandas as pd

headers = {
    'authority': 'www.zhihu.com',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36',
    'x-udid': 'AACoDn_Wcw6PTtckbdUX8X7JAG5F1AWh0fE='
}


def get_followees(num: int):
    followees = []
    for i in range(num):
        url = r'https://www.zhihu.com/api/v4/members/jiang-zhan-95-72/followees?include=data%5B*%5D.answer_count%2Carticles_count%2Cgender%2Cfollower_count%2Cis_followed%2Cis_following%2Cbadge%5B%3F(type%3Dbest_answerer)%5D.topics&offset={}&limit=20'.format(i * 20)
        try:
            response = requests.get(url, headers=headers)
            r = response.json()['data']
            print('爬取史gay关注的人第{}页，状态码{}'.format(i + 1, response.status_code))
            followees.extend(r)
            time.sleep(1)
        except:
            break
    return followees


def get_follow_questions(num: int):
    follow_questions = []
    for i in range(num):
        url = r'https://www.zhihu.com/api/v4/members/jiang-zhan-95-72/following-questions?include=data%5B*%5D.created%2Canswer_count%2Cfollower_count%2Cauthor&offset={}&limit=20'.format(i * 20)
        try:
            response = requests.get(url, headers=headers)
            r = response.json()['data']
            print('爬取史gay关注的问题第{}页，状态码{}'.format(i + 1, response.status_code))
            follow_questions.extend(r)
            time.sleep(1)
        except:
            break
    return follow_questions


if __name__ == '__main__':
    num = 20
    followees = get_followees(num)
    follow_questions = get_follow_questions(num)
    df1 = pd.DataFrame.from_dict(followees)
    df2 = pd.DataFrame.from_dict(follow_questions)
    df1.to_csv('C:\\Users\\jjff1\\Desktop\\followees.csv', encoding='utf-8-sig')
    df2.to_csv('C:\\Users\\jjff1\\Desktop\\follow_questions.csv', encoding='utf-8-sig')
