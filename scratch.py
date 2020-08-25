from selenium.webdriver import Chrome
from selenium.common.exceptions import NoSuchElementException
from time import sleep


def get_data(links_file):
    driver_path = r'C:\Users\krish\Documents\common_project_resources\chromedriver.exe'
    driver = Chrome(driver_path,)

    with open(links_file, 'r') as file:
        links = file.readlines()

    print(links)
    for link in links[0:3]:
        url = link
        print('\n', link)
        driver.get(url)
        sleep(3)

        features = ['value_make', 'value_model', 'value_variant',
                    'value_year', 'value_petrol', 'value_transmission',
                    'value_mileage', 'value_first_owner', 'itemPrice',
                    'itemTitle', 'itemLocation', 'itemDescriptionContent']

        for feature in features:
            try:
                print(feature, driver.find_element_by_css_selector(f'[data-aut-id={feature}]').text, sep=' - ')
            except NoSuchElementException:
                print(feature, ' - not available')
    driver.quit()


# Main Program starts here
if __name__ == '__main__':
    get_data('22_06_chennai_links.txt')
