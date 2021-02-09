# -*- coding: utf-8 -*-
"""
Created on Tue Nov 10 11:14:20 2020

@author: 鹏
"""

import asyncio
import random
import zlib
from aiowebsocket.converses import AioWebSocket
import json
import win32com.client
import threading
from playwav import wavplay
from relaycom import SerialSwitch
import time
import nest_asyncio
import stop_thread
from tts import play_tts
from giftconfig import gift,Giftdict1,Giftdict2


roomid = '22616007'#22616007
hb = '00000010001000010000000200000001'
data_raw='000000{headerLen}0010000100000007000000017b22726f6f6d6964223a{roomid}7d'
data_raw=data_raw.format(headerLen=hex(27+len(roomid))[2:], roomid=roomid.encode().hex())
com_id = "COM4"
lock=threading.Lock()
gift().get_gift()

async def sendHeartBeat(websocket):
    '''心跳包'''
    while True:
        await asyncio.sleep(30)
        await websocket.send(bytes.fromhex(hb))

async def receDM(websocket):
    '''接收'''
    while True:
        recv_text = await websocket.receive()
        printDM(recv_text)

async def startup(url):
    '''开始'''
    async with AioWebSocket(url) as aws:
        converse = aws.manipulator
        
        await converse.send(bytes.fromhex(data_raw))
        tasks=[sendHeartBeat(converse), receDM(converse)]
        await asyncio.wait(tasks)

def speak(gift):
    '''语音播放'''    
    speaker = win32com.client.Dispatch("SAPI.SpVoice")
    speaker.Speak(gift)
        
def pin_hudie(num):
    '''启动机关1'''
    lock.acquire()
    switch_obj = SerialSwitch(com_id)
    funlist = [switch_obj.switch_pin1_on, switch_obj.switch_pin2_on]
    #    随机启动
    random.shuffle(funlist)
    for f in funlist:
        f()
    print('正在启动%s' % num+'秒'+name+'召唤的蝴蝶')
    for i in range(num):
#        print(i)
        unsec=num-i
        print(unsec,'秒')
        time.sleep(1)
    switch_obj.switch_pin1_off()
    print('完毕')     
    switch_obj.close()
    lock.release()#开锁

def pin_touwei(num):
    '''启动机关2'''
    lock.acquire()#上锁
    switch_obj = SerialSwitch(com_id)
    print('正在启动%s' % num+'秒'+name+'投喂的小零食')
    switch_obj.switch_pin3_on()
    time.sleep(num)
    switch_obj.switch_pin1_off()
    print('完毕')     
    switch_obj.close()
    lock.release()#开锁

def printDM(data):
    '''数据包模块'''
    # 获取数据包的长度，版本和操作类型
    packetLen = int(data[:4].hex(),16)
    ver = int(data[6:8].hex(),16)
    op = int(data[8:12].hex(),16)

    # 有的时候可能会两个数据包连在一起发过来，所以利用前面的数据包长度判断，
    if(len(data)>packetLen):
        printDM(data[packetLen:])
        data=data[:packetLen]

    # 有时会发送过来 zlib 压缩的数据包，这个时候要去解压。
    # if(ver == 2):
    #    data = zlib.decompress(data)
    #    printDM(data)
    #    print('db3')
    #    return
    
    if(ver==2):
        data = zlib.decompress(data[16:])
        printDM(data)
        return
    
    # ver 为1的时候为进入房间后或心跳包服务器的回应。op 为3的时候为房间的人气值。
    if(ver == 1):
        if(op == 3):
             pass
        return

    # ver 不为2也不为1目前就只能是0了，也就是普通的 json 数据。
    # op 为5意味着这是通知消息，cmd 基本就那几个了。
    if(op==5):
        try:
            jd = json.loads(data[16:].decode('utf-8', errors='ignore'))
            global name
            if(jd['cmd']=='DANMU_MSG'):
                Ttsplay=threading.Thread(target=play_tts,args=(jd['info'][1],))
                Ttsplay.start()
                if jd['info'][1]=='要讲武德':
                    name=jd['info'][2][1]
                    run_1=threading.Thread(target=pin_hudie,args=(10,))
                    run_1.start()
#                else:
#                    ttspaly(jd['info'][1])
#                    Ttsplay=threading.Thread(target=play_tts,args=(jd['info'][1],))
#                    Ttsplay.start()
            elif(jd['cmd']=='SEND_GIFT'):
                num=int(jd['data']['num'])
                name=jd['data']['uname']
                giftName=jd['data']['giftName']
                print('感谢',jd['data']['uname'],jd['data']['action'],jd['data']['num'],'个', jd['data']['giftName'])
                giftprice=Giftdict1.get(giftName)
                gifttype=Giftdict2.get(giftName)
                if (gifttype =='silver'):
                    run_1=threading.Thread(target=pin_hudie,args=(num*20,))
                    run_1.start()
                else:
                    run_1=threading.Thread(target=pin_touwei,args=(num*giftprice/500,))
                    run_1.start()
                    Ttsplay=threading.Thread(target=play_tts,args=('小熊小熊你又拉了吗，谢谢老板赏饭，小伙伴们快来开饭啦',))
                    Ttsplay.start()

        except Exception as e:
            pass
        
        
if __name__ == '__main__':
    nest_asyncio.apply()
    remote = 'wss://broadcastlv.chat.bilibili.com:2245/sub'
    try:
        asyncio.get_event_loop().run_until_complete(startup(remote))
    except KeyboardInterrupt as exc:
        print('Quit.',exc)