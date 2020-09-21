import time

from selenium import webdriver
from selenium.webdriver import Proxy
from selenium.webdriver.common.proxy import ProxyType




driver = webdriver.Firefox(executable_path=r'../geckodriver.exe')
driver.get("https://kart.1881.no/?query=oslo&type=adresse")
time.sleep(10)
elements = driver.find_elements_by_xpath("//a")
click_element = None
for element in elements:
    if "Personer" in element.text:
        click_element = element
click_element.click()
time.sleep(5)
people = driver.find_elements_by_class_name("result-item")
for person in people:
    name_class = person.find_element_by_class_name("result-item-name")
    location_class = person.find_element_by_class_name("result-item-address")
    print(name_class.text,location_class.text)
    coordinates_button = person.find_element_by_class_name("link-directions")
    name_class.click()
    time.sleep(3)
    driver.back()
