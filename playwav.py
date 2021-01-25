# -*- coding: utf-8 -*-
"""
Created on Tue Nov 10 11:03:16 2020

@author: 鹏
"""
# Our raison d'etre - playing sounds

import pywintypes
import struct
import win32event
import win32com.directsound.directsound as ds

import os


WAV_HEADER_SIZE = struct.calcsize('<4sl4s4slhhllhh4sl')

def wav_header_unpack(data):
    '''解包wav文件头信息'''
    (riff, riffsize, wave, fmt, fmtsize, format, nchannels, samplespersecond, \
    datarate, blockalign, bitspersample, data, datalength) = struct.unpack('<4sl4s4slhhllhh4sl', data)

    if riff != b'RIFF' or fmtsize != 16 or fmt != b'fmt ' or data != b'data':
        raise ValueError

    wfx = pywintypes.WAVEFORMATEX()
    wfx.wFormatTag = format
    wfx.nChannels = nchannels
    wfx.nSamplesPerSec = samplespersecond
    wfx.nAvgBytesPerSec = datarate
    wfx.nBlockAlign = blockalign
    wfx.wBitsPerSample = bitspersample

    return wfx, datalength


# 播放wav文件，直到结束
def wavplay(wavpath):
    sound_file = wavpath
    fname = os.path.join(os.path.dirname(__file__), sound_file)
    
    f = open(fname, 'rb')
    
    # 读取/解包wav文件头
    hdr = f.read(WAV_HEADER_SIZE)
    
    wfx, size = wav_header_unpack(hdr)
    
    
    d = ds.DirectSoundCreate(None, None)
    d.SetCooperativeLevel(None, ds.DSSCL_PRIORITY)
    
    
    sdesc = ds.DSBUFFERDESC()
    
    sdesc.dwFlags = ds.DSBCAPS_STICKYFOCUS | ds.DSBCAPS_CTRLPOSITIONNOTIFY
    sdesc.dwBufferBytes = size
    sdesc.lpwfxFormat = wfx
    
    buffer = d.CreateSoundBuffer(sdesc, None)
    
    
    event = win32event.CreateEvent(None, 0, 0, None)
    
    notify = buffer.QueryInterface(ds.IID_IDirectSoundNotify)
    notify.SetNotificationPositions((ds.DSBPN_OFFSETSTOP, event))
    
    
    buffer.Update(0, f.read(size))
    buffer.Play(0)
    
    win32event.WaitForSingleObject(event, -1)
    
if __name__ == '__main__':
    wavplay("F:\dltool\code\录音-022.wav")
    wavplay("F:\dltool\code\录音-023.wav")