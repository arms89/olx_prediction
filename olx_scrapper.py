"""
Author : Sai A R
Date : 22/August/2020

"""

# Import Statements
import pandas as pd
from selenium.webdriver import Chrome
from time import sleep


# function for scrapping data from olx site
def get_data(*args, web_driver_path='/', no_of_entries=500, verbose= True):
    """
    This function scraps data from olx site (https://www.olx.in) and stores it as CSV file and
    returns the number of entries it scrapped.

    usage :
        get_data(*args, verbose= True, no_of_entries=500, web_driver_path='/')

    *args= [keyword, location, min_price, max_price]
        keyword: item to search (String)
        location: locality to confine the search (String)
        min_price: minimum price value (String)
        max_price: maximum price value (String)

    web_driver_path = Chrome driver executable path
        path of chrome driver on your pc, by default within the project folder

    no_of_entries= 500
        number of search results to fetch, by default 500.

    verbose= boolean (True (or) False)
        prints verbose

    """

    keyword, location, min_price, max_price = args[0]
    # reference_url = "https://www.olx.in/"
    url = f"https://www.olx.in/"
    driver = Chrome(web_driver_path,)
    driver.get(url)
    driver.maximize_window()

    # inputs the location, keyword, min-max price vales and clicks search
    if location != '':
        driver.find_element_by_xpath(
            '//*[@id="container"]/header/div/div/div[2]/div/div/div[1]/div/div/input').clear()
        driver.find_element_by_xpath(
            '//*[@id="container"]/header/div/div/div[2]/div/div/div[1]/div/div/input').send_keys(location)

        sleep(2)
        driver.find_element_by_xpath(
            '//*[@id="container"]/header/div/div/div[2]/div/div/div[1]/div/div[2]/div/div/div[1]').click()
    if min_price != '':
        pass
    if max_price != '':
        pass
    driver.find_element_by_xpath(
        '//*[@id="container"]/header/div/div/div[2]/div/div/div[2]/div/form/fieldset/div/input').send_keys(keyword)

    driver.find_element_by_xpath('//*[@id="container"]/header/div/div/div[2]/div/div/div[3]').click()
    sleep(5)
    driver.quit()
    return 0


# main program starts here
if __name__ == "__main__":
    driver_path = r"C:\Users\krish\Documents\common_project_resources\chromedriver.exe"
    options = ['cars', 'chennai', '', '']
    get_data(options, web_driver_path=driver_path)
