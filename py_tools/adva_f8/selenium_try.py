#! /usr/bin/env python
# _*_ conding: utf-8 _*_

'''This script is a trial on selenium
'''

from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# import os
# from time import sleep

USERNAME = 'admin'
PASSWD = 'CHGME.1a'
USERNAME_ID = 'username'    # id of input 'User Name'
PASSWD_ID = 'password'    # id of input 'Password'
LOGIN_ID = 'signin-btn'    # id of button 'LOGIN'
CONFIRM_CLS_NAME = 'footer-form-action-button'
# class name of button 'CONFIRM'
USERMENU_CLS_NAME = 'nav-bar-user-btn'
# class name of button 'User Menu'

SAVE_PATH = '/home/user/my_codes/py_ex/'
BROWSER_FF = webdriver.Firefox()

browser = BROWSER_FF
file_name = 'f8_create_card_new.html'
file_name_full = SAVE_PATH + file_name
browser.get('file://' + file_name_full)

# fill out fields 'username' and 'password', and click button 'LOGIN'
# ele_username = browser.find_element_by_id(USERNAME_ID)
# ele_username.send_keys(USERNAME)
# ele_passwd = browser.find_element_by_id(PASSWD_ID)
# ele_passwd.send_keys(PASSWD)
# ele_login = browser.find_element_by_id(LOGIN_ID)
# ele_login.click()

'''
file_name = 'f8_login_confirm.html'
file_name_full = os.path.join(SAVE_PATH, file_name)
file_obj = open(file_name_full, 'w')
# file_obj = codecs.open(file_name_full, 'w', 'utf-8')
file_obj.write(browser.page_source)
file_obj.close()
'''

# get button 'CONFIRM'
# ele_confirm = browser.find_element_by_css_selector(
#     '.footer-form-action-button')
# ele_confirm = browser.find_element_by_class_name(
#     'footer-form-action-button')
# wait = WebDriverWait(browser, 30)
# ele_confirm = wait.until(EC.presence_of_element_located(
#     (By.CLASS_NAME, CONFIRM_CLS_NAME)
# ))

# click button 'CONFIRM'
# ele_confirm.click()

# get context_menu
# ele_context_menu = browser.find_element_by_xpath(
#     '//svg[@x="13109"]')
# ele = browser.find_element_by_xpath('//div[@class="root ng-scope"]')
slot = '11'
x = str(int(slot) * 2032 + 2949)
# loc = '//svg[@x="' + x + '"]'
# loc = '//div[@style="width:100%;height: 0; padding: 0; "]\
#      //*[local-name()="svg"][' + slot + ']'
# ele = browser.find_element_by_xpath(loc)
loc = 'svg[x="' + x + '"]'
ele = browser.find_element_by_css_selector(loc)
# ele = browser.find_element_by_xpath('//svg[@version="1.1"]')
print(ele.text)

# right click on card 5
# actionChains = ActionChains(self.browser)
# actionChains.context_click(ele_context_menu).perform()


# get button 'User Menu'
# ele_usermenu = browser.find_element_by_class_name(
#     'nav-bar-user-btn')
# wait = WebDriverWait(browser, 30)
# ele_usermenu = wait.until(EC.presence_of_element_located(
#     (By.CLASS_NAME, USERMENU_CLS_NAME)
# ))

# click button 'User Menu'
# ele_usermenu.click()

# click button 'Logout'
# ele_logout = browser.find_element_by_xpath(
#    '//div[@ng-click="logOut()"]')
# ele_logout.click()

# close the browser
# browser.quit()
