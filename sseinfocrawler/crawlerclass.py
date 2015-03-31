# -*- coding: utf-8 -*-
__author__ = 'JoshOY'

import info_crawler
import sendmail
import sys
import json

reload(sys)
sys.setdefaultencoding('utf-8')


class SSEInfoCrawler:
    """
    class SSEInfoCrawler
    该类提供各种API，静态方法。
    """

    def __init__(self):
        pass

    @staticmethod
    def search_info_ids(keywords=u'', page_limit=1):
        return info_crawler.search_info_ids(keywords, page_limit)

    @staticmethod
    def get_info_detail(url_id):
        return info_crawler.get_info_detail(url_id)

    @staticmethod
    def send_packaged_mail(info):
        with open('settings.json') as jsonf:
            mail_settings = json.loads(jsonf.read())
            for each_to_send in mail_settings[u'toMail']:
                sendinfo = sendmail.create_sendinfo(mail_settings[u'smtpHost'],
                                                    mail_settings[u'fromMail'],
                                                    each_to_send,
                                                    mail_settings[u'senderUsername'],
                                                    mail_settings[u'senderPassword'])
                mailobj = sendmail.create_mailobj(u'【软院新通知提醒】' + info['title'],
                                                  info['content'] + u'\n\n发布日期：' + info['date'],
                                                  mail_settings[u'fromMail'],
                                                  each_to_send)
                sendmail.send_mail(sendinfo, mailobj)
        return True


if __name__ == '__main__':
    print SSEInfoCrawler.send_packaged_mail(SSEInfoCrawler.get_info_detail(u'1003697'))