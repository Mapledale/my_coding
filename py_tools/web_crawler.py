#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date    : 2018-10-08 14:31:56
# @Author  : David Deng (ddengca@gmail.com)
# @Version :
# my web crawler to login to safaribooksonline.com
# and grab pages of a book
# and save each pages

import os
import re
import urllib.request
from selenium import webdriver
from bs4 import BeautifulSoup


class WebCrawler(object):
    """
    my crawler
    """
    def __init__(self, tgt, inter='Firefox'):
        self.SIGNIN_CLS_NAME = 't-sign-in' # class name of 'Signin'
        self.USERNAME_ID = 'id_email'    # id of input 'User Name'
        self.PASSWD_ID = 'id_password1'    # id of input 'Password'
        self.SIGNIN_BTN_CLS_NAME = 'buttongroup'    # id of button 'SIGNIN'
        
        if inter == 'Firefox':
            self.browser = webdriver.Firefox()
        elif inter == 'Chrome':
            self.browser = webdriver.Chrome()

        self.browser.get('https://' + tgt)

    def log_in(self, username, passwd):
        # go to the page of 'SIGNIN'
        ele_signin = self.browser.find_element_by_class_name(
            self.SIGNIN_CLS_NAME)
        ele_signin.click()

        # fill out fields 'username' and 'password', then click signin btn
        ele_username = self.browser.find_element_by_id(self.USERNAME_ID)
        ele_username.send_keys(username)
        ele_passwd = self.browser.find_element_by_id(self.PASSWD_ID)
        ele_passwd.send_keys(passwd)
        ele_signin_btn = self.browser.find_element_by_class_name(
            self.SIGNIN_BTN_CLS_NAME)
        ele_signin_btn.click()

    def log_out(self):
        pass

    def quit(self):
        self.browser.quit()

    def save_webpage(self, file_name):
        file_obj = open(file_name, 'w')
        # file_obj = codecs.open(file_name_full, 'w', 'utf-8')
        file_obj.write(self.browser.page_source)
        file_obj.close()


def main():
    save_path = os.path.dirname(os.path.abspath(__file__))
    tgt = 'www.safaribooksonline.com/library/view/\
        creating-apps-in/9781491947333'
    user = 'ddengca@gmail.com'
    passwd = 'safari318'

    my_web = WebCrawler(tgt)
    my_web.log_in(user, passwd)
    
    soup_toc = BeautifulSoup(my_web.browser.page_source, 'html.parser')
    
    link_text = ['Preface', 
                 '1. Introducing Kivy', 
                 '2. Events and Properties', 
                 '3. Manipulating Widgets', 
                 '4. Iterative Development',
                 '5. Kivy Graphics',
                 '6. Kivy Storage', 
                 '7. Gestures', 
                 '8. Advanced Widgets', 
                 '9. Releasing to Android and iOS', 
                 '10. Writing a Simple Mobile Game', 
                 '11. Modeling Enemies', 
                 '12. Advanced Graphics', 
                 'Index', 
                 'Colophon', 
                 'Copyright']
    pat_1 = re.compile(
        ' src="/library/view/creating-apps-in/9781491947333/callouts/\d+.png"')
    pat_2 = re.compile(
        ' src="/library/view/creating-apps-in/9781491947333/images/caky_\d+.png"')
    ct = 1
    for link_t in link_text:
        '''
        WebDriverWait(my_web.browser, 30).until(EC.element_to_be_clickable((
            By.LINK_TEXT, link)))
        # element = wait.until(EC.element_to_be_clickable((By.XPath, "//*[@title='Create Incident']")))
        loc = my_web.browser.find_element_by_link_text(link)
        loc.click()
        '''
        print(ct, link_t)
        link_url = soup_toc.find('a', href=True, text=link_t)['href']
        my_web.browser.get(
                'https://www.safaribooksonline.com' + link_url)
        soup_page = BeautifulSoup(my_web.browser.page_source,
                              'html.parser')
        soup_div = soup_page.find(name='div',
                                  attrs={'class': 'annotator-wrapper'})
        soup_sec = soup_div.find(name='section')
        file_name = r'part%04d.html' %ct
        file_name_full = os.path.join(save_path, file_name)
        my_file = open(file_name_full, 'a', encoding="utf-8")
        try:
            content = str(soup_sec)
            img2 = pat_2.findall(content)
            # print(img2)
            
            for i in img2:
                i = i[6:-1]
                u = 'https://www.safaribooksonline.com' + i
                '''
                img2_file_name = i[-20:] # 'images/caky_0102.png'
                img2_file_name_full = os.path.join(save_path, img2_file_name)
                print(img2_file_name_full)
                print(u)
                '''
                img2_file_name = i[-13:]
                img2_file_name_full = os.path.join(save_path, img2_file_name)
                urllib.request.urlretrieve(u, img2_file_name)
            
            content = content.replace(
                    '/library/view/creating-apps-in/9781491947333/callouts/',
                    'images/callouts/')
            content = content.replace(
                    '/library/view/creating-apps-in/9781491947333/images/',
                    'images/')
            my_file.write(content)
        except Exception as e:
            print('Exception: ' + str(e))
        my_file.close
        ct += 1
    
        #Ask Selenium to click the back button
        # my_web.browser.execute_script("window.history.go(-1)")
        my_web.browser.back()
    my_web.quit()


if __name__ == '__main__':
    main()
