import inspect
from core.kmdv.base.test_base import Browser, get_driver, testcase
from time import sleep
def tester(func):
    pass

@testcase(browser="chrome")
def sample_1(browser:Browser):
    browser.get("https://www.google.com")
    sleep(10)
    print("Executing test_1")
    
@testcase(browser="firefox")
def sample_2(browser):
    browser.get("https://www.google.com")
    sleep(10)
    print("Executing test_2")

@testcase(tag=['smoke'])
def sample_3():
    print("Executing test_3")
    raise Exception("My custom")

@testcase(tag=['smoke'])
def sample_4():
    print("Executing test_4")
    assert 1 == 0

@testcase(tag=['smoke'])
def sample_5():
    print("Executing test_3")
    raise ValueError()

@testcase(tag=['smoke'])
def sample_6():
    print("Executing test_4")
    assert 1 == 1
