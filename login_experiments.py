#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      User
#
# Created:     09-12-2016
# Copyright:   (c) User 2016
# Licence:     <your licence>
#-------------------------------------------------------------------------------
# Stdlib
import logging
import os
import re
import time
# Libraries
import requests
# Local
import config_pastebin as config







def fetch(url):
    for try_num in range(10):
        logging.debug('Fetch %s' % (url))
        if try_num > 1:
            time.sleep(30)# Back off a bit if something goes wrong
        try:
            response = requests.get(url, timeout=300)
        except requests.exceptions.Timeout, err:
            logging.exception(err)
            logging.error('Caught requests.exceptions.Timeout')
            continue
        except requests.exceptions.ConnectionError, err:
            logging.exception(err)
            logging.error('Caught requests.exceptions.ConnectionError')
            continue
        except requests.exceptions.ChunkedEncodingError, err:
            logging.exception(err)
            logging.error('Caught requests.exceptions.ChunkedEncodingError')
            continue
        else:
            time.sleep(1)
            return response

    raise Exception('Giving up!')



# This didn't seem to work
### Log in using API calls
##login_url = 'http://pastebin.com/api/api_login.php'#?api_dev_key={api_dev_key}&api_user_name={api_user_name}&api_user_password={api_user_password}'.format(
##    #api_dev_key=config.PASTEBIN_DEVELOPER_API_KEY, api_user_name=config.API_USER_NAME, api_user_password=config.API_USER_PASSWORD)
##
##login_response = requests.post(login_url,
##    data = {
##    'api_dev_key':config.PASTEBIN_DEVELOPER_API_KEY,
##    'api_user_name':config.API_USER_NAME,
##    'api_user_password':config.API_USER_PASSWORD
##    }
##)
##if len(login_response.content) == 32:
##    api_user_key = login_response.content
##else:
##    print('Could not get api_user_key')
##
##test_page_response = requests.get('http://pastebin.com/api_scrape_item_meta.php?i=PASTEID&api_user_key={0}'.format(api_user_key))
##print(test_page_response.content)








session=requests.session()
print('session.headers: {0!r}'.format(session.headers))
session.headers['user-agent'] = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'
# Log in using web form
# Get token
pre_login_response = session.get(url='http://pastebin.com/login')
with open(os.path.join('debug', 'login_experiments.pre_login.htm'), "wb") as pre_f:
    pre_f.write(pre_login_response.content)
csrf_token_login_search = re.search('input type="hidden"\sname="csrf_token_login"\svalue="(\w+)"', pre_login_response.content)
csrf_token_login = csrf_token_login_search.group(1)
print('csrf_token_login: {0!r}'.format(csrf_token_login))

# Log in
login_response = session.get(
    url = 'http://pastebin.com/login.php',
    data = {
    'csrf_token_login':csrf_token_login,
    'submit_hidden':'submit_hidden',
    'user_name':config.API_USER_NAME,
    'user_password':config.API_USER_PASSWORD,
    'submit':'Login'
    },
    headers={'Referer':'http://pastebin.com/login'}
)

with open(os.path.join('debug', 'login_experiments.login.htm'), "wb") as login_f:
    login_f.write(login_response.content)

# Check if login worked
post_login_response = session.get(url='http://pastebin.com/')
with open(os.path.join('debug', 'login_experiments.post_login.htm'), "wb") as post_f:
    post_f.write(post_login_response.content)



def main():
    pass

if __name__ == '__main__':
    main()
