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

def main():
    exist_id = []

    db = MySQLdb.connect("localhost", "root", "jssq245q2t", "sseinfo", charset="utf8")
    cursor = db.cursor()
    cursor.execute("select id from info")
    records = cursor.fetchall()
    for row in records:
        for r in row:
            exist_id.append(str(r))
    db.close()

    request = urllib2.Request(info_url, None, header)
    response = urllib2.urlopen(request)
    page = response.read()
    #print page
    with open("sseinfo.html", 'wb') as infofile:
        infofile.write(page)
    soup = BeautifulSoup(page, from_encoding="utf-8")
    news_div_list = soup.find_all('div', class_="news_title")
    for item in news_div_list:
        print item.a['href'][10:]
        print item.a.text
        news_url = news_common_url + item.a['href'][10:]
        news_req = urllib2.Request(news_url, None, header)
        news_res = urllib2.urlopen(news_req)
        news_page = news_res.read()
        if news_page == None:
            print "Oops, failed..."
            continue
        news_soup = BeautifulSoup(news_page, from_encoding="utf-8")
        title = news_soup.find('span', class_="title")
        content = news_soup.find('div', class_="content")
        datetime = news_soup.find('span', class_="date")

        print news_url
        print content.text.encode(encoding="utf-8")

        if item.a['href'][10:] in exist_id:
            continue

        with open("news/" + item.a['href'][10:] + ".txt", 'w') as news_file:
            news_file.write(news_url + '\n')
            news_file.write('\n' + title.text + '\n\n')
            news_file.write(content.text + '\n')

        #Connect to database
        db = MySQLdb.connect("localhost", "root", "jssq245q2t", "sseinfo", charset="utf8")
        cursor = db.cursor()
        sql = "INSERT INTO info(id, title, content, post_time) VALUES (" \
              + item.a['href'][10:] + ", '" \
              + title.text.encode(encoding="utf-8") + "', '"   \
              + content.text.encode(encoding="utf-8") + "', '" \
              + datetime.text + "');"
        print sql
        try:
            cursor.execute(sql)
            db.commit()
        except Exception as e:
            print e
            print "************Insert failed!***************"
            db.rollback()
        db.close()

if __name__ == "__main__":
    main()
