import csv
import time

from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys

people_in_csv = []
people_file = csv.DictReader(open("People.csv"),delimiter = ';')
for row in people_file:
    people_in_csv.append(row['Surname'])

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

time.sleep(3)
new_people = True
observed_people = set()
actions = ActionChains(driver)
added_people = 0
with open("People.csv",'a') as people_csv:
    while added_people < 1000 :
        new_people = False
        people = driver.find_elements_by_class_name("result-item")
        for person in people:
            try:
                if person not in observed_people:
                    observed_people.add(person)
                    time.sleep(2)
                    name_class = person.find_element_by_class_name("result-item-name")
                    person_name = name_class.text
                    time.sleep(1)
                    driver.execute_script("arguments[0].scrollIntoView();", name_class)
                    time.sleep(1)
                    if person_name not in people_in_csv:
                        print(person_name)
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
                        observed_people.add(person)
                        people_csv.write(person_name + ";" + lat + ";" + long + "\n")
                        added_people += 1
                        time.sleep(2)
                        driver.back()
                        time.sleep(1)
            except Exception as e:
                if "not clickable" in str(e):
                    print("not clickable:")
                    if "another element <strong> obscure" in str(e) or 'class="ui-menu-item"> obscures it' in str(e):
                        print("We have an obscure error: ")
                        actions.send_keys('X').perform()
                        time.sleep(2)
                    print(e)
                elif '<a href="#"> could not be scrolled into view' in str(e):
                    time.sleep(2)
                    actions.send_keys('X')
                    time.sleep(2)
                    name_class = person.find_element_by_class_name("result-item-name")
                    time.sleep(1)
                    print("name could not be scrolled into view:")
                    print(e)
                else:
                    print("Other error:")
                    print(e)
                x_button = driver.find_element_by_class_name("ad-sleepy__close")
                if x_button.is_displayed() and x_button.is_enabled():
                    x_button.click()
                    time.sleep(2)
        actions.send_keys(Keys.DOWN).perform()
        time.sleep(1)