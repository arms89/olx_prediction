from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from selenium.common import exceptions as e
import resources

from time import sleep


def get_data(links_file, web_driver_path='', verbose=False):
    # Opens text file with ad links
    with open(links_file, 'r') as file:
        links = set(file.readlines())

    count = 0
    driver = Chrome()
    features = resources.features
    data = []
    for url in list(links)[0:3]:
        temp = [url]
        driver.get(url)
        sleep(1)
        for feature in features:
            try:
                temp.append(driver.find_element_by_css_selector(f'[data-aut-id={feature}]').text)
            except e.NoSuchElementException:
                temp.append(None)
        data.append(dict(zip(['link']+features, temp)))
        count += 1
        if count % 100 == 0:
            # df(data).to_csv("test.csv", index=False, header=True,)
            pass
        if verbose:
            print(f'Collected {count} of {len(links)} records')
    # df(data).to_csv("test.csv", index=False, header=True)
    print(data)
    driver.quit()


get_data("links.txt")