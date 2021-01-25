# -*- coding: utf-8 -*-
"""
Created on Sun Nov  8 02:04:28 2020

@author: 鹏
"""
import win32com.client

speaker = win32com.client.Dispatch("SAPI.SpVoice")
speaker.Speak('你好')