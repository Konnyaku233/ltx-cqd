from sendmsg import sendTaskLog
from time import strftime, localtime, sleep
from getmsg import getmsg



if __name__ == '__main__':
    print('是否定时自动发送（1：是；2：否）')
    if int(input()) == 1:
        print("您选择了定时发送，请输入发送时间（如08:05）：")
        time1 = input()
        time2 = strftime('%H:%M', localtime())
        if time1 != time2:
            print("时间未到，到时候将自动发送")
        while time1 != time2:
            sleep(30)
            time2 = strftime('%H:%M', localtime())
        while sendTaskLog() == 1:
            print("查找失败，重新查找")
            print(strftime('%H:%M', localtime()))
            sleep(200)
        print("已成功自动发送")
    else:
        print("是否自动获取当天早报（1：自动获取；2：手动输入网址）")
        if int(input()) == 1:
            msg = getmsg()
        else:
            print("请输入目标网址：")
            msg = getmsg(input())
        with open("早报.txt", 'w') as f:
            f.write(msg)
            f.close()
        print("已保存至早报.txt")
    input()