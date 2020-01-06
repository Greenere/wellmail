#!/usr/bin/env python
# coding=utf-8

#Auxiliary functions
#Written by Xin Liu

from urllib.request import urlopen
from bs4 import BeautifulSoup
import operator

def weather():
    '''
    :return: 包含temperatureLow（最低气温）,temperatureHigh（最高气温）,weather（天气）,wind（风力级数）的列表
    '''
    resp = urlopen('http://www.weather.com.cn/weather/101200101.shtml')
    soup = BeautifulSoup(resp, 'html.parser')
    # 第一个包含class="tem"的p标签即为存放今天天气数据的标签
    tagToday = soup.find('p', class_="tem")
    try:
        # 有时候这个最高温度是不显示的，此时利用第二天的最高温度代替。
        temperatureHigh = tagToday.span.string
    except AttributeError as e:
        # 获取第二天的最高温度代替
        temperatureHigh = tagToday.find_next('p', class_="tem").span.string

    temperatureLow = tagToday.i.string  # 获取最低温度
    weather = soup.find('p', class_="wea").string  # 获取天气
    wind = soup.find('p', class_="win").i.string  # 获取风力

    # print('最低温度:' + temperatureLow)
    # print('最高温度:' + temperatureHigh)
    # print('天气:' + weather)
    # print('风力级数：' + wind)

    return temperatureLow,temperatureHigh,weather,wind

#管理辅助函数
def getClass(data):
        '''
        :param item:获取的分类标准
        :param datas:Mon到Sun的一个字典，key为对应的星期，value为属于对应星期的邮件编号列表
        :return: Mon到Sun的一个字典，key为对应的星期，value为属于对应星期的邮件编号列表
        '''
        #item为获取的分类标准
        item =[]
        datas = {}
        datas['Mon']=[]
        datas['Tue']=[]
        datas['Wed']=[]
        datas['Thu']=[]
        datas['Fri']=[]
        datas['Sat']=[]
        datas['Sun']=[]
        for i in range(0,len(data)):
            data[i]['number']=i
            if "Mon" in data[i][item]:
                datas['Mon'].append(data[i]['number'])
            if "Tue" in data[i][item]:
                datas['Tue'].append(data[i]['number'])
            if "Wen" in data[i][item]:
                datas['Wed'].append(data[i]['number'])
            if "Tur" in data[i][item]:
                datas['Thu'].append(data[i]['number'])
            if "Fri" in data[i][item]:
                datas['Fri'].append(data[i]['number'])
            if "Sat" in data[i][item]:
                datas['Sat'].append(data[i]['number'])
            if "Sun" in data[i][item]:
                datas['Sun'].append(data[i]['number'])
        return datas

def getSearch(data):
        '''
        可以选择对邮件的subject,from,to,date进行search
        :param  keyword:查找的关键字
        :param  item:需要查找的关键字对应的key
        :return:  line：查找到的对应邮件编号列表
        (print对应的邮件编号，及查找邮件对应的key的value值)
        '''
        #print("Search!")
        #keyword为查找的关键字
        keyword=[]
        #item为对应关键字所属的key
        item=[]
        line=[]

        for values in range(0,len(data)):
            if keyword in data[values][item]:
                #print("This is "+str(values) +"th letter!\n"+ item + ":" + data[values][item])
                line.append(values)

        return line

def getMembers(data={}):
    '''
          :param member:需要添加的用户名
          :param members:获取的所有用户名及用户邮箱
          :param  memberss:去除重复用户后的最终用户列表
          :param  lines:二维列表，分离过后的用户名及用户邮箱
          :return: 一个二维列表，子列表个数为不同用户的数目，
          每个子列表有对应用户的用户名和邮箱地址(同时保存有一个通讯簿文件)
          '''
    # member为需要添加的用户名
    filename = 'member.txt'

    members = []
    memberss = []
    lines = []
    for i in range(0, len(data)):
        members.append(str(data[i]['from']))

    # if member is not None and member not in members:
    #     members.append(member)

    for i in members:
        if i not in memberss:
            memberss.append(i)

    for i in range(0, len(memberss)):
        memberss[i] = memberss[i].replace('>', '')
        memberss[i] = memberss[i].replace('"', '')
        memberss[i] = memberss[i].replace(' ', '')
        line = memberss[i].split("<")
        lines.append(line)

    with open(filename, 'w')as file_object:
        file_object.write(str(lines))
    return lines

