# -*- coding:utf-8 -*-

__author__ = 'JoshOY'

import urllib, urllib2
from bs4 import BeautifulSoup
import sys
import json

reload(sys)
sys.setdefaultencoding('utf-8')

sseInfoUrl = ''
noticeUrlType = ''
header = {}


with open('constants.json', 'r') as const_file:
    data_string = const_file.read()
    data = json.loads(data_string, encoding="utf-8")
    #print data
    try:
        sseInfoUrl = data[u'sseInfoUrl']
        noticeUrlType = data[u'noticeUrlType']
        header = data[u'header']
    except Exception as err:
        print 'Exception: Cannot get sseInfoUrl or noticeUrlType.'
        print 'Check "constants.json" to see if everything is correct.'
        exit(1)


class SSEInfoOpener(urllib.FancyURLopener):
    version = header[u'User-Agent']


"""
Function search_info_ids
@args
    keywords: 搜索关键词，默认为空字符串
    page_range: 搜索页数限制，默认1页
"""
def search_info_ids(keywords=u'', page_range=1):
    ids = []
    opener = SSEInfoOpener()

    response = opener.open(sseInfoUrl)
    # Transform the latestNews content into BS
    latest_news_soup = BeautifulSoup(response)

    # Some post values
    view_state_generator = latest_news_soup.select("#__VIEWSTATEGENERATOR")[0]['value']
    view_state = latest_news_soup.select("#__VIEWSTATE")[0]['value']
    event_validation = latest_news_soup.select("#__EVENTVALIDATION")[0]['value']

    form_data = (
        ('__VIEWSTATEGENERATOR', view_state_generator),
        ('__EVENTVALIDATION', event_validation),
        ('__VIEWSTATE', view_state),
        ('ddlPeriod', '0'),
        ('txtTitle', keywords),
        ('btnNoticeQuery', u'搜索')
    )
    encoded_fields = urllib.urlencode(form_data)
    filtered_page = opener.open(sseInfoUrl, encoded_fields).read()
    filtered_page_soup = BeautifulSoup(filtered_page, from_encoding="utf-8")
    info_div_list = filtered_page_soup.find_all('div', class_="news_title")

    for each_div in info_div_list:
        url_id = each_div.a['href'][10:]
        ids.append(url_id)

    page_range -= 1
    event_argument = 1

    while page_range > 0:
        page_range -= 1
        event_argument += 1

        view_state_generator = filtered_page_soup.select("#__VIEWSTATEGENERATOR")[0]['value']
        view_state = latest_news_soup.select("#__VIEWSTATE")[0]['value']
        event_validation = latest_news_soup.select("#__EVENTVALIDATION")[0]['value']

        form_data = (
            ('__VIEWSTATEGENERATOR', view_state_generator),
            ('__EVENTVALIDATION', event_validation),
            ('__VIEWSTATE', view_state),
            ('__EVENTTARGET', 'GridView1$ctl23$AspNetPager1'),
            ('ddlPeriod', '0'),
            ('txtTitle', keywords),
            ('__EVENTARGUMENT', str(event_argument)),
        )
        encoded_fields = urllib.urlencode(form_data)
        filtered_page = opener.open(sseInfoUrl, encoded_fields).read()
        filtered_page_soup = BeautifulSoup(filtered_page)
        info_div_list = filtered_page_soup.find_all('div', class_="news_title")
        for each_div in info_div_list:
            url_id = each_div.a['href'][10:]
            ids.append(url_id)

    return ids


if __name__ == '__main__':
    print search_info_ids()