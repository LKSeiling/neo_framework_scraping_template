# SCRAPING TEMPLATE
# to automatically add existing posts to newswfeed settings

## import all helper functions
from utils_scraper import post_to_settings, get_params

## set relevant parameters
### to be set either in the .env file or as arguments to scraping_template.py
BASE_URL, API_KEY, PLATFORM, SETTING_ID = get_params() 

## run your own scraping script, saving the output in a list of dictionaries
# post_list = your_post_scraping_script(your_arguments)
# author_list = your_author_scraping_script(your_arguments)


## send the scraping results to the framwork
post_to_settings(post_list, author_list, API_KEY, PLATFORM, SETTING_ID, BASE_URL)