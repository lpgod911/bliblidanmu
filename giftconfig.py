# -*- coding: utf-8 -*-
"""
Created on Sat Dec  5 22:43:01 2020

@author: 鹏

    获取bilibili直播间礼物列表
    房间号从网页源代码中获取
    打开直播画面后，按ctrl+u 打开网页源代码，按ctrl+f 搜索 room_id
    搜到的"room_id":1016中，1016就是房间号 
"""

import requests;
import time;
import win32com.client

global Giftdict1,Giftdict2
Giftdict1 = {}
Giftdict2 = {}


class gift():
    def __init__(self):
        # 弹幕url
        self.url = 'https://api.live.bilibili.com/xlive/web-room/v1/giftPanel/giftConfig?platform=pc&room_id=22616007';
        # 请求头
        self.headers = {
            'Host':'api.live.bilibili.com',
            'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:78.0) Gecko/20100101 Firefox/78.0',
        }

    def get_gift(self):
        # 获取直播间礼物
        html = requests.get(url=self.url,headers=self.headers).json();
#        # 解析礼物列表
        for content in html['data']['list']:
            # 获取投币类型
            gift_type = content['coin_type'];
            # 获取礼物名称
            gift_name = content['name'];
            # 获取价格
            gift_price = content['price'];
            Giftdict1[gift_name] = gift_price
            Giftdict2[gift_name] = gift_type

if __name__ == '__main__':
    gift().get_gift()
