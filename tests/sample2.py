import inspect
from core.pyvic.base.test_base import Browser, beforetest, get_driver, testcase
from time import sleep


def tester(func):
    pass


@testcase(browser="firefox")
def sample_2(browser):
    browser.get("https://www.google.com")
    sleep(10)
    print("Executing sample_2")


@testcase(tag=["smoke"])
def sample_4():
    print("Executing sample_4")
    assert 1 == 0


@testcase()
def sample_6():
    print("Executing sample_6")
    assert 1 == 1

@beforetest(tag=["smoke"])
def sample_7():
    print(f"Before executing the")
    
@beforetest()
def sample_8():
    print(f"Before executing the")
