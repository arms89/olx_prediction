"""
Author : Sai A R
Date : 22/August/2020

"""

# Import Statements
import pandas as pd
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
import selenium.common.exceptions as e
from time import sleep
from datetime import datetime
from pandas import DataFrame as df

# DOM Resources file
import resources


# function for scrapping ad links from olx site
def get_links(keyword, location='', min_price='0', max_price='9223372036854776000',
              no_of_entries=100, verbose=False):
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

    no_of_entries= 100
        number of search results to fetch, by default 100 (max 1000 due to site limit).
    verbose = boolean
        displays progress at every 20 ad links fetched
    """

    url = f"https://www.olx.in/"
    try:
        driver = Chrome()
    except WebDriverException:
        print("WebDriver executable is not found in project folder. \n"
              "Please enter the correct WebDriver path and re-run the code. \n"
              "Program is now exiting...")
        return -1
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
    sleep(5)

    entries_loaded = 20
    while entries_loaded <= no_of_entries:
        resources.scroll_down(driver)
        print(f'Loaded {entries_loaded} results')
        try:
            driver.find_element_by_class_name(resources.load_more_button).click()
            sleep(1)
        except e.NoSuchElementException:
            print('"Load More" button not found')
            break
        except e.ElementClickInterceptedException:
            sleep(2)
            entries_loaded -= 20

        entries_loaded += 20

    items = driver.find_elements_by_class_name(resources.result_items)
    print(f'total links = {len(items)}')
    # with open(f'{datetime.now().strftime("%H_%M")}_{location}_links.txt', "w+") as file:
    with open('links.txt', "a+") as file:
        for i in items:
            file.write(i.find_elements_by_tag_name('a')[0].get_property('href'))
            file.write("\n")
    sleep(1)
    driver.quit()
    return 0


# function for scrapping data from the links collected previously by "get_links()" function
def get_data(links_file, verbose=False):

    # Opens text file with ad links
    with open(links_file, 'r') as file:
        links = list(set(file.readlines()))

    count = 0
    chrome_options = Options()
    chrome_options.add_experimental_option("prefs", {'profile.managed_default_content_settings.javascript': 2})
    driver = Chrome()
    features = resources.features
    data = []
    for url in links:
        temp = [url]
        driver.get(url)
        sleep(1)
        for feature in features:
            try:
                temp.append(driver.find_element_by_css_selector(f'[data-aut-id={feature}]').text)
            except e.NoSuchElementException:
                temp.append(-1)
        data.append(dict(zip(['link']+features, temp)))
        count += 1
        if count % 100 == 0:
            df(data).to_csv("olx.csv", index=False, header=True,)
        if verbose:
            print(f'Collected {count} of {len(links)} records')
    df(data).to_csv("olx.csv", index=False, header=True)
    driver.quit()


# main program starts here
if __name__ == "__main__":
    with open('links.txt', "w+") as file:
        file.write('')
    driver_path = r"C:\Users\krish\Documents\common_project_resources\chromedriver.exe"
    locations = ['chennai', 'trichy', 'coimbatore', 'madurai']
    for location in locations:
        get_links('car', location=location, min_price='50000', no_of_entries=999)
    get_data('links.txt', verbose=True)
