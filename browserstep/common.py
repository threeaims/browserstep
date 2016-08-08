# -*- coding: utf-8 -*-
# Copyright James Gardner MIT license

import os
import time
import re

from behave import *
from selenium import webdriver
from selenium.webdriver.support.ui import Select

from selenium.webdriver.common.action_chains import ActionChains


@step('I hover over "{container_selector}"')
def step_impl(context, container_selector):
    element_to_hover_over = context.browser.find_element_by_css_selector(container_selector)
    hover = ActionChains(context.browser).move_to_element(element_to_hover_over)
    hover.perform()
    time.sleep(0.7)


@step('I follow the "{text}" link in "{container_selector}"')
def step_impl(context, text, container_selector):
    container = context.browser.find_element_by_css_selector(container_selector)
    elements = container.find_elements_by_link_text(text)
    if not elements:
        elements = container.find_elements_by_xpath("//img[contains(@alt,'{}')]".format(text))
    assert len(elements) == 1, "Expected 1 matching link, not {}".format(len(elements))
    elements[0].click()


@step('I navigate to /{path}')
def step_impl(context, path):
    context.browser.get(context.config.userdata['test_host'] + '/' + path)

@step('I navigate to the formatted URL /{path}')
def step_impl(context, path):
    context.browser.get((context.config.userdata['test_host'] + '/' + path).format(**context.variables))

@step('I navigate to /')
def step_impl(context):
    context.browser.get(context.config.userdata['test_host'] + '/')

@step('the browser moves to /{path}')
def step_impl(context, path):
    expected_url = context.config.userdata['test_host'] + '/' + path
    assert expected_url == context.browser.current_url, "Expected browser to be at {!r} but it as at {!r}".format(expected_url, context.browser.current_url)

@step('the browser moves to /')
def step_impl(context):
    expected_url = context.config.userdata['test_host'] + '/'
    assert expected_url == context.browser.current_url, "Expected browser to be at {!r} but it as at {!r}".format(expected_url, context.browser.current_url)

@step('the browser is still at /')
def step_impl(context):
    context.execute_steps('Then the browser moves to /')

@step('the browser is still at /{path}')
def step_impl(context, path):
    context.execute_steps('Then the browser moves to /{}'.format(path))

@step('the browser is at the formatted URL /{path}')
def step_impl(context, path):
    expected_url = (context.config.userdata['test_host'] + '/' + path).format(**context.variables)
    assert expected_url == context.browser.current_url, "Expected browser to be at {!r} but it as at {!r}".format(expected_url, context.browser.current_url)

@step('I click on "{selector}"')
def step_impl(context, selector):
    element = context.browser.find_element_by_css_selector(selector)
    assert element is not None, "No such element found"
    element.click()

@step('I follow the "{text}" link')
def step_impl(context, text):
    elements = context.browser.find_elements_by_link_text(text)
    if not elements:
        elements = context.browser.find_elements_by_xpath("//img[contains(@alt,'{}')]".format(text))
    assert len(elements) == 1, "Expected 1 matching link, not {}".format(len(elements))
    elements[0].click()

@step('I click the "{text}" button')
def step_impl(context, text):
    element = context.browser.find_element_by_xpath("//button[contains(text(), '{}')] | //input[@type='submit' and contains(@value,'{}')]".format(text, text))
    assert element is not None, "No such button found"
    element.click()

@step('I click the "{text}" label')
def step_impl(context, text):
    element = context.browser.find_element_by_xpath("//label[contains(text(), '{}')]".format(text))
    assert element is not None, "No such label found"
    element.click()

@step('I wait {seconds} seconds')
def step_impl(context, seconds):
    time.sleep(float(seconds))

@step('I wait 1 second')
def step_impl(context):
    time.sleep(1)

@step('there are {n} "{selector}" elements in "{container_selector}"')
def step_impl(context, n, selector, container_selector):
    container = context.browser.find_element_by_css_selector(container_selector)
    elements = container.find_elements_by_css_selector(selector)
    assert len(elements) != n, "Expected {} elements, got {}".format(n, len(elements))

@step('there is 1 "{selector}" element in "{container_selector}"')
def step_impl(context, selector, container_selector):
    context.execute_steps('Then there are 1 "%s" elements in "%s"' % (selector, container_selector))

@step('there are {n:d} "{selector}" elements')
def step_impl(context, n, selector):
    context.execute_steps('Then there are %d "%s" elements in "html"' % (n, selector))

