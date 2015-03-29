# -*- coding:utf-8 -*-

__author__ = 'JoshOY'

import urllib
import urllib2
from bs4 import BeautifulSoup
import sys
import json

reload(sys)
sys.setdefaultencoding('utf-8')

sseInfoUrl = ''
noticeUrlType = ''
downloadUrlType = ''
header = {}


with open('constants.json', 'r') as const_file:
    data_string = const_file.read()
    data = json.loads(data_string, encoding="utf-8")
    #print data
    try:
        sseInfoUrl = data[u'sseInfoUrl']
        noticeUrlType = data[u'noticeUrlType']
        downloadUrlType = data[u'downloadUrlType']
        header = data[u'header']
    except Exception as err:
        print 'Exception: Cannot get sseInfoUrl or noticeUrlType.'
        print 'Check "constants.json" to see if everything is correct.'
        exit(1)


class SSEInfoOpener(urllib.FancyURLopener):
    version = header[u'User-Agent']


def search_info_ids(keywords=u'', page_range=1):
    """
    search_info_ids -> list
    @:argument
        keywords: 搜索关键词，默认为空字符串
        page_range: 搜索页数限制，默认1页
    @:return
        检索到通知的url id列表（字符串格式）
    """
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


def get_info_detail(url_id):
    """
    get_info_detail -> dict
    @:argument
        url_id: 通知的id
    @:return
        一个dict，其中的键值为：
            "id": 通知id,
            "title": 通知标题,
            "content": 正文内容,
            "date": 发布时间
            "attachment": 一个list，里面为二元组：(附件名, 附件id)，若不含附件则为空list
    """
    info_url = noticeUrlType + str(url_id)
    detail = {}

    page = urllib2.urlopen(info_url).read()
    soup = BeautifulSoup(page)

    detail['id'] = str(url_id)
    detail['title'] = soup.find('span', class_='title').text.encode(encoding="utf-8")
    detail['date'] = soup.find('span', class_='date').text.encode(encoding="utf-8")
    detail['content'] = soup.find('div', class_='content').text.encode(encoding="utf-8")
    detail['attachment'] = []

    attachment_list = soup.find('div', class_='attachment').find_all('li')

    if not attachment_list:
        return detail

    for li in attachment_list:
        attachment_id = li.a['href'][20:]
        attachment_name = li.a.text
        detail['attachment'].append((attachment_name.encode(encoding="utf-8"), attachment_id.encode(encoding="utf-8")))

    return detail


if __name__ == '__main__':
    d = get_info_detail('1003635')
    print d['id']
    print d['title']
    print d['date']
    print d['content']
    print str(d['attachment'])