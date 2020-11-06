from scraper import Crawler

'''
Will write to the People.csv file 
the names,latitudes and longitudes of the people that can be parsed.
'''
crawler = Crawler()
crawler.get_people_by_keyword()