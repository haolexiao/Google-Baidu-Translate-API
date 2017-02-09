#/usr/bin/env python
#coding=utf8
 
import httplib
import md5
import urllib
import urllib2
import HTMLParser

import random
import json
import re

agent = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.137 Safari/537.36 LBBROWSER'}

def TranslateByBaidu(text,fromLang = 'auto',toLang = 'zh', appid, secretKey):
    httpClient = None
    myurl = '/api/trans/vip/translate'
    q = text
    salt = random.randint(32768, 65536)

    sign = appid+q+str(salt)+secretKey
    m1 = md5.new()
    m1.update(sign)
    sign = m1.hexdigest()
    myurl = myurl+'?appid='+appid+'&q='+urllib.quote(q)+'&from='+fromLang+'&to='+toLang+'&salt='+str(salt)+'&sign='+sign
     
    try:
        httpClient = httplib.HTTPConnection('api.fanyi.baidu.com')
        httpClient.request('GET', myurl)

        #response是HTTPResponse对象
        response = httpClient.getresponse()
        result = response.read()
        data = json.loads(result)
        return data["trans_result"][0]["dst"]
    except Exception, e:
        print e
    finally:
        if httpClient:
            httpClient.close()



def unescape(text):
    parser = HTMLParser.HTMLParser()
    return (parser.unescape(text))


def TranslateByGoogle(text, fromLang="auto", toLang="zh-CN"):
    base_link = "http://translate.google.cn/m?hl=%s&sl=%s&q=%s"
    text = urllib.quote_plus(text)
    link = base_link % (toLang, fromLang, text)
    request = urllib2.Request(link, headers=agent)
    try:
        raw_data = urllib2.urlopen(request).read()
        data = raw_data.decode("utf-8")
        expr = r'class="t0">(.*?)<'
        re_result = re.findall(expr, data)
        if (len(re_result) == 0):
            result = ""
        else:
            result = unescape(re_result[0])
        return (result)
    except Exception, e:
        print e
