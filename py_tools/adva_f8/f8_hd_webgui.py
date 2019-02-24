#! /usr/bin/env python
# _*_ coding: utf-8

from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
from time import sleep

SAVE_PATH = '/home/user'


class F8Webgui(object):
    """Library for Adva F8 WebGUI."""

    def __init__(self, inter='Firefox'):
        self.TIMEOUT = 30    # 30 sec
        self.USERNAME_ID = 'widget_user'    # id of input 'User Name'
        self.PASSWD_ID = 'widget_password'    # id of input 'Password'
        self.LOGIN_ID = 'blogin'    # id of button 'LOGIN'
        self.CONFIRM_CLS_NAME = 'footer-form-action-button'
        # class name of button 'CONFIRM'
        self.USERMENU_CLS_NAME = 'nav-bar-user-btn'
        # class name of button 'User Menu'

        if inter == 'Firefox':
            self.browser = webdriver.Firefox()
        elif inter == 'Chrome':
            self.browser = webdriver.Chrome()

    def log_in(self, ip, username='admin', passwd='chgme.1a'):
        self.browser.get('http://' + ip)

        # fill out fields 'username' and 'password'
        # ele_username = self.browser.find_element_by_id(self.USERNAME_ID)
        # ele_username.click()
        ele_username = self.browser.find_element_by_id('user')
        ele_username.send_keys(username)
        # ele_passwd = self.browser.find_element_by_id(self.PASSWD_ID)
        # ele_passwd.send_keys(passwd)
        # ele_login = self.browser.find_element_by_id(self.LOGIN_ID)

        # click button 'LOGIN'
        # ele_login.click()

        # get button 'CONFIRM'
        # ele_confirm = browser.find_element_by_css_selector(
        #     '.footer-form-action-button')
        # ele_confirm = browser.find_element_by_class_name(
        #     'footer-form-action-button')
        # wait = WebDriverWait(self.browser, self.TIMEOUT)
        # ele_confirm = wait.until(EC.presence_of_element_located(
        #     (By.CLASS_NAME, self.CONFIRM_CLS_NAME)
        # ))

        # click button 'CONFIRM'
        # ele_confirm.click()

    def log_out(self):
        # get button 'User Menu'
        # ele_usermenu = browser.find_element_by_class_name(
        #     'nav-bar-user-btn')
        # wait = WebDriverWait(self.browser, self.TIMEOUT)
        # ele_usermenu = wait.until(EC.presence_of_element_located(
        #     (By.CLASS_NAME, self.USERMENU_CLS_NAME)
        # ))

        # click button 'User Menu'
        # ele_usermenu.click()

        # click button 'Logout'
        # ele_logout = self.browser.find_element_by_xpath(
        #     '//div[@ng-click="logOut()"]')
        ele_logout = self.browser.find_element_by_id('header-logout')
        ele_logout.click()

    def quit(self):
        self.browser.quit()

    def create_entity(self, shelf, slot, type_eqpt, **kwargs):
        # get element of card 3
        # ele_context_menu = self.browser.find_element_by_xpath(
        #     '//svg[@x="13109"]')
        ele_context_menu = self.browser.find_element_by_xpath(
            '//div[@style="width:100%;height: 0; padding: 0; "]\
            //*[local-name()="svg"][16]')

        # right click on card 3
        actionChains = ActionChains(self.browser)
        actionChains.context_click(ele_context_menu).perform()

        # click 'Add Equipment'
        sleep(10)
        ele_add_eqpt = self.browser.find_element_by_xpath(
            '//*[contains(text(), "Add Equipment")]')
        ele_add_eqpt.click()

        # click 'Card Type'
        sleep(10)
        ele_card_type = self.browser.find_element_by_xpath(
            '//div[@label="Card Type"]')
        ele_card_type.click()

        # click 'AM-S20H-2'
        sleep(10)
        ele_type_eqpt = self.browser.find_element_by_xpath(
            '//*[contains(text(), "AM-S20H-2")]')
        ele_type_eqpt.click()

        # click 'CREATE'
        sleep(10)
        ele_create = self.browser.find_element_by_xpath(
            '//*[contains(text(), "Create")]')
        ele_create.click()

    def destroy_entity(self, shelf, slot):
        ele_context_menu = self.browser.find_element_by_xpath(
            '//div[@style="width:100%;height: 0; padding: 0; "]\
            //*[local-name()="svg"][16]')

        # right click on card 3
        actionChains = ActionChains(self.browser)
        actionChains.context_click(ele_context_menu).perform()

        # click 'Delete'
        sleep(10)
        ele_del_eqpt = self.browser.find_element_by_xpath(
            '//*[contains(text(), "Delete")]')
        ele_del_eqpt.click()

        # click 'OK'
        sleep(10)
        # self.save_webpage('f8_del_ok.html')
        ele_ok = self.browser.find_element_by_xpath(
            '//*[contains(text(), "OK")]')
        ele_ok.click()

    def get_entity_param(self, shelf, slot, **kwargs):
        pass

    def set_entity_param(self, shelf, slot, **kwargs):
        pass

    def save_webpage(self, file_name):
        file_obj = open(file_name, 'w')
        # file_obj = codecs.open(file_name_full, 'w', 'utf-8')
        file_obj.write(self.browser.page_source)
        file_obj.close()


def main():
    # inter = 'Chrome'
    ip = '10.19.40.10'
    my_f8 = F8Webgui()
    sleep(10)
    file_name = 'f8_hd_login.html'
    file_name_full = os.path.join(SAVE_PATH, file_name)
    my_f8.save_webpage(file_name_full)
    
    # my_f8.log_in(ip)

    # sleep(30)
    # file_name = 'f8_create_card.html'
    # file_name_full = os.path.join(SAVE_PATH, file_name)
    # my_f8.save_webpage(file_name_full)
    # type_eqpt = 'AM-S20H-2'
    # my_f8.create_entity(1, 5, type_eqpt)
    # my_f8.destroy_entity(1, 5)
    # my_f8.log_out()
    # my_f8.quit()


if __name__ == '__main__':
    main()
