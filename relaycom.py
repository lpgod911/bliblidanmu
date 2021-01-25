# -*- coding: utf-8 -*-
"""
Created on Fri Nov 13 16:59:35 2020

@author: 鹏
"""

# coding=utf-8
import os
import serial
import time
#import random
# 定义本模块（本.py文件)需要用到的变量
com_id = "COM4"

class SerialSwitch(object):
    def __init__(self, com_id):
        self.s_obj = serial.Serial(com_id, baudrate=9600)

    def switch_pin1_on(self):
        self.s_obj.write([0x01, 0x0F, 0x00, 0x00, 0x00, 0x10, 0x02, 0x03, 0x00, 0xE2, 0xD0])
        self.s_obj.read()
        
    def switch_pin1_longon(self):
        self.s_obj.write([0x01, 0x34, 0xF0, 0x00, 0x00, 0x0A, 0x03, 0x09])
        self.s_obj.read()


    def switch_pin1_off(self):
        self.s_obj.write([0x01, 0x0F, 0x00, 0x00, 0x00, 0x10, 0x02, 0x02, 0x00, 0xE3, 0x40])
        self.s_obj.read()

    def switch_pin2_on(self):
        self.s_obj.write([0x01, 0x0F, 0x00, 0x00, 0x00, 0x10, 0x02, 0x00, 0x00, 0xE2, 0x20])
        self.s_obj.read()
    def switch_pin2_off(self):
        pass
    
    def switch_pin3_on(self):
        self.s_obj.write([0x01, 0x05, 0x00, 0x02, 0xFF, 0x00, 0x2D, 0xFA])
        self.s_obj.read()
        
    def switch_pin3_off(self):
        self.s_obj.write([0x01, 0x05, 0x00, 0x02, 0x00, 0x00, 0x6C, 0x0A])
        self.s_obj.read()

    def close(self):
        self.s_obj.close()


if __name__ == '__main__':
    switch_obj = SerialSwitch(com_id)
    for i in range(100):
        print("正在进行第%s次设备异常上电/断电测试" % i)
        switch_obj.switch_pin3_on()
        time.sleep(0.8)
        switch_obj.switch_pin3_off()
        time.sleep(1)
    switch_obj.close()
    os.system("pause")

