'''
Yelp Scraper
To use run 'python yelp-scraper.py keyword'
Where you replace keyword by your business of interest
The script will open Firefox and for each city in 'cities.txt' scrape business links first
Then it will scrape all individual business pages for information
(title, website, category, phone, address, description)
And save it to a folder named 'output' in JSON format using a separate file for each city
'''

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import os
import json
import argparse


LINKS = []
BUSINESS_DATA = {}
COUNT = 0
XPATH_TITLE = "/html/body/div[2]/div[3]/div/div[1]/div[3]/div/div/div[2]/div[1]/div[1]/div/div/h1"
XPATH_TITLE_2 = "/html/body/div[2]/div[3]/div/div[1]/div[2]/div/div/div[2]/div[1]/div[1]/div/div/h1"
XPATH_CATEGORY = "/html/body/div[2]/div[3]/div/div[1]/div[3]/div/div/div[2]/div[1]/div[1]/div/span/span/a"
XPATH_CATEGORY_2 = "/html/body/div[2]/div[3]/div/div[1]/div[2]/div/div/div[2]/div[1]/div[1]/div/span/span/a"
XPATH_WEBSITE = "/html/body/div[2]/div[3]/div/div[1]/div[3]/div/div/div[2]/div[2]/div/div/section/div/div[1]/div/div[2]/a"
XPATH_WEBSITE_2 = "/html/body/div[2]/div[3]/div/div[1]/div[2]/div/div/div[2]/div[2]/div/div/section/div/div[1]/div/div[2]/a"
XPATH_PHONE = "/html/body/div[2]/div[3]/div/div[1]/div[2]/div/div/div[2]/div[2]/div/div/section/div/div[1]/div/div[2]/p[2]"
XPATH_PHONE_2 = "/html/body/div[2]/div[3]/div/div[1]/div[3]/div/div/div[2]/div[2]/div/div/section/div/div[2]/div/div[2]/p[2]"
XPATH_PHONE_3 = "/html/body/div[2]/div[3]/div/div[1]/div[2]/div/div/div[2]/div[2]/div/div/section/div/div[2]/div/div[2]/p[2]"
XPATH_PHONE_4 = "/html/body/div[2]/div[3]/div/div[1]/div[3]/div/div/div[2]/div[2]/div/div/section/div/div[1]/div/div[2]/p[2]"
XPATH_RATING = "/html/body/div[2]/div[3]/div/div[1]/div[3]/div/div/div[2]/div[1]/div[1]/div/div[2]/div[1]/span/div"
XPATH_RATING_2 = "/html/body/div[2]/div[3]/div/div[1]/div[2]/div/div/div[2]/div[1]/div[1]/div/div[2]/div[1]/span/div"
XPATH_DESCRIPTION = "/html/body/div[2]/div[3]/div/div[1]/div[3]/div/div/div[2]/div[1]/section[4]/div[2]/div[2]/p"
XPATH_ADDRESS =   "/html/body/div[2]/div[3]/div/div[1]/div[3]/div/div/div[2]/div[1]/section[1]/div[2]/div[1]/div/div/div/div[1]/address/p/span"
XPATH_ADDRESS_2 = "/html/body/div[2]/div[3]/div/div[1]/div[2]/div/div/div[2]/div[1]/section[2]/div[2]/div[1]/div/div/div/div[1]/address/p/span"
XPATH_ADDRESS_3 = "/html/body/div[2]/div[3]/div/div[1]/div[2]/div/div/div[2]/div[1]/section[3]/div[2]/div[1]/div/div/div/div[1]/address/p/span"
XPATH_ADDRESS_4 = "/html/body/div[2]/div[3]/div/div[1]/div[3]/div/div/div[2]/div[1]/section[2]/div[2]/div[1]/div/div/div/div[1]/address/p/span"
XPATH_ADDRESS_5 = "//address/p/span"

def try_driver_get(driver, url):
	try: driver.get(url)
	except TimeoutException: try_driver_get(driver, url)


#Scrapes all business links from search page recursively and saves to LINKS
def scrape_search_page(driver, keyword, city, start = 0):
    global LINKS
    global START
    search_link=f'https://www.yelp.com/search?find_desc={keyword}&find_loc={city}&start={start}'

    try_driver_get(driver, search_link)

    try:
        #This will fail if there is no links that interest us, so we stop and return
        raw_links = driver.find_elements(By.XPATH, "//a[contains(@href,'/biz/')]")
        if not raw_links: raise ValueError
        
        for link in {link.get_attribute("href") for link in raw_links}:
            LINKS.append(link.split("hrid=")[0].split("osq=")[0].replace("?", ""))
            print(link.split("hrid=")[0].split("osq=")[0])

        start += 10
        scrape_search_page(driver, keyword, city, start)
        
    except ValueError: return


