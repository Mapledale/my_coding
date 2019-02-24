#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date    : 2018-10-05 10:37:35
# @Author  : David Deng (ddengca@gmail.com)
# @Version :

import os
import datetime
import urllib.request
# import http.cookiejar
from selenium import webdriver

def get_html_urllib_basic(url):
    my_req = urllib.request.Request(url)
    with urllib.request.urlopen(my_req) as response:
        my_html = str(response.read())

    return my_html

def get_html_urllib_opener(url, charset='utf-8'):    
    '''
    to grab a web page

    url: URL of the web page to grab
    charset: charset of the web page
    '''
    opener = urllib.request.build_opener()
    resp = opener.open(url, timeout=20)
    html_text = resp.read().decode(charset)

    return html_text

def get_html_selenium(url):
    my_browser = webdriver.Chrome()
    my_browser.get(url)
    return my_browser.page_source

def main():
    save_path = os.path.dirname(os.path.abspath(__file__))
    ts = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
    file_name = r'wp_%s.txt' %ts
    file_name_full = os.path.join(save_path, file_name)
    target_url = 'https://www.google.com'
    # target_url = 'https://otexts.org/fpp2/index.html'
    # target_url = 'https://www.safaribooksonline.com/library/view/\
    #    creating-apps-in/9781491947333/cover.html'

    my_file = open(file_name_full, 'a')
    # my_file = codecs.open(file_name_full, 'a', 'utf-8')
    
    mode = '2'
    if mode == '1':
        my_html = get_html_urllib_basic(target_url)
    elif mode == '2':
        my_html = get_html_urllib_opener(target_url)
    elif mode == '3':
        my_html = get_html_selenium(target_url)
    
    my_file.write(my_html)
    my_file.write('\n\n')
    my_file.close()

if __name__ == '__main__':
    main()
