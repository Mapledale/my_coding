#! /usr/bin/env python
# _*_ coding: utf-8 _*_

from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common import exceptions
# import os
import random
from time import sleep
from pexpect.pxssh import pxssh

SAVE_PATH = '/home/user/my_codes/py_ex/'


class F8Webgui(object):
    """Library for Adva F8 WebGUI."""

    def __init__(self, inter='Firefox'):
        self.TIMEOUT = 30    # 30 sec
        self.USERNAME_ID = 'username'    # id of input 'User Name'
        self.PASSWD_ID = 'password'    # id of input 'Password'
        self.LOGIN_ID = 'signin-btn'    # id of button 'LOGIN'
        self.CONFIRM_CLS_NAME = 'footer-form-action-button'
        # class name of button 'CONFIRM'
        self.USERMENU_CLS_NAME = 'nav-bar-user-btn'
        # class name of button 'User Menu'
        self.SLOT_TO_SVG = {'10': '1',
                            '11': '21',
                            '13': '12',
                            '14': '14',
                            '15': '15',
                            '16': '16',
                            '17': '17',
                            '18': '18',
                            '19': '19',
                            '20': '20'}

        if inter == 'Firefox':
            self.browser = webdriver.Firefox()
        elif inter == 'Chrome':
            self.browser = webdriver.Chrome()

    def log_in(self, ip, username='admin', passwd='CHGME.1a'):
        self.browser.get('http://' + ip)

        # fill out fields 'username' and 'password'
        ele_username = self.browser.find_element_by_id(self.USERNAME_ID)
        ele_username.send_keys(username)
        ele_passwd = self.browser.find_element_by_id(self.PASSWD_ID)
        ele_passwd.send_keys(passwd)
        ele_login = self.browser.find_element_by_id(self.LOGIN_ID)

        # click button 'LOGIN'
        ele_login.click()

        # get button 'CONFIRM'
        # ele_confirm = browser.find_element_by_css_selector(
        #     '.footer-form-action-button')
        # ele_confirm = browser.find_element_by_class_name(
        #     'footer-form-action-button')
        wait = WebDriverWait(self.browser, self.TIMEOUT)
        ele_confirm = wait.until(EC.presence_of_element_located(
            (By.CLASS_NAME, self.CONFIRM_CLS_NAME)
        ))

        # click button 'CONFIRM'
        ele_confirm.click()

        # wait for the webpage loaded until alarms are updated
        loc = '//div[@style="width:100%;height: 0; padding: 0; "]\
            //*[local-name()="svg"][26]'
        wait.until(EC.presence_of_element_located(
            (By.XPATH, loc)))

    def log_out(self):
        # get button 'User Menu'
        # ele_usermenu = browser.find_element_by_class_name(
        #     'nav-bar-user-btn')
        wait = WebDriverWait(self.browser, self.TIMEOUT)
        ele_usermenu = wait.until(EC.presence_of_element_located(
            (By.CLASS_NAME, self.USERMENU_CLS_NAME)
        ))

        # click button 'User Menu'
        ele_usermenu.click()

        # click button 'Logout'
        ele_logout = self.browser.find_element_by_xpath(
            '//div[@ng-click="logOut()"]')
        ele_logout.click()

    def quit(self):
        self.browser.quit()

    def slot_to_x(self, slot):
        x = int(slot) * 2032 + 2949
        return str(x)

    def create_entity(self, shelf, slot, type_eqpt, **kwargs):
        # get element of card at slot
        # ele_context_menu = self.browser.find_element_by_xpath(
        #     '//svg[@x="13109"]')
        # trial 1: calculate x and use css selector
        # x = self.slot_to_x(slot)
        # loc = 'svg[x="' + x + '"]'
        # ele_context_menu = self.browser.find_element_by_css_selector(loc)
        # trial 2: use x with xpath
        # loc = '//svg[@x="' + x + '"]'  # this doesn't work with xpath
        # trial 3:
        loc = '//div[@style="width:100%;height: 0; padding: 0; "]\
            //*[local-name()="svg"][' + self.SLOT_TO_SVG[slot] + ']'
        ele_context_menu = self.browser.find_element_by_xpath(loc)
        # ele_context_menu = self.browser.find_element_by_xpath(
        #     '//div[@style="width:100%;height: 0; padding: 0; "]\
        #     //*[local-name()="svg"][16]')

        # right click on card
        actionChains = ActionChains(self.browser)
        actionChains.context_click(ele_context_menu).perform()

        # click 'Add Equipment'
        sleep(5)
        loc_add_eqpt = '//*[contains(text(), "Add Equipment")]'
        wait = WebDriverWait(self.browser, self.TIMEOUT)
        ele_add_eqpt = wait.until(EC.presence_of_element_located(
            (By.XPATH, loc_add_eqpt)))
        # ele_add_eqpt = self.browser.find_element_by_xpath(loc_add_eqpt)
        ele_add_eqpt.click()

        # click 'Card Type'
        sleep(5)
        loc_card_type = '//div[@label="Card Type"]'
        ele_card_type = wait.until(EC.presence_of_element_located(
            (By.XPATH, loc_card_type)))
        # ele_card_type = self.browser.find_element_by_xpath(
        #     '//div[@label="Card Type"]')
        ele_card_type.click()

        # click on type_eqpt
        loc_type_eqpt = '//*[contains(text(), "' + type_eqpt + '")]'
        ele_type_eqpt = wait.until(EC.presence_of_element_located(
            (By.XPATH, loc_type_eqpt)))
        # sleep(10)
        # ele_type_eqpt = self.browser.find_element_by_xpath(loc_type_eqpt)
        # ele_type_eqpt = self.browser.find_element_by_xpath(
        #     '//*[contains(text(), "AM-S20H-2")]')
        ele_type_eqpt.click()

        # click 'CREATE'
        loc_create = '//*[contains(text(), "Create")]'
        ele_create = wait.until(EC.presence_of_element_located(
            (By.XPATH, loc_create)))
        # sleep(10)
        # ele_create = self.browser.find_element_by_xpath(loc_create)
        ele_create.click()

    def destroy_entity(self, shelf, slot):
        # trial 1: calculate x and use css selector
        # x = self.slot_to_x(slot)
        # loc = 'svg[x="' + x + '"]'
        # ele_context_menu = self.browser.find_element_by_css_selector(loc)
        # trial 2: use x with xpath
        # loc = '//svg[@x="' + x + '"]'  # this one doesn't work with xpath
        # trial 3:
        loc = '//div[@style="width:100%;height: 0; padding: 0; "]\
            //*[local-name()="svg"][' + self.SLOT_TO_SVG[slot] + ']'
        ele_context_menu = self.browser.find_element_by_xpath(loc)
        # ele_context_menu = self.browser.find_element_by_xpath(
        #     '//div[@style="width:100%;height: 0; padding: 0; "]\
        #     //*[local-name()="svg"][16]')

        # right click on card
        actionChains = ActionChains(self.browser)
        actionChains.context_click(ele_context_menu).perform()

        # click 'Delete'
        loc_del_eqpt = '//*[contains(text(), "Delete")]'
        wait = WebDriverWait(self.browser, self.TIMEOUT)
        ele_del_eqpt = wait.until(EC.presence_of_element_located(
            (By.XPATH, loc_del_eqpt)))
        # sleep(10)
        # ele_del_eqpt = self.browser.find_element_by_xpath(loc_del_eqpt)
        ele_del_eqpt.click()

        # click 'OK'
        loc_ok = '//*[contains(text(), "OK")]'
        ele_ok = wait.until(EC.presence_of_element_located(
            (By.XPATH, loc_ok)))
        # sleep(10)
        # self.save_webpage('f8_del_ok.html')
        # ele_ok = self.browser.find_element_by_xpath(loc_ok)
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


def set_card_oos(ip, shelf, slot, user='admin', passwd='CHGME.1a'):
    my_f8_ssh = pxssh()
    # 3 cases of prompt: 'admin@FSP3000C> ',
    # 'admin@FSP3000C# ', 'admin@FSP3000C*# '
    my_f8_ssh.PROMPT = r"admin@FSP3000C[*]?[#>] "
    my_f8_ssh.login(ip, user, passwd, auto_prompt_reset=False)
    # disable auto_prompt_reset as my_f8_ssh.PROMPT is explicitly defined
    my_f8_ssh.prompt()
    my_f8_ssh.before  # to consume the warning after login

    cmd = 'configure'  # enter configure mode
    my_f8_ssh.sendline(cmd)
    my_f8_ssh.prompt()
    my_f8_ssh.before

    cmd = 'set card ' + shelf + '/' + slot + ' admin oos'
    my_f8_ssh.sendline(cmd)
    my_f8_ssh.prompt()
    my_f8_ssh.before

    cmd = 'commit'
    my_f8_ssh.sendline(cmd)
    my_f8_ssh.prompt()
    my_f8_ssh.before

    cmd = 'exit'  # exit configure mode
    my_f8_ssh.sendline(cmd)
    my_f8_ssh.prompt()
    my_f8_ssh.before

    my_f8_ssh.logout()


def crud(web, ip, shelf, slot, type_eqpt):
    print('Creating %s at slot %s...' % (type_eqpt, slot))
    try:
        web.create_entity(shelf, slot, type_eqpt)
        sleep(5)
        print('Card created!')
    except exceptions.NoSuchElementException:
        print("wrong element picked!")
        print("jump to next case...")

    print('Setting card to oos...')
    set_card_oos(ip, shelf, slot)
    print('Card set to oos!')

    print('Destroying the card...')
    web.destroy_entity(shelf, slot)
    print('Card destroyed!')
    print('+++++++++++++++++++++++++++')


def main():
    EQPT_RAW = {'AM-S20H-2': 1,
            'AM-S23H': 1,
            'AM-S23L-TD': 3,
            'AM-S23L': 1,
            'MA-B2C3LT-A': 'na',
            'MA-2C2C3LT-A': 'na',
            'FD-40D24L-TD': 4,
            'FD-48E': 1,
            'MA-B5LT': 'na',
            'MA-2C5LT': 'na',
            'MP-2B4CT-S': 'na',
            'MP-2B4CT': 'na',
            'Tst Tm2 Cc3 Card': 1}
    EQPT = {'AM-S20H-2': 1,
            'AM-S23H': 1,
            'AM-S23L-TD': 3,
            'AM-S23L': 1,
            'FD-40D24L-TD': 4,
            'FD-48E': 1,
            'Tst Tm2 Cc3 Card': 1}
    # inter = 'Chrome'
    ip = '172.16.37.22'
    # user = 'admin'
    # passwd = 'CHGME.1a'
    shelf = '1'

    my_f8 = F8Webgui()
    my_f8.log_in(ip)
    # sleep(5)
    # file_name = 'f8_create_card_new.html'
    # file_name_full = os.path.join(SAVE_PATH, file_name)
    # my_f8.save_webpage(file_name_full)
    for s in range(10, 13):
        if s == 12:
            continue
        while True:
            type_eqpt = random.choice(EQPT.keys())
            if EQPT[type_eqpt] + s < 21:
                break
        slot = str(s)
        crud(my_f8, ip, shelf, slot, type_eqpt)
    sleep(5)
    my_f8.log_out()
    sleep(5)
    my_f8.quit()


if __name__ == '__main__':
    main()
