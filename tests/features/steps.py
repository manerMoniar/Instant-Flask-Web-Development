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


@step(u'Debo llenar el campo "([^"]*)" con "([^"]*)"')
def debo_llenar_el_usuario_y_contrasenia(step, id, value):
    text_field = world.browser.find_element_by_id(id)
    text_field.clear()
    text_field.send_keys(value)


@step(u'y enviare el formulario')
def y_enviare_el_formulario(step):
    with AssertContextManager(step):
        form = world.browser.find_element_by_tag_name('form')
        form.submit()


@step(u'Debo ver la "([^"]*)" cita "([^"]*)"')
def debo_ver_la_cita(step, numero, cita): 
    element = world.browser.find_element_by_css_selector("#main > div.content.container > div > div:nth-child("+numero+") > div > h3 > a")
    assert element.text == cita


@step('Debo ver que el elemento con clase "(.*?)" contiene "(.*?)"')
def elemento_contiene(step, element_class, value):
    with AssertContextManager(step):
        element = world.browser.find_element_by_class_name(element_class)
        assert (value in element.text), "Got %s, %s " % (element.text, value)

@step('Debo ver que el titulo de la pagina contiene "([^"]*)"')
def debo_ver_titulo(step, title):
    with AssertContextManager(step):
        element = world.browser.find_element_by_tag_name('h2')
        assert title == element.text, "Got %s " % element.text

@step('Debo hacer clic en el boton"([^"]*)"')
def debo_hacer_clic_en_boton(step, field_class):
    with AssertContextManager(step):
        button = world.browser.find_element_by_class_name(field_class)
        button.click()

@step('Debo ver que el elemento con clase "(.*?)" no contiene "(.*?)"')
def then_the_element_with_the_class_not_contains(step, element_class, title):
    with AssertContextManager(step):
        elements = world.browser.find_elements_by_class_name(element_class)
        lst = []
        for e in elements:
            lst.append(e.text)

        assert title not in lst