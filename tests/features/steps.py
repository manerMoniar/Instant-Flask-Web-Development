# -*- coding: utf-8 -*-
from lettuce import *
from lettuce_webdriver.util import AssertContextManager  
  
from selenium import webdriver  
from selenium.webdriver.common.keys import Keys
import lettuce_webdriver.webdriver  

@before.all
def setup_browser():
    world.browser = webdriver.Firefox()


@step(u'Dado que vaya a "([^"]*)"')
def dado_que_vaya_a_lista_citas(step, url):
    world.response = world.browser.get(url)