# -*- coding: utf-8 -*-
__author__ = 'JoshOY'

import info_crawler
import sys

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


if __name__ == '__main__':
    print SSEInfoCrawler.search_info_ids()