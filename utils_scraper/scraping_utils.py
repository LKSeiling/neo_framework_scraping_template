import requests
import json
import sys
from os.path import abspath, exists
from os import getcwd
from decouple import config
from argparse import ArgumentParser 

def env_exists():
    path = "".join([abspath(getcwd()),"/.env"])
    return exists(path)

def check_baseurl(baseurl:str):
    if baseurl[-1] != "/":
        return "".join([baseurl, "/"])
    else:
        return baseurl

def get_params():

    parser = ArgumentParser(description='Get parameters from arguments.')
    parser.add_argument('--url', metavar='BASE URL', type=str,
                    help='(str) base url of your instance of the NEO framework')
    parser.add_argument('--apikey', metavar='API_KEY', type=str,
                    help='(str) API key shown on your profile, only works while logged-in')
    parser.add_argument('--platform', metavar='PLATFORM', type=str,
                    help="(str) either 'facebook' [or 'twitter' or 'instagram']")
    parser.add_argument('--sid', metavar='SETTING_ID', type=int,
                    help='(int) ID of newsfeed settings that should receive data')

    args = parser.parse_args()

    if len(sys.argv) == 9:
        BASE_URL, API_KEY, PLATFORM, SETTING_ID = check_baseurl(args.url), args.apikey, args.platform, int(args.sid)
    elif env_exists():
        BASE_URL, API_KEY, PLATFORM, SETTING_ID = check_baseurl(config('BASE_URL')), config('API_KEY'), config('PLATFORM'), int(config('SETTING_ID'))
    else:
        sys.exit("Please provide the parameters for the variables BASE_URL, API_KEY, PLATFORM, and SETTING_ID in an .env-file or as arguments to the function. See '-h' for more information.")

    if "" in [BASE_URL, API_KEY, PLATFORM] or SETTING_ID <= 0:
        sys.exit("Please make sure to specify all neccessary parameters (BASE_URL, API_KEY, PLATFORM), and set SETTING_ID to a value greater than 0.")
        
    else:
        return BASE_URL, API_KEY, PLATFORM, SETTING_ID


def check_platform(platform):
    accepted = ["facebook"] #, "twitter", "instagram"]
    if platform in accepted:
        pass
    else:
        raise ValueError(f'The platform you provided is not supported. Supported platforms: {accepted}')

def post_to_NEOF(data, platform, data_type, API_KEY, NB_ID, BASE_URL):
    url = "".join([BASE_URL, "newsfeed-setting/", NB_ID, "/", data_type, "?auth_key=", API_KEY])
    r = requests.post(url, json=json.dump(data))
    print(f"Status Code: {r.status_code}, Response: {r.json()}")

def post_to_fb_settings(post_list, author_list, API_KEY, NB_ID, BASE_URL):
    post_to_NEOF(post_list, "fb", "post", API_KEY, NB_ID, BASE_URL)
    post_to_NEOF(author_list, "fb", "author", API_KEY, NB_ID, BASE_URL)
    
def post_to_twitter_settings(post_list, author_list, API_KEY, NB_ID, BASE_URL):
    post_to_NEOF(post_list, "twitter", "post", API_KEY, NB_ID, BASE_URL)
    post_to_NEOF(author_list, "twitter", "author", API_KEY, NB_ID, BASE_URL)

def post_to_settings(post_list, author_list, API_KEY, PLATFORM, NB_ID, BASE_URL):
    check_platform(PLATFORM)
    if PLATFORM == "facebook":
        post_to_fb_settings(post_list, author_list, API_KEY, NB_ID, BASE_URL)
    elif PLATFORM == "twitter":
        post_to_twitter_settings(post_list, author_list, API_KEY, NB_ID, BASE_URL)
