#-*- coding:utf-8 -*-

from findbilibili import *

#funtion name [checkinfo]
#判断要输出的回答
#param array 抓取的文字
#return string 回答
def checkinfo2(content):
    content[1] = content[1].decode('gbk')
    key = content[1].encode('utf-8')
    if key == '节操':
        return '这种东西早就没有了'


    result = animation(key)    #搜动漫
    return result
    

#funtion name [animation]
#搜索动漫
#param array 动漫名字
#return string 最后更新网址
def animation(name):
    url = bilibili(name)
    try:
        result = 'bilibili最后更新:第'+url[-1][0]+'集'+url[-1][1]
        return result
    except IndexError:
        return '什么都找不到！'