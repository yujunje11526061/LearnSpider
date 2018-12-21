#!/usr/bin/env python
# -*- coding:utf-8 -*-
import requests, re
from requests import session


def main():
    uid = input("请输入账号：")
    password = input("请输入密码：")
    s = session()
    url = "https://mail.zju.edu.cn/coremail/index.jsp?cus=1"
    header = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        'Content-Length': '243',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Cookie': 'locale=zh_CN; face=undefined',
        'Host': 'mail.zju.edu.cn',
        'Origin': 'https://mail.zju.edu.cn',
        'Referer': 'https://mail.zju.edu.cn/coremail/index.jsp?cus=1',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'
    }
    data = {'locale': 'zh_CN',
            'nodetect': 'false',
            'destURL': '',
            'supportLoginDevice': 'true',
            'accessToken': '',
            'timestamp': '',
            'signature': '',
            'nonce': '',
            'device': '',
            'supportDynamicPwd': 'true',
            'supportBind2FA': 'true',
            'authorizeDevice': '',
            'uid': uid,
            'password': password,
            'hiddenUseSSL': 'true',
            'useSSL': 'true',
            'action:login': ''
            }

    resp = s.post(url, headers=header, data=data)
    # print(resp.status_code)
    # print(resp.text)
    text = resp.text
    try:
        r1 = re.search('mainUrl.*;', text).group()
    except:
        print("登陆失败！请检查账号密码")
        return 0
    mainUrl = re.search('".*"', r1).group().strip('\"')
    _, sid = mainUrl.split("=")
    # print(mainUrl)
    response = s.get(mainUrl)
    # print(response.status_code)
    # print(response.text)
    urlForUnread = "https://mail.zju.edu.cn/coremail/XT5/jsp/mail.jsp?func=searchMessages&sid=" + sid
    print(urlForUnread)
    dataForUnread = {
        'start': '0',
        'limit': '100',
        'refresh': 'true',
        'read': 'false'
    }
    result = s.post(urlForUnread, data=dataForUnread).json()
    if len(result.get("var",[]))==0:
        print("无未读邮件。")
        return 1
    for d in result.get("var", []):
        print("时间：{}\n发件人：{}\n主题：{}\n摘要：{}\n".format(d.get("receivedDate"), d.get("from"), d.get("subject"),
                                                     d.get("summary")))
    return 1


if __name__ == "__main__":
    while main()==0:
        print("请重新登陆")
