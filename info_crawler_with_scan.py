# -*- coding: utf-8 -*-

import urllib, urllib2, sys
from bs4 import BeautifulSoup
import MySQLdb

reload(sys)
sys.setdefaultencoding('utf-8')


info_url = "http://sse.tongji.edu.cn/Infocenter/Lastest_Notice.aspx"
news_common_url = "http://sse.tongji.edu.cn/Notice/"
header = {}
header["User-Agent"] = "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.101 Safari/537.36"


class MyOpener(urllib.FancyURLopener):
    version = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.101 Safari/537.36'


def get_exist_id_list():
    exist_id = []

    db = MySQLdb.connect("localhost", "root", "*********", "sseinfo", charset="utf8")
    cursor = db.cursor()
    cursor.execute("select id from info")
    records = cursor.fetchall()
    for row in records:
        for r in row:
            exist_id.append(str(r))
    db.close()

    return exist_id


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
    page = f.read()

    with open("scanpage.html", 'wb') as scanprintf:
        scanprintf.write(page)

    news_soup = BeautifulSoup(page, from_encoding="utf-8")
    exist_id = get_exist_id_list()

    info_div_list = news_soup.find_all('div', class_="news_title")

    db = MySQLdb.connect("localhost", "root", "*******", "sseinfo", charset="utf8")
    cursor = db.cursor()

    for each_div in info_div_list:
        title = each_div.a.text
        url_id = each_div.a['href'][10:]
        print url_id, title
        if url_id in exist_id:
           continue
        single_info_page = urllib2.urlopen(news_common_url + url_id).read()
        single_info_soup = BeautifulSoup(single_info_page)

        content = single_info_soup.find('div', class_="content").text
        datetime = single_info_soup.find('span', class_="date").text
        print content
        sql = "INSERT INTO info(id, title, content, post_time) VALUES (" \
            + url_id + ", '" \
            + title.encode(encoding="utf-8") + "', '"   \
            + content.encode(encoding="utf-8") + "', '" \
            + datetime + "');"
        try:
            cursor.execute(sql)
            db.commit()
        except Exception as e:
            print "**********  INSERT FAILED!  *************"
            print e
            print "**************  LOG END  ****************"
            db.rollback()
    db.close()

if __name__ == "__main__":
    scan_content(u'13级')
