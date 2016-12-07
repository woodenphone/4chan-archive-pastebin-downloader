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
import datetime
# Libraries
import requests
# Local
import config_archive_scan as config



def uniquify(seq, idfun=None):
    # List uniquifier from
    # http://www.peterbe.com/plog/uniqifiers-benchmark
   # order preserving
   if idfun is None:
       def idfun(x): return x
   seen = {}
   result = []
   for item in seq:
       marker = idfun(item)
       # in old Python versions:
       # if seen.has_key(marker)
       # but in new ones:
       if marker in seen: continue
       seen[marker] = 1
       result.append(item)
   return result




# To find pastebins for a board:
all_user_links = []
all_paste_links = []

# To scan through the archive one week at a time:
print('Scanning from {0} to {1}'.format(config.START_DATE, config.END_DATE))

# Setup conditions for first cycle
low_date = config.START_DATE
high_date = low_date + config.STEP_LENGTH

while low_date < config.END_DATE:
    # Grab for the current range
    print('low_date: {0!r}, high_date: {1!r}.'.format(low_date, high_date))
    low_date_str = low_date.strftime('%Y-%m-%d')
    high_date_str = high_date.strftime('%Y-%m-%d')

    previous_page_post_ids = []
    for page_num in xrange(1, config.MAX_SEARCH_PAGES):
        # Load the page
        #'http://desuarchive.org/mlp/search/text/pastebin/page/2/'
        search_page_url = '{base}/{board}/search/text/pastebin/start/{low}/end/{high}/page/{page_num}/'.format(
            base=config.BASE_URL, board=config.BOARD, low=low_date_str, high=high_date_str, page_num=page_num)
        print('Loading: {0!r}'.format(search_page_url))
        search_page_request = requests.get(search_page_url)
        search_page = search_page_request.content

        # Find all pastebin user links
        page_user_links = re.findall('pastebin.com/u/[a-zA-Z0-9-_]+', search_page)
        all_user_links += page_user_links

        # Find all pastebin paste links
        page_paste_links = re.findall('pastebin.com/[a-zA-Z0-9]{8}', search_page)
        all_paste_links += page_paste_links

        print('Found {0} results this page'.format(len(page_user_links) + len(page_paste_links)))

        # Stop if we have gone past the last page
        # Test postIDs
        current_page_post_ids = re.findall('data-post="(\d+)"', search_page)
        print('Found {0} postIDs this page.'.format(len(current_page_post_ids)))
        if current_page_post_ids == previous_page_post_ids:
            print('The results on this page are the same as last page, moving on.')
            break
        previous_page_post_ids = current_page_post_ids
        # Test for error message
        if ('<h4 class="alert-heading">Error!</h4>' in search_page) and ('No results found.' in search_page):
            print('Detected end of results error message, moving on.')
            break

        continue

    # Advance date by one step
    low_date = high_date
    high_date += config.STEP_LENGTH
    continue


print('Finished searching for links.')


# Remove duplicates
all_paste_links = uniquify(all_paste_links)
all_user_links = uniquify(all_user_links)


# Save what we found.
with open(config.FOUND_USERS_FILEPATH, "wb") as uf:
    for user_link in all_user_links:
        uf.write('{0}\n'.format(user_link))

with open(config.FOUND_PASTES_FILEPATH, "wb") as pf:
    for paste_link in all_paste_links:
        pf.write('{0}\n'.format(paste_link))


print('Done.')



def main():
    pass

if __name__ == '__main__':
    main()
