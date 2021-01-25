# -*- coding: utf-8 -*-
"""
Created on Sat Nov  7 22:49:20 2020

@author: 鹏
"""

import pyttsx3
engine = pyttsx3.init()
voices = engine.getProperty('voices')
for voice in voices:
    print(voice.id+'hahahahaha',voice)
    engine.setProperty('voice', voice.id)
    engine.say("过来")
    engine.runAndWait()
    engine.stop()