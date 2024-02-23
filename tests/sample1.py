import inspect
from core.pyvic.base.test_base import Browser, get_driver, testcase
from time import sleep


def tester(func):
    pass


@testcase(browser="chrome")
def sample_1(browser: Browser):
    browser.get("https://www.google.com")
    sleep(10)
    print("Executing sample_1")


@testcase(tag=["smoke"])
def sample_3():
    print("Executing sample_3")
    raise Exception("My custom")


@testcase(tag=["smoke"])
def sample_5():
    print("Executing sample_5")
    raise ValueError()
