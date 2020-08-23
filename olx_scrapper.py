"""
Author : Sai A R
Date : 22/August/2020

"""

# Import Statements
import pandas as pd
from selenium.webdriver import Chrome
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import resources

from time import sleep


# function for scrapping data from olx site
def get_links(keyword, location='', min_price='0', max_price='9223372036854776000',
             web_driver_path='/', no_of_entries=100):
    """
    This function scraps data from olx site (https://www.olx.in) and stores it as CSV file and
    returns the number of entries it scrapped.

    usage :
        get_links(keyword)
        get_links(keyword, kwargs)

    keyword: item to search (String)

    kwargs:
    =======
    location: locality to confine the search (String)

    min_price: minimum price value (String)

    max_price: maximum price value (String)

    web_driver_path = Chrome driver executable path
        path of chrome driver on your pc, by default within the project folder

    no_of_entries= 100
        number of search results to fetch, by default 100 (max 1000 due to site limit).

    """

    # reference_url = "https://www.olx.in/"
    url = f"https://www.olx.in/"
    driver = Chrome(web_driver_path,)
    driver.get(url)
    driver.maximize_window()
    sleep(2)

    # inputs the location, keyword and clicks search
    if location != '':
        driver.find_element_by_xpath(resources.location_textbox).clear()
        driver.find_element_by_xpath(resources.location_textbox).send_keys(location)
        sleep(2)
        driver.find_element_by_xpath(resources.first_location_item).click()

    driver.find_element_by_xpath(resources.keyword_textbox).send_keys(keyword)
    driver.find_element_by_xpath(resources.search_button).click()

    # After search results loads, appends url with min-max price vales and filters the results
    driver.get(f'{driver.current_url}&filter=price_between_{min_price}_to_{max_price}')
    # driver.find_element_by_xpath(resources.price_filter_button).click()
    sleep(5)

    # Check whether no_of_entries is lesser or equal to actual number of results available on site
    num_of_available_results = int(driver.find_element_by_class_name(resources.max_results_available).text.split(' ')[0])
    print(num_of_available_results)
    if num_of_available_results < no_of_entries:
        print(f"The actual number of results available on site is less than number of entries requested."
              f"Will try to load the maximum available {num_of_available_results} results, "
              f"instead of specified {no_of_entries} qty")
        no_of_entries = num_of_available_results

    items = driver.find_elements_by_class_name(resources.result_items)
    load_more_btn_dynamic_xpath = 22
    while load_more_btn_dynamic_xpath-2 < no_of_entries:
        resources.scroll_down(driver)
        sleep(2)
        print(load_more_btn_dynamic_xpath - 2)
        load_button = \
            f'//*[@id="container"]/main/div/section/div/div/div[4]/div[2]/div/div[2]/ul/li[{load_more_btn_dynamic_xpath}]/div/button'
        load_button_present = EC.presence_of_element_located((By.XPATH, load_button))
        WebDriverWait(driver, 10).until(load_button_present)
        driver.find_element_by_xpath(load_button).click()
        load_more_btn_dynamic_xpath += 20

    items = driver.find_elements_by_class_name(resources.result_items)
    print(len(items))
    with open("links.txt", "a+") as file:
        for i in items:
            file.write(i.find_elements_by_tag_name('a')[0].get_property('href'))
    driver.quit()
    return 0


def get_data(url):
    driver = Chrome(web_driver_path, )
    driver.get(url)
    driver.maximize_window()
    sleep(2)


# main program starts here
if __name__ == "__main__":
    driver_path = r"C:\Users\krish\Documents\common_project_resources\chromedriver.exe"
    get_links('car', 'chennai', min_price='50000', no_of_entries=1000, web_driver_path=driver_path)
