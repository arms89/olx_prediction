"""
Author : Sai A R
Date : 22/August/2020

"""

# Import Statements
from selenium.webdriver import Chrome
import selenium.common.exceptions as e
from time import sleep
from pandas import DataFrame as df

# DOM Resources file
import resources


""" 
CAUTION: OLX blocks the ip for one day (approximately 24 hours) after running the scrapper
may be they think this as some kind of DOS attack, I don't know exactly.

You have to wait for one day before you can run scrapper another time. Or you can use some proxy. 
"""


# function for scrapping ad links from olx site
def get_links(keyword, location='', min_price='0', max_price='9223372036854776000',
              no_of_entries=100, verbose=False):
    """
    This function scraps ad results links from olx site (https://www.olx.in) and
    stores it as text file with all ad urls

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

    url = "https://www.olx.in/"
    try:
        driver = Chrome()
    except e.WebDriverException:
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
    # scrolls down until the number od loaded results are less than the required number of results
    while entries_loaded <= no_of_entries:
        resources.scroll_down(driver)
        print(f'Loaded {entries_loaded} results')
        try:
            driver.find_element_by_class_name(resources.load_more_button).click()
            sleep(1)
        # in olx site there is an upper limit of 1000 results per session, after which "Load More" button doesnt show up
        # so stopping the scroll down once the button is not found.
        except e.NoSuchElementException:
            print('"Load More" button not found')
            break
        # Some times the click gets executed before the page scrolls down and displays the "load more" button.
        # to prevent that issue this exception is used.
        except e.ElementClickInterceptedException:
            sleep(2)
            entries_loaded -= 20

        entries_loaded += 20

    items = driver.find_elements_by_class_name(resources.result_items)
    print(f'total links = {len(items)}')

    # write the links of ads loaded in the results to a file.
    with open('links.txt', "a+") as file:
        for i in items:
            file.write(i.find_elements_by_tag_name('a')[0].get_property('href'))
            file.write("\n")
    sleep(1)
    driver.quit()


# function for scrapping data from the links collected previously by "get_links()" function
def get_data(links_file, verbose=False):
    """
        This function scraps data from olx site (https://www.olx.in) and stores it as CSV file

        usage :
            get_links(links_file)
            get_links(links_file, kwargs)

        links_file: path / name of the text file that contains olx ad urls (String)

        kwargs:
        =======
        verbose = boolean
            displays progress at every 1 ad links fetched
        """

    # Opens text file with ad links
    with open(links_file, 'r') as file:
        links = list(set(file.readlines()))

    count = 0   # Counter for displaying the verbose and tracking progress
    # initializing new chrome driver, because found some memory usage issues on reusing previous driver.
    # or when using a common driver for both functions
    driver = Chrome()
    features = resources.features   # getting feature attributes from resources file

    # Stores collected features and its values in dict format inside this data list. (for ex.)
    # data = [{'make': "abc", 'year': '2002',...},
    #         {'make': "xyz", 'year': '2010',...},
    #         {'make': "pqr", 'year': '2009',...}, ...]
    data = []

    # iterates through each url stores the scrapped {feature : value} pair into a list
    for url in links:
        temp = [url]    # temporary variable to store values
        driver.get(url)
        sleep(1)
        for feature in features:
            try:
                temp.append(driver.find_element_by_css_selector(f'[data-aut-id={feature}]').text)
            except e.NoSuchElementException:
                temp.append(None)

        data.append(dict(zip(['link']+features, temp)))     # appending key(features) and its values to list
        count += 1

        if count % 100 == 0:    # quiting and restarting driver every 100 links to prevent memory usage issues
            # df(data).to_csv("olx.csv", index=False, header=True,)
            driver.quit()
            sleep(1)
            driver = Chrome()

        if verbose:
            print(f'Collected {count} of {len(links)} records')

    # Stores the data to csv file
    df(data).to_csv("olx.csv", index=False, header=True)
    driver.quit()


# main program starts here
if __name__ == "__main__":
    # Clear the links file before starting to store new entries
    with open('links.txt', "w+") as file:
        file.write('')

    locations = ['chennai', 'trichy', 'coimbatore', 'madurai']

    # Iterate through each location and get ads links posted in that location
    for location in locations:
        get_links('car', location=location, min_price='50000', no_of_entries=200)

    # runs get_data function which fetches the data of the ads from each ad link and
    # finally stores it to a csv file.
    get_data('links.txt', verbose=True)
