# -*- coding: utf-8 -*-
from lettuce import *
from lettuce_webdriver.util import AssertContextManager  
from datetime import datetime  
from selenium import webdriver  
from selenium.webdriver.common.keys import Keys
import lettuce_webdriver.webdriver  

@before.all
def setup_browser():
    world.browser = webdriver.Firefox()
    world.browser.implicitly_wait(10) #wait 10 seconds when doing a find_element before carrying 
    
@after.all
def close_browser(total):
    world.browser.quit()

@step(u'Dado que vaya a "([^"]*)"')
def dado_que_vaya_a_lista_citas(step, url):
    world.response = world.browser.get(url)


@step(u'Debo ver la "([^"]*)" cita "([^"]*)"')
def debo_ver_la_cita(step, numero, cita):
    element = world.browser.find_element_by_css_selector("#main > div.content.container > div > div:nth-child("+numero+") > div > h3 > a")
    assert element.text == cita