# -*- coding: utf-8 -*-
from lettuce import *
from lettuce_webdriver.util import AssertContextManager  
  
from selenium import webdriver  
from selenium.webdriver.common.keys import Keys
import lettuce_webdriver.webdriver  

@before.all
def setup_browser():
    driver = webdriver.Firefox()
    driver.get("http://mawd1tic.com/maw/")
    elem = driver.find_element_by_css_selector("#content > div > div > div:nth-child(3) > div > div > div.span6.plain_text.alignment_left > h1")
    assert elem.text == "Nuestros Servicios"
    driver.close() 

