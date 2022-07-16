# -*-coding:utf-8 -*-
# author:sakia   
# time:2022-07-11 9:52
import urllib.request as ur

class HtmlDownloader(object):
    def download(self, url):
        if url is None:
            return None
        response = ur.urlopen(url)
        if response.getcode() != 200:
            return None
        return response.read()
