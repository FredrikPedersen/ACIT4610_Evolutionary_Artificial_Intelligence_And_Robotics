import time

from selenium.webdriver.common.keys import Keys
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains

from selenium.webdriver import Proxy
from selenium.webdriver.common.proxy import ProxyType

driver = webdriver.Firefox(executable_path=r'geckodriver.exe')
driver.maximize_window()
time.sleep(10)
driver.get("https://kart.1881.no/?query=oslo&type=adresse")
time.sleep(4)

pages_links= driver.find_elements_by_xpath("//a")
people_link = None
for page_link in pages_links:
    if "Personer" in page_link.text:
        people_link = page_link
people_link.click()

f = open("coordinates.txt", "w")
time.sleep(3)
new_people = True
observed_people = set()
actions = ActionChains(driver)

while new_people:
    new_people = False
    people = driver.find_elements_by_class_name("result-item")
    for person in people:
        try:
            x_button = driver.find_element_by_class_name("ad-sleepy__close")
            time.sleep(2)
            x_button.click()
        except Exception as e:
            print(e)
        finally:
            try:
                if person not in observed_people:
                    new_people = True
                    observed_people.add(person)
                    name_class = person.find_element_by_class_name("result-item-name")
                    person_name = name_class.text
                    time.sleep(2)
                    driver.execute_script("arguments[0].scrollIntoView();", name_class)
                    details_link = name_class.find_element_by_tag_name("a")
                    location_class = person.find_element_by_class_name("result-item-address")
                    print(person_name,location_class.text)
                    directions_button = person.find_element_by_class_name("link-directions")
                    details_link.click()
                    time.sleep(3)
                    coordinates_link = driver.find_element_by_class_name("link-coords")
                    time.sleep(2)
                    coordinates_link.click()
                    time.sleep(2)
                    lat = driver.find_element_by_id("sidebar_coord_lat").text
                    long = driver.find_element_by_id("sidebar_coord_lon").text
                    f.write(person_name + " " + lat + " " + long + "\n")
                    time.sleep(1)
                    driver.back()
                    time.sleep(2)
            except Exception as e:
                if "not clickable" in str(e):
                    print("not clickable:")
                    if "another element <strong> obscure" in str(e) or 'class="ui-menu-item"> obscures it' in str(e):
                        actions.send_keys('X').perform()
                        time.sleep(2)
                    print(e)
                    continue
                elif '<a href="#"> could not be scrolled into view' in str(e):
                    driver.back()
                    actions.send_keys('X').perform()
                    time.sleep(2)
                    print("name could not be scrolled into view:")
                    print(e)
                    continue
                else:
                    print("Other error:")
                    print(e)
                new_people = True
                break
    actions.send_keys(Keys.DOWN).perform()