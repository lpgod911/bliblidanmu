# -*- coding: utf-8 -*-
"""
Created on Sat Dec  5 22:43:01 2020

@author: 鹏
"""

# -*- coding:utf-8 -*-
# 时间:2020/8/3
# 作者:猫先生的早茶
"""
    获取bilibili直播间弹幕
    房间号从网页源代码中获取
    打开直播画面后，按ctrl+u 打开网页源代码，按ctrl+f 搜索 room_id
    搜到的"room_id":1016中，1016就是房间号 
    获取不同房间的弹幕:修改代码第26行的roomid的值为对应的房间号
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
        # 获取直播间弹幕
        html = requests.get(url=self.url,headers=self.headers).json();
#        # 解析弹幕列表
        for content in html['data']['list']:
            

            # 获取昵称
            gift_type = content['coin_type'];
            gift_name = content['name'];
            # 获取发言
            gift_price = content['price'];
            
            Giftdict1[gift_name] = gift_price
            Giftdict2[gift_name] = gift_type

if __name__ == '__main__':
    gift().get_gift()
#    giftprice=GIFTDICT1.get('“棋”开得胜')
#    gifttype=GIFTDICT2.get('“棋”开得胜')
#    print(giftprice)
#    print(gifttype)
