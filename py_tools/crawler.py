# -*- coding: utf-8 -*-
"""
original web crawler code
Created on Wed Oct  3 15:36:23 2018

@author: ZhiD
"""

import urllib.request
import http.cookiejar
from bs4 import BeautifulSoup
import time
import random

def get_html(url: str, charset: str='utf-8') -> str:
    """
    按照url伪装成浏览器获取网页
    url: 网页URL
    charset: 网页字符集
    """
    headers = {
    'Connection': 'Keep-Alive',
    'Accept': 'text/html, application/xhtml+xml, */*',
    'Accept-Language': 'en-US,en;q=0.8,zh-Hans-CN;q=0.5,zh-Hans;q=0.3',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 ( \
        KHTML, like Gecko) Chrome/49.0.2623.75 Safari/537.36 LB'
    }
    cj = http.cookiejar.CookieJar()
    opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))
    header_items = []

    for key, value in headers.items():
        elem = (key, value)
        header_items.append(elem)

    opener.addheaders = header_items

    resp = opener.open(url, timeout=20)
    html_text = resp.read().decode(charset)

    return html_text

def purify_html(html: str) -> str:
    """
    清理网页，只保留内容文本
    html: 网页源码
    """
    page = BeautifulSoup(html, 'html.parser')
    p_list = []

    for p in page.find_all('p'):
        p_list.append(p.text)

    return '\n'.join(p_list[1:-1])

def main():
    """
    主程序，按文章索引分别下载链接的网页
    """
    file_path = r'ebooks.txt'
    book_file = open(file_path, 'a', encoding='gbk')

    book_url = 'http://www.luoxia.com/jingzhou/'
    html = get_html(book_url)

    page_soup = BeautifulSoup(html, 'html.parser')
    # get the content of <div class="...">...</div>
    div_soup = page_soup.find(name='div', attrs={'class': 'book-list clearfix'})
    # get the content of <ul>...</ul>
    ul_soup = div_soup.find('ul')

    # for each part of <li>...</li> in ul_soup
    for li in ul_soup.find_all('li'):
        time.sleep(random.random())     # randomly delay 0.x second

        print('processing ', li.text)
        book_file.write(li.text.replace(u'\xa0', u' '))
        # insert chapter title, remove &nbsp;
        book_file.write('\n\n')

        # for the part of <a ...>...</a>
        link = li.find(name='a')
        html = get_html(link.attrs['href'])
        pure_text = purify_html(html)
        book_file.write(pure_text)  # 写入每章内容
        book_file.write('\n\n')

    book_file.close()

if __name__ == '__main__':
    main()
