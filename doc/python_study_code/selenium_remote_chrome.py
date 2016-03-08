#!/usr/bin/env python
# coding=utf-8
#remote chrome localIP 
#java -jar selenium-server-standalone-2.43.1.jar -port 44444 -Dwebdriver.chrome.driver=/home/softs/selenium/chromedriver
import os
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

from time import sleep
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

tommy_remote_url = 'http://192.168.85.123:44444/wd/hub'
derek_remote_url = 'http://192.168.87.72:18181/wd/hub'

driver = webdriver.Remote(
    command_executor=tommy_remote_url,
    desired_capabilities=DesiredCapabilities.CHROME)

'''
driver = webdriver.Remote(
   command_executor='http://127.0.0.1:4444/wd/hub',
   desired_capabilities=DesiredCapabilities.OPERA)

driver = webdriver.Remote(
   command_executor='http://127.0.0.1:4444/wd/hub',
   desired_capabilities=DesiredCapabilities.HTMLUNITWITHJS)

'''
driver.get("http://www.baidu.com")
eg_title = "百度"
print driver.title

try:
    if not eg_title in driver.title:
        raise Exception("Unable to load", eg_title, " page!")

    elem = driver.find_element_by_name("wd")
    elem.send_keys("domain")
    elem.submit()
    sleep(10)
except Exception, e:
    raise e
finally:
    driver.quit()
