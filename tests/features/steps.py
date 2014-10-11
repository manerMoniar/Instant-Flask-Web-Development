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

def encontrar_campo_por_clase(browser, attribute):
    xpath = "//input[@class='%s']" % attribute
    elems = browser.find_elements_by_xpath(xpath)
    return elems[0] if elems else False

@step(u'Dado que vaya a "([^"]*)"')
def dado_que_vaya_a_lista_citas(step, url):
    world.response = world.browser.get(url)


@step(u'Debo ver la "([^"]*)" cita "([^"]*)"')
def debo_ver_la_cita(step, numero, cita):
    element = world.browser.find_element_by_css_selector("#main > div.content.container > div > div:nth-child("+numero+") > div > h3 > a")
    assert element.text == cita