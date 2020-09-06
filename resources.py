# Import statements
from time import sleep

# Webscrapper page elements

# xpaths :
location_textbox = '//*[@id="container"]/header/div/div/div[2]/div/div/div[1]/div/div/input'
keyword_textbox = '//*[@id="container"]/header/div/div/div[2]/div/div/div[2]/div/form/fieldset/div/input'
first_location_item = '//*[@id="container"]/header/div/div/div[2]/div/div/div[1]/div/div[2]/div/div/div[1]'
search_button = '//*[@id="container"]/header/div/div/div[2]/div/div/div[3]'
min_price_textbox = '//*[@id="container"]/main/div/section/div/div/div[4]/div[1]/div/div[4]/div/div[2]/div/input[1]'
max_price_textbox = '//*[@id="container"]/main/div/section/div/div/div[4]/div[1]/div/div[4]/div/div[2]/div/input[2]'
price_filter_button = '//*[@id="container"]/main/div/section/div/div/div[4]/div[1]/div/div[4]/div/div[2]/div/a'

# class names :
max_results_available = '_3RsTo'
result_items = 'EIR5N'
load_more_button = 'JbJAl'

# Css Selector attribute names of fields present in individual ad page:
features = ['value_make', 'value_model', 'value_variant',
            'value_year', 'value_petrol', 'value_transmission',
            'value_mileage', 'value_first_owner', 'itemPrice', 'itemTitle', 'itemLocation', 'itemDescriptionContent']

# Scrolling page
# Source: Stackoverflow
# Link: https://stackoverflow.com/questions/48850974/selenium-scroll-to-end-of-page-in-dynamically-loading-webpage
# Answered by Ratmir Asanov "https://stackoverflow.com/users/7901720/ratmir-asanov"


def scroll_down(driver):
    """A method for scrolling the page."""
    # Get scroll height.
    last_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        # Scroll down to the bottom.
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        # Wait to load the page.
        sleep(2)
        # Calculate new scroll height and compare with last scroll height.
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height