@step('there is 1 "{selector}" element')
def step_impl(context, selector):
    context.execute_steps('Then there are 1 "%s" elements in "html"' % (selector))

@step('I see "{text}" in "{container}"')
def step_impl(context, text, container):
    element = context.browser.find_element_by_css_selector(container)
    assert element is not None and text in element.get_attribute('textContent'), "Did not find text"

def strip_all_whitespace(text):
    return text.replace(' ', '').replace('\n', '').replace('\t', '')

@step('"{selector}" has the following text with all whitespace removed')
def step_impl(context, selector):
    element = context.browser.find_element_by_css_selector(selector)
    assert element is not None and strip_all_whitespace(context.text) == strip_all_whitespace(element.get_attribute('textContent')), "Different: {}".format(element.get_attribute('textContent'))


import subprocess

@step('I run the following command')
def step_impl(context):
    context.output = None
    p = subprocess.Popen(
        context.text,
        cwd=context.config.userdata.get("cwd", os.getcwd()),
        shell=True,
        stdout=subprocess.PIPE
    )
    context.output, err = p.communicate()
    assert 0 == p.wait(), "Non-zero exit status"

import difflib

@step('there is no output')
def step_impl(context):
    assert context.output is not None, "No command has been run yet, so there is no output"
    assert context.text == None, 'Unexpected output:\n{!s}'.format(context.text)

@step('the output is')
def step_impl(context):
    assert context.output is not None, "No command has been run yet, so there is no output"
    if context.output != context.text.encode('utf8'):
        s1 = [s+'\n' for s in context.text.split('\n')]
        s2 = [s+'\n' for s in context.output.split('\n')]
        assert False, '\n'+(''.join(difflib.unified_diff(s1, s2, fromfile='expected', tofile='actual')))

@step('I type "{text}" into "{selector}"')
def step_impl(context, text, selector):
    element = context.browser.find_element_by_css_selector(selector)
    assert element is not None, "No such element found"
    element.clear()
    element.send_keys(text)


@step('I type "" into "{selector}"')
def step_impl(context, selector):
    element = context.browser.find_element_by_css_selector(selector)
    assert element is not None, "No such element found"
    element.clear()


@step('I type the following into "{selector}"')
def step_impl(context, selector):
    element = context.browser.find_element_by_css_selector(selector)
    assert element is not None, "No such element found"
    element.clear()
    element.send_keys(context.text)

@step('I\'m using the {name} browser')
def step_impl(context, name):
    context.browser = getattr(context, name+'_browser')

@step('I switch to the {name} browser')
def step_impl(context, name):
    context.execute_steps("Given I'm using the {} browser".format(name))

@step('I capture the value of "{selector}" to the "{name}" variable')
def step_impl(context, selector, name):
    element = context.browser.find_element_by_css_selector(selector)
    assert element is not None, "No such element found"
    value = element.get_attribute("value")
    if not hasattr(context, 'variables'):
        context.variables = {}
    context.variables[name] = value
    print(context.variables)

@step('I capture the value of "{regex}" in the URL to the "{name}" variable')
def step_impl(context, regex, name):
    if not hasattr(context, 'variables'):
        context.variables = {}
    reg = re.compile(regex)
    string = context.browser.current_url
    value = reg.search(string).group(1)
    context.variables[name] = value
    print(context.variables)

@step('the value of "{selector}" is "{value}"')
def step_impl(context, selector, value):
    element = context.browser.find_element_by_css_selector(selector)
    assert element is not None, "No such element found"
    assert value == element.get_attribute("value"), '{} != {}'.format(value, element.get_attribute("value"))


@step(u'"{selector}" is checked')
def step_impl(context, selector):
    element = context.browser.find_element_by_css_selector(selector)
    assert element is not None, "No such element found"
    assert element.get_attribute('checked') == 'true', "Element is not checked"


@step(u'"{selector}" is not checked')
def step_impl(context, selector):
    element = context.browser.find_element_by_css_selector(selector)
    assert element is not None, "No such element found"
    assert element.get_attribute('checked') is None, "Element is checked"


@step('I choose "{choice}" from "{selector}"')
def step_impl(context, choice, selector):
    select = Select(
        context.browser.find_element_by_css_selector(selector)
    )
    select.select_by_visible_text(choice)
    # select.select_by_value(choice)

