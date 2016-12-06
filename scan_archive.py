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

for page in xrange(1, config.MAX_SEARCH_PAGES):
    # Load the page
    #'http://desuarchive.org/mlp/search/text/pastebin/page/2/'
    search_page_url = '{base}/{board}/search/text/pastebin/page/{page}/'.format(
        base=config.BASE_URL, board=config.BOARD, page=page)
    print('Loading: {0!r}'.format(search_page_url))
    search_page_request = requests.get(search_page_url)
    search_page = search_page_request.content

    # Stop if we have gone past the last page

    # Find all pastebin user links
    page_user_links = re.findall('pastebin.com/u/[a-zA-Z0-9-_]+', search_page)
    all_user_links += page_user_links

    # Find all pastebin paste links
    page_paste_links = re.findall('pastebin.com/[a-zA-Z0-9]{8}', search_page)
    all_paste_links += page_paste_links


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
