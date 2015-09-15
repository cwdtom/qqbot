# -*- coding: utf-8 -*-

__author__ = 'Tom Chen'

import urllib2,sys,re,time
from sgmllib import SGMLParser
from datetime import datetime,date
from urllib import unquote,quote

default_encoding = 'utf-8'                        #设置文件使用UTF-8编码
if sys.getdefaultencoding() != default_encoding:
    reload(sys)
    sys.setdefaultencoding(default_encoding)
 

class findbilibili(SGMLParser):                #分析HTML源代码
    def __init__(self):
        SGMLParser.__init__(self)
        self.is_script = ''
        self.url = []
        self.videonum = []
        self.is_li = ''
        self.seasonnum = []
        self.season = []
        self.is_a = ''
        self.num = []


    def start_script(self,attrs):
        try:
            if attrs[0][0] == 'language' and attrs[0][1] == 'javascript':
                self.is_script = 'num'
        except IndexError:
            pass


    def end_script(self):
        self.is_script = ""

    def start_li(self,attrs):
        try:
            if attrs[0][0] == 'season_id' and attrs[1][0] == 'id':
                if re.match(r's_\d+',attrs[1][1]):
                    self.is_li = 'season'
                    self.seasonnum.append(attrs[0][1])

        except IndexError:
            pass

    def end_li(self):
        self.is_li = ''

    def start_a(self,attrs):
        try:
            if attrs[0][0] == 'class' and attrs[0][1] == 't':
                if attrs[1][0] == 'href' and re.match(r'/video/av\d+',attrs[1][1]):
                    if attrs[2][0] == 'target' and attrs[2][1] == '_blank':
                        self.is_a = 'url'
                        self.url.append(attrs[1][1])

        except IndexError:
            pass

    def end_a(self):
        self.is_a = ''

    
    def handle_data(self, data):
        if self.is_script == 'num':
            self.videonum.append(data)
        if self.is_li == 'season':
            self.season.append(data)
        if self.is_a == 'url':
            self.num.append(data)

            
#funtion name [bilibili]
#在bilibili上抓取动画网址
#param string 动画名字
#return array[array] 2维数组 [1,[第一集][地址]][2,[][]][3...]...
def bilibili(sname):
    name = sname
    name = unquote(name)
    l = name.split(' ')
    m = []
    s = ''
    rename = re.compile('第')
    if len(l) != 1:
        s = l[len(l)-1]
        if rename.findall(s):
            m = name.split(s)
        else:
            m.append(name) 
        if s == '续':
            s = '第二季'
    else:
        m.append(name)
    m[0] = quote(m[0])
    if name == '无头骑士异闻录×2 转':
        s = name
    if name == '无头骑士异闻录×2 承':
        s = name


    url = 'http://www.bilibili.com/sp/'+m[0]
    user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'       #伪装浏览器请求数据
    headers = { 'User-Agent' : user_agent }
    request = urllib2.Request(url, headers=headers)
    try:
        content = urllib2.urlopen(request).read()
    except urllib2.HTTPError:
        return []
    listname = findbilibili()
    listname.feed(content)
    rename = re.compile(r'\d+')
    try:
        videoid = rename.findall(listname.videonum[0])
    except IndexError:
        return []
    videoid2 = ''
    try:
        n = len(listname.season)
        a = 0
        for a in range(n):
            if listname.season[a] == s:
                videoid2 = listname.seasonnum[a]
                break
        if videoid2 == '':
            videoid2 = listname.seasonnum[0]
    except  IndexError:
        pass
    if videoid2:
        y = '-'
    else:
        y = ''

    try:
        url = 'http://www.bilibili.com/sppage/bangumi-'+videoid[0]+y+videoid2+'-1.html'
    except IndexError:
        return []
    user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'       #伪装浏览器请求数据
    headers = { 'User-Agent' : user_agent }
    request = urllib2.Request(url, headers=headers)
    content = urllib2.urlopen(request).read()
    listname = findbilibili()
    listname.feed(content)
    n = len(listname.url)
    a = 0
    for a in range(n):
        listname.url[a] = 'http://www.bilibili.com'+listname.url[a]
    rename = re.compile(r'\d+')
    l = []
    for a in range(n):
        z = rename.findall(listname.num[a])
        zz = ''.join(z)
        l.append(zz)

    dname = []
    qname = []
    a = 0
    for a in range(n):
        x = []
        x.append(l[a])
        x.append(listname.url[a])
        qname.append(x)

    for a in range(n):
        dname.append(qname[n - a -1])

    return dname





if __name__ == '__main__':
    name = '噬神者'.encode('gbk')
    newname = name.decode('gbk')
    newname = newname.encode('utf-8')
    print newname
    bilibili(newname)
