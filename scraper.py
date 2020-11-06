import csv
import time
import random
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from proxyscrape import get_proxyscrape_resource
from proxyscrape import create_collector, get_collector
from selenium.webdriver.firefox.options import Options
from threading import Lock
lock = Lock()

'''
We need a class to parse the results from the 1881.no website.
The report described the method of obtaining real people addresses in Oslo.
Howewer,this crawler does not tackle the problem when there is a robot detection from the website.
'''
class Crawler:

    def __init__(self):
        self.proxies = []
        self.Options = Options()
        self.get_people()
        self.get_addresses()

    '''
    Attempt to make the crawler multi threaded.Howewer,this failed.
    '''
    def create_proxies(self):
        if len(self.proxies) == 0:
            resource_name = get_proxyscrape_resource(proxytype='all', timeout=10000, ssl='yes', anonymity='elite',
                                                         country='DE')
            collector = create_collector('my-collector', resources=resource_name)
            generatedProxies = 0
            while generatedProxies <= 3:
                proxy = collector.get_proxy()
                if proxy:
                    proxyPath = proxy.host + ":" + proxy.port
                    if proxyPath not in self.proxies:
                        print("Proxy added :",proxyPath)
                        generatedProxies += 1
                        self.proxies.append(proxyPath)
    '''
    The web crawler will access the page from where we get our results.
    '''
    def access_people_page(self,keyword,driver):
        driver.get("https://kart.1881.no/?query=" + keyword + "&type=adresse")
        time.sleep(4)
        pages_links= driver.find_elements_by_xpath("//a")
        people_link = None
        for page_link in pages_links:
            if "Personer" in page_link.text:
                people_link = page_link

        people_link.click()

    '''
    Read the people that we already parsed.We try to avoid adding duplicates.
    '''
    def get_people(self):
        self.people_in_csv = []
        csv_path = "People.csv"
        delimiter = ';'
        schema = ["Surname","Latitude","Longitude"]
        try:
            people_file = csv.DictReader(open(csv_path), delimiter= delimiter)
            for row in people_file:
                self.people_in_csv.append(row['Surname'])
        except:
            with open(csv_path, 'w') as people_file:
                print("People csv did not exist.Creating it.")
                writer = csv.writer(people_file, delimiter=delimiter)
                # Gives the header name row into csv
                writer.writerow([g for g in schema])
    '''
    An attempt to parse people by addresses.
    Howewer,this did not prove useful.
    '''
    def get_addresses(self):
        self.addreses = set()
        try:
            addresses_file = open("Addresses.txt", 'r')
            for line in addresses_file.readlines():
                self.addreses.add(line.replace('\r', '').replace('\n', ''))
        except:
            print("Addresess file does not exist")

    '''
    This is messy,but seemed the easiest way to parse the results.
    '''
    def get_people_by_keyword(self,keyword="Oslo"):
        driver = webdriver.Firefox()
        print("Keyword is",keyword)
        try:
            self.access_people_page(keyword,driver)
            time.sleep(3)
            observed_people = set()
            actions = ActionChains(driver)
            timeout = 0
            with open("Addresses.txt",'a') as addresses_file:
                with open("People.csv",'a') as people_csv:
                    while timeout < 1000:
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
                                    if person_name not in self.people_in_csv:
                                        print(person_name)
                                        details_link = name_class.find_element_by_tag_name("a")
                                        location_class = person.find_element_by_class_name("result-item-address")
                                        print(person_name,location_class.text)
                                        with lock:
                                            if location_class.text and location_class.text not in self.addreses:
                                                addresses_file.write(location_class.text+'\n')
                                        details_link.click()
                                        time.sleep(3)
                                        coordinates_link = driver.find_element_by_class_name("link-coords")
                                        time.sleep(2)
                                        coordinates_link.click()
                                        time.sleep(2)
                                        lat = driver.find_element_by_id("sidebar_coord_lat").text
                                        long = driver.find_element_by_id("sidebar_coord_lon").text
                                        with lock:
                                            if lat and long:
                                                people_csv.write(person_name + ";" + lat + ";" + long + "\n")
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
                                    time.sleep(1)
                                    driver.back()
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
                        timeout += 1
                        time.sleep(1)
        except Exception as e:
            print("Exiting the thread with exception:",e)
            driver.quit()