#!/usr/bin/env python
# -*- utf-8 -*-

'''
for Selenuim, webdriver
'''

from selenium import webdriver
from selenium.webdriver.common.by import By

# xpath
str1 = 'example1'
str2 = 'example2'

# a span below something (*), whose id is ';example1'
loc = "//*[@id=';%s']/span" % str_ex

# a table row, under a div, which contains 'example1' in its id, then a table, then a tbody.
# this table row contains a standard cell, which contains 'example2' 
loc = "//div[contains(@id, '%s')]/table/tbody/tr[td[contains(., '%s')]]" % (str1, str2)

# the 2nd standard cell of a tr
loc = "//*[@id = 'example']/tbody/tr/td[2]"

# firstly found a span, then go up a level, then find a div
loc = "//span[@id = 'example']/../div[contains(., 'something')]"

browser = webdriver.Chrome()
# to use Selenium with remote WebDriver
server_ip = '10.16.24.16'
browser = webdriver.Remote(
    desired_capabilities = webdriver.DesiredCapabilities.CHROME,
    command_executor = 'http://%s:4444/wd/hub' % server_ip
)

if loc.startswith('/') or loc.startswith('(/'):
    by_type = By.XPATH
else:
    by_type = By.ID

elem = browser.find_element(by_type, loc)

# to get properties of an element
elem_tag = elem.tag_name # e.g. input, span, button, div
elem_type = elem.get_attribute('type')
elem_role = elem.get_attribute('role')