def findMembers():
        '''
        :return: 对应用户的邮箱地址
        '''
        #member为需要查找的用户名的部分信息
        member = []
        filename='member.txt'

        with open(filename,'r')as file_object:
            lines=file_object.read()
            lines=eval(lines)

        for i in range(0,len(lines)):
           if member in lines[i][0]:
               return lines[i][1]

def getRange(data=[]):
    '''
    :param line：二维列表，行为用户，列为日期的具体信息（被分割）
    :param lines: 被分割的日期信息
    :return: 排序后的邮件内容列表
    '''
    line = []
    datas= []
    for i in range(0, len(data)):
        try:
            lines = data[i]['date'].split(" ")
            if data[i]['date']=='-':
                lines = 'Sun, 31 Dec 1970 00:00:00 -0000'.split(' ')
        except:
            lines = 'Sun, 31 Dec 1970 00:00:00 -0000'.split(' ')
        line.append(lines)
        line[i][int(len(line[i])) - 1] = i
        for j in range(0, len(line[i])):
            if line[i][j] == 'Jan': line[i][j] = 'A'
            if line[i][j] == 'Feb': line[i][j] = 'B'
            if line[i][j] == 'Mar': line[i][j] = 'C'
            if line[i][j] == 'Apr': line[i][j] = 'D'
            if line[i][j] == 'May': line[i][j] = 'E'
            if line[i][j] == 'Jun': line[i][j] = 'F'
            if line[i][j] == 'Jul': line[i][j] = 'G'
            if line[i][j] == 'Aug': line[i][j] = 'H'
            if line[i][j] == 'Sept':line[i][j] = 'I'
            if line[i][j] == 'Oct': line[i][j] = 'J'
            if line[i][j] == 'Nov': line[i][j] = 'K'
            if line[i][j] == 'Dec': line[i][j] = 'L'
            if line[i][j] == 'Mon,':line[i][j] = 'M'
            if line[i][j] == 'Tue,':line[i][j] = 'N'
            if line[i][j] == 'Wed,':line[i][j] = 'O'
            if line[i][j] == 'Thu,':line[i][j] = 'P'
            if line[i][j] == 'Fri,':line[i][j] = 'Q'
            if line[i][j] == 'Sat,':line[i][j] = 'R'
            if line[i][j] == 'Sun,':line[i][j] = 'S'

    line.sort(key=operator.itemgetter(3, 2, 1, 0, 4))
    for i in range(0, len(data)):
        for j in range(0, len(line[i])):
            if line[i][j] == 'A': line[i][j] = 'Jan,'
            if line[i][j] == 'B': line[i][j] = 'Feb,'
            if line[i][j] == 'C': line[i][j] = 'Mar,'
            if line[i][j] == 'D': line[i][j] = 'Apr,'
            if line[i][j] == 'E': line[i][j] = 'May,'
            if line[i][j] == 'F': line[i][j] = 'Jun,'
            if line[i][j] == 'G': line[i][j] = 'Jul,'
            if line[i][j] == 'H': line[i][j] = 'Aug,'
            if line[i][j] == 'I': line[i][j] = 'Sept,'
            if line[i][j] == 'J': line[i][j] = 'Oct,'
            if line[i][j] == 'K': line[i][j] = 'Nov,'
            if line[i][j] == 'L': line[i][j] = 'Dec,'
            if line[i][j] == 'M': line[i][j] = 'Mon,'
            if line[i][j] == 'N': line[i][j] = 'Tue,'
            if line[i][j] == 'O': line[i][j] = 'Wed,'
            if line[i][j] == 'P': line[i][j] = 'Thu,'
            if line[i][j] == 'Q': line[i][j] = 'Fri,'
            if line[i][j] == 'R': line[i][j] = 'Sat,'
            if line[i][j] == 'S': line[i][j] = 'Sun,'

    trans={}
    for i in range(0, len(line)):
         trans[len(line)-i-1]=line[i][-1]
         datas.append(data[line[i][-1]])
    datas.reverse()
    #print('reverse')
    return datas,trans