def scrape_business_page(driver, link):
    '''Scrape data from business page based on XPATH
        Add to memory in BUSINESS_DATA in dictionary format if title found'''
    global BUSINESS_DATA
    global COUNT
    
    try_driver_get(driver, link)

    try: raw_title = driver.find_element(By.XPATH, XPATH_TITLE)
    except:
        try: raw_title = driver.find_element(By.XPATH, XPATH_TITLE_2)
        except: raw_title = 0
    try: raw_category = driver.find_element(By.XPATH, XPATH_CATEGORY)
    except: 
    	try: raw_category = driver.find_element(By.XPATH, XPATH_CATEGORY_2)
    	except: raw_category = 0
    try: raw_website = driver.find_element(By.XPATH, XPATH_WEBSITE)
    except: 
    	try: raw_website = driver.find_element(By.XPATH, XPATH_WEBSITE_2)
    	except: raw_website = 0
    try: raw_phone = driver.find_element(By.XPATH, XPATH_PHONE)
    except:
        try: raw_phone = driver.find_element(By.XPATH, XPATH_PHONE_2)
        except:
	        try: raw_phone = driver.find_element(By.XPATH, XPATH_PHONE_3)
	        except: raw_phone = 0
    try: raw_rating = driver.find_element(By.XPATH, XPATH_RATING).get_attribute("aria-label")
    except: 
        try: raw_rating = driver.find_element(By.XPATH, XPATH_RATING_2).get_attribute("aria-label")
        except: raw_rating = 0
    try: raw_description = driver.find_element(By.XPATH, XPATH_DESCRIPTION)
    except: raw_description = 0
    try: raw_address = driver.find_elements(By.XPATH, XPATH_ADDRESS)
    except:
        try: raw_address = driver.find_elements(By.XPATH, XPATH_ADDRESS_2)
        except:
	        try: raw_address = driver.find_elements(By.XPATH, XPATH_ADDRESS_3)
	        except: 
	        	try: raw_address = driver.find_elements(By.XPATH, XPATH_ADDRESS_4)
	        	except: 
		        	try: raw_address = driver.find_elements(By.XPATH, XPATH_ADDRESS_5)
		        	except: raw_address = 0
    
    title = raw_title.text if raw_title else None
    category = raw_category.text if raw_category else None
    website = raw_website.text if raw_website else None
    phone = raw_phone.text if raw_phone else None
    rating = raw_rating.split("star")[0].strip() if raw_rating else None
    description = raw_description.text if raw_description else None
    address = " ".join([address.text for address in raw_address]) if raw_address else None

    print(f'\ntitle: {title}\ncategory: {category}\nwebsite: {website}\n\
phone: {phone}\nrating: {rating}\ndescription: {description}\naddress: {address}')

    business = {
        "title": title,
        "address": address,
        "website": website,
        "phone": phone,
        "rating": rating,
        "category": category
    }

    if business["title"] != None:
        BUSINESS_DATA[f'{COUNT}'] = business
        COUNT += 1


def get_cities():
    with open("cities.txt", "r") as f: return [city.strip() for city in f.read().split(",")]


def write_data_to_file(filename = "data"):
    #Create output folder if it doesn't exist
    if not (os.path.isdir("output")): os.mkdir("output")
    if BUSINESS_DATA:
        with open(f'output/{filename}.json', 'w') as file:
            json.dump(BUSINESS_DATA, file)


def main(keyword):
    driver = webdriver.Firefox(executable_path='geckodriver.exe')
    CITIES = get_cities()

    #Loop through all the cities saved in text file to search for business links
    for city in CITIES:
        scrape_search_page(driver, keyword, city)

        #Loop through the business links found earlier and extract business data
        for link in LINKS:
            scrape_business_page(driver, link)

        write_data_to_file(f'{keyword}-{city}')
        
    driver.close()
    print("Success!")


if __name__=="__main__":
    argparser = argparse.ArgumentParser()
    argparser.add_argument('keyword', help = 'Search Keyword')
    args = argparser.parse_args()
    keyword = args.keyword

    main(keyword)