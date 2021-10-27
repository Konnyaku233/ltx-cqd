# -*- coding = utf8 -*-
# @Time : 2021/8/11 18:28
# @Author : Anic
# @File : sendmeg.py
# @Software : PyCharm
import win32api
import win32gui
import win32con
import win32clipboard as clipboard
import time
from getmsg import getmsg


###############################
#  微信发送
###############################
def send_m():

    win32api.keybd_event(17, 0, 0, 0)  # ctrl键位码是17
    win32api.keybd_event(86, 0, 0, 0)  # v键位码是86
    win32api.keybd_event(86, 0, win32con.KEYEVENTF_KEYUP, 0)  # 释放按键
    win32api.keybd_event(17, 0, win32con.KEYEVENTF_KEYUP, 0)

    time.sleep(1)
    win32api.keybd_event(18, 0, 0, 0)  # Alt键位码
    win32api.keybd_event(83, 0, 0, 0)  # s键位码
    win32api.keybd_event(18, 0, win32con.KEYEVENTF_KEYUP, 0)  # 释放按键
    return


def txt_ctrl_v(txt_str):
    # 定义文本信息,将信息缓存入剪贴板
    clipboard.OpenClipboard()
    clipboard.EmptyClipboard()
    clipboard.SetClipboardData(win32con.CF_UNICODETEXT, txt_str)
    clipboard.CloseClipboard()
    return


#######################发送过程=================
def sendTaskLog():
    # 查找微信小窗口
    msg = getmsg()
    if msg is None:
        return 1
    txt_ctrl_v(msg)
    send_m()
    return 0


