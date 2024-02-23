import inspect
import os
import ast
import sys
import traceback
import concurrent.futures
from selenium import webdriver
from selenium.webdriver import Chrome, Edge, Firefox

project_dir = os.path.abspath(__file__).split("core")[0]
test_dir = os.path.join(project_dir, "tests")

sys.path.append(test_dir)

def browser():
    pass

def get_driver(browser_name)-> Chrome | Edge | Firefox:
    if browser_name.lower() == 'chrome':
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("--enable-chrome-browser-cloud-management")
        return webdriver.Chrome(options=chrome_options)
    elif browser_name.lower() == 'firefox':
        return webdriver.Firefox()
    elif browser_name.lower() == 'edge':
        edge_options = webdriver.EdgeOptions()
        edge_options.add_argument("--enable-chrome-browser-cloud-management")
        return webdriver.Edge(options=edge_options)
    else:
        raise ValueError(f"unsupported browser - {browser_name}")

def beforetest(func):
    def wrapper(*args, **kwargs):
        print(f"Before executing the {func.__name__} method")
        try:
            result = func(*args, **kwargs)
        except AssertionError as ae:
            if ae.args:
                return None, ae.args[0]
            else:
                return None, traceback.format_exc()
        except Exception as e:
            return None, traceback.format_exc()
        else:
            return result, None
    return wrapper


def testcase(tag: list[str] = None, browser=None):
    def decorator(func):
        def wrapper(*args, **kwargs):
            if browser is not None:
                driver:Chrome | Edge | Firefox = get_driver(browser)
            try:
                if browser is not None:
                    print(type(browser) == str)
                    result = func(*args, **kwargs, browser = driver)
                else:
                    result = func(*args, **kwargs)
            except AssertionError as ae:
                if ae.args:
                    return None, ae.args[0]
                else:
                    return None, traceback.format_exc()
            except Exception as e:
                return None, traceback.format_exc()
            else:
                return result, None
            finally:
                if browser is not None:
                    driver.quit()
                print(f"After executing the {func.__name__}")
        return wrapper
    return decorator


def get_decorators(function):
    source = inspect.getsource(function)
    index = source.find("def ")
    return [
        line.strip().split()[0]
        for line in source[:index].strip().splitlines()
        if line.strip().startswith("@")
    ]


testcase_storage = {}

def is_testcase_present(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        source_code = file.read()
        if "@testcase" in source_code:
            return True
        else:
            return False

def remove_cache_directories(directory, folder_name):
    for root, dirs, files in os.walk(directory):
        if folder_name in dirs:
            cache_dir = os.path.join(root, folder_name)
            try:
                for item in os.listdir(cache_dir):
                    item_path = os.path.join(cache_dir, item)
                    if os.path.isfile(item_path):
                        os.unlink(item_path)
                    else:
                        for sub_item in os.listdir(item_path):
                            sub_item_path = os.path.join(item_path, sub_item)
                            os.unlink(sub_item_path)
                        os.rmdir(item_path)
                os.rmdir(cache_dir)
            except Exception as e:
                print(f"Error removing {folder_name} directory: {e}")

def execute_tests(max_threads:int = 1):
    for module_name in os.listdir(test_dir):
        if (
            module_name.endswith(".py")
            and module_name != "__init__.py"
        ):
            module_path = os.path.join(test_dir, module_name)
            if is_testcase_present(module_path):
                module_name = module_name[:-3]
                module = __import__(module_name)
                for name, obj in inspect.getmembers(module):
                    if inspect.isfunction(obj):
                        if obj.__closure__ is not None:
                            for cell in obj.__closure__:
                                if isinstance(cell.cell_contents, type(execute_tests)):
                                    testcase_storage[f"{module_name}.{name}"] = obj
    next_execution(max_threads)
    remove_cache_directories(project_dir,"__pycache__")  



def next_execution(max_threads):
    test_results = {}

    with concurrent.futures.ThreadPoolExecutor(max_workers=max_threads) as executor:
        futures = {
            executor.submit(value): key for key, value in testcase_storage.items()
        }

        for future in concurrent.futures.as_completed(futures):
            key = futures[future]
            test_results[key] = {}

            try:
                result, error = future.result()
                if error:
                    test_results[key]["status"] = "Failed"
                    test_results[key]["error"] = error
                else:
                    test_results[key]["status"] = "Passed"

            except Exception as e:
                test_results[key]["status"] = "Failed"
                test_results[key]["error"] = traceback.format_exc()

    for method_name, result in test_results.items():
        if result["status"] == "Failed":
            print(f"\n\033[91m{method_name}: Failed\033[0m \n{result['error']}")
        else:
            print(f"\n\033[92m{method_name}: Passed\033[0m")
    

class Browser(Chrome, Firefox, Edge):
    pass