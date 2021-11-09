# -*- coding = utf8 -*-
# @Time : 2021/8/11 19:03
# @Author : Anic
# @File : getmsg.py
# @Software : PyCharm
import requests
import datetime
import parsel
import time
import xlrd
from bs4 import BeautifulSoup


def week(num:int):
    if num == 1:
        return "一"
    elif num == 2:
        return "二"
    elif num == 3:
        return "三"
    elif num == 4:
        return "四"
    elif num == 5:
        return "五"
    elif num == 6:
        return "六"
    elif num == 7:
        return "日"


headers = {
    'Cookie': 'SUID=3DDC5D70721A910A000000006113B341; SUID=3DDC5D70741A910A000000006113B342; weixinIndexVisited=1; SUV=00F9E661705DDC3D6113B3426F4EF907; wuid=AAGlHfjrNwAAAAqHI2SLzAAAkwA=; ABTEST=0|1633886555|v1; SNUID=EF83A018C8C2092A7D9A6253C81928CF; IPLOC=CN4400',
    'Host': 'weixin.sogou.com',
    'Referer': 'https://www.sogou.com/web?query=python&_asf=www.sogou.com&_ast=&w=01019900&p=40040100&ie=utf8&from=index-nologin&s_from=index&sut=1396&sst0=1610779538290&lkt=0%2C0%2C0&sugsuv=1590216228113568&sugtime=1610779538290',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36',
}


def geturl():
    url = 'https://weixin.sogou.com/weixin?type=2&query=杨记杂货铺 互联网早报|{}月{}日&ie=utf8&s_from=input&_sug_=n&_sug_type_=1&w=01015002&oq=&ri=3&sourceid=sugg&sut=0&sst0=1628682739410&lkt=0%2C0%2C0&p=40040108'.format(
        datetime.datetime.now().month, datetime.datetime.now().day)
    # print(url)
    response = requests.get(url=url, headers=headers)
    selector = parsel.Selector(response.text)
    # print(response.text)
    # print(time.strftime("%Y-%m-%d", time.localtime()))
    lis = selector.css('.news-list li')
    for li in lis:
        name = li.css('.s-p a::text').get()
        # print(name)
        date = li.css('.s-p::attr(t)').get()
        timeArray = time.localtime(int(date))
        otherStyleTime = time.strftime("%Y-%m-%d", timeArray)
        # print(otherStyleTime)
        if name == '杨记杂货铺' and otherStyleTime == time.strftime("%Y-%m-%d", time.localtime()):
            href = li.css('.txt-box h3 a::attr(href)').get()
            article_url = 'https://weixin.sogou.com' + href
            return article_url


    url = 'https://weixin.sogou.com/weixin?type=1&s_from=input&query=杨记杂货铺&ie=utf8&_sug_=y&_sug_type_=&w=01019900&sut=2882&sst0=1629363334676&lkt=0%2C0%2C0'
    response = requests.get(url=url, headers=headers)
    bf = BeautifulSoup(response.text, features="lxml")
    cqd = bf.find_all('a', uigs='account_article_0')
    if len(cqd) == 1 and len(cqd[0].text) > 15:
        if cqd[0].text[:13] == '互联网早报 | {}月{}日 '.format(datetime.datetime.now().month, datetime.datetime.now().day) or \
                cqd[0].text[:13] == '互联网早报 | {}月{}日'.format(datetime.datetime.now().month, datetime.datetime.now().day) or \
                cqd[0].text[:13] == '互联网早报 | {}月{}'.format(datetime.datetime.now().month, datetime.datetime.now().day):
            return 'https://weixin.sogou.com' + cqd[0]['href']

    print('not found')
    return None


def getmsg(url=None):
    msg = '【猎头早知道】1分钟行业快讯\n'
    msg = msg+'{}年{}月{}日 星期{}'.format(datetime.datetime.now().year,
                                      datetime.datetime.now().month, datetime.datetime.now().day, week(datetime.datetime.now().isoweekday()))
    msg = msg + '\n———————————————'

    if (url == None):
        url = geturl()
        response = requests.get(url=url, headers=headers)
        url = ''
        flag = 0
        cnt = 0
        for i in response.text:
            if i == '{':
                flag = 1
            elif i == '\'':
                cnt = cnt +1
            elif flag == 1 and cnt %2 == 1 :
                url = url + i
    if url is None:
        return None
    # print(url)
    response = requests.get(url=url)
    bf = BeautifulSoup(response.text, features="lxml")
    cqd = bf.find_all('p', style=['text-align:justify;line-height: 2em;',
                                  'text-align:justify;vertical-align:inherit;line-height: 2em;',
                                  'text-align:left;text-autospace:none;', 'text-align:left;line-height: 2em;',
                                  'text-align:left;vertical-align:inherit;line-height: 2em;'])
    title = bf.find_all('section', style=['height: 40px;display: flex;justify-content: center;', 'height:40px;display: flex;justify-content: center;'])
    cnt = -1
    lis = ['国内要闻','科技通信','金融财经','住房地产','医疗健康','国际视角']
    flag = 0
    for ltx in cqd:
        # print(ltx.text)
        if len(ltx.text) >10 and ltx.text[0] == '1' and ltx.text[1] == '、':
            cnt = cnt + 1
            if lis.count(title[cnt].text) > 0:
                msg = msg + '\n【'+title[cnt].text+'】\n'
        if lis.count(title[cnt].text) > 0 and len(ltx.text) >10 and ltx.text[0] < '4' and ltx.text[1] == '、':
            msg = msg + ltx.text + '。\n'
            flag = flag + 1
    if flag < 17:
        return None
    msg = msg + '————————————\n以上早报由倍小罗汇总整理\n信息来源：腾讯科技、36氪、界面等\n————————————\n'
    readbook = xlrd.open_workbook(r'每日吐槽.xlsx')
    day = datetime.datetime.now().day
    table = readbook.sheets()[0]
    msg = msg + '今日吐槽：' + table.cell_value(day, 1)
    return msg
