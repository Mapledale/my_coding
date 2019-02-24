# -*- coding: utf-8 -*-
"""
Created on Wed Oct 17 20:44:54 2018
to save an HTML file in a pretty format
@author: ZhiD
"""

import os.path
from bs4 import BeautifulSoup as bs

def main():
    save_path = os.path.dirname(os.path.abspath(__file__))
    file_name = r'part0002_ori.html'
    file_name_full = os.path.join(save_path, file_name)
    with open(file_name_full, encoding='utf-8') as f:
#        content = list(f)
        content = f.read()
#        for line in f:
#            content.append(line)
    save_file_name = file_name[:-5] + '_new' + file_name[-5:]
    with open(save_file_name, 'w', encoding='utf-8') as f:
        soup = bs(content, 'lxml')
        html = soup.prettify()  # return a PRETTY html
        f.write(html)
# =============================================================================
#         for line in content:
#             soup = bs(line, 'lxml')
#             html = soup.prettify()
#             f.write(html)
# =============================================================================

if __name__ == '__main__':
    main()
