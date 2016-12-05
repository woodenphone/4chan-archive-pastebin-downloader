#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      User
#
# Created:     02-12-2016
# Copyright:   (c) User 2016
# Licence:     <your licence>
#-------------------------------------------------------------------------------
# Stdlib
import logging
import os
import re
# Libraries
import requests
# Local
import config

# Config vars
BASE_URL = 'http://desuarchive.org'# ex. 'http://desuarchive.org'
BOARD = 'mlp'# ex. 'mlp'
MAX_SEARCH_PAGES = 10

FOUND_USERS_FILEPATH = 'found_users.txt'
FOUND_PASTES_FILEPATH = 'found_pastes.txt'




# To find pastebins for a board:
all_user_links = []
all_paste_links = []

for page in xrange(1, MAX_SEARCH_PAGES):
    # Load the page
    #'http://desuarchive.org/mlp/search/text/pastebin/page/2/'
    search_page_url = '{base}/{board}/search/text/pastebin/page/{page}/'.format(
        base=BASE_URL, board=BOARD, page=page)
    logging.debug('Loading: {0!r}'.format(search_page_url))
    search_page_request = requests.get(search_page_url)
    search_page = search_page_request.content

    # Stop if we have gone past the last page

    # Find all pastebin user links
    page_user_links = re.findall('http://pastebin.com/u/[a-zA-Z0-9-_]+', search_page)
    all_user_links += page_user_links

    # Find all pastebin paste links
    page_paste_links = re.findall('http://pastebin.com/[a-zA-Z0-9]{8}', search_page)
    all_paste_links += page_paste_links



with open(FOUND_USERS_FILEPATH, "wb") as uf:
    for user_link in all_user_links:
        uf.write('{0}\n'.format(user_link))

with open(FOUND_PASTES_FILEPATH, "wb") as pf:
    for paste_link in all_paste_links:
        pf.write('{0}\n'.format(paste_link))



def main():
    pass

if __name__ == '__main__':
    main()
