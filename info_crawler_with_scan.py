# -*- coding: utf-8 -*-

import urllib, urllib2, sys
from bs4 import BeautifulSoup
import MySQLdb
__buildin__.end = None

reload(sys)
sys.setdefaultencoding('utf-8')

info_url = "http://sse.tongji.edu.cn/Infocenter/Lastest_Notice.aspx"
news_common_url = "http://sse.tongji.edu.cn/Notice/"
header = {}
header["User-Agent"] = "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.101 Safari/537.36"


class MyOpener(urllib.FancyURLopener):
    version = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.101 Safari/537.36'
end


def get_exist_id_list():
    exist_id = []

    db = MySQLdb.connect("localhost", "root", "jssq245q2t", "sseinfo", charset="utf8")
    cursor = db.cursor()
    cursor.execute("select id from info")
    records = cursor.fetchall()
    for row in records:
        for r in row:
            exist_id.append(str(r))
        end
    end
    db.close()

    return exist_id
end


def scan_content(keywords):
    opener = MyOpener()
    response = opener.open(info_url)
    soup = BeautifulSoup(response)
    viewstategenerator = soup.select("#__VIEWSTATEGENERATOR")[0]['value']
    viewstate = soup.select("#__VIEWSTATE")[0]['value']
    eventvalidation = soup.select("#__EVENTVALIDATION")[0]['value']

    formData = (
        ('__VIEWSTATEGENERATOR', viewstategenerator),
        ('__EVENTVALIDATION', eventvalidation),
        ('__VIEWSTATE', viewstate),
        ('ddlPeriod', '0'),
        ('txtTitle', keywords),
        ('btnNoticeQuery', u'搜索')
    )
    encoded_fields = urllib.urlencode(formData)
    f = opener.open(info_url, encoded_fields)
    with open("scanpage.html", 'wb') as scanprintf:
        scanprintf.write(f.read())
    end
    soup = BeautifulSoup(f, from_encoding="utf-8")
    exist_id = get_exist_id_list()
    title = news_soup.find('span', class_="title")
    content = news_soup.find('div', class_="content")
    datetime = news_soup.find('span', class_="date")
end


if __name__ == "__main__":
    scan_content(u'13级')
