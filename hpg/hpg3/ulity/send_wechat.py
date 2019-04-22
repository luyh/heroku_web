#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
from china_time import ChinaTime

def send_wechat(title,content):
    now = ChinaTime().getChinaTime()
    text = {'text': title, 'desp': content +'\n\n'+ now}
    try:
        response = requests.post('',\
                      data= text )
        print(response.content)
        print(text)
    except:
        print('发送微信报错')


if __name__ == '__main__':
    send_wechat('wechat title','微信测试内容')