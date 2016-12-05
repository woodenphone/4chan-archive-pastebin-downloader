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





def download_paste(paste_id, output_dir):
    """Save a single paste"""
    assert(len(paste_id) == 8)
    # Prebuild filepaths
    item_filepath = os.path.join(output_dir, '{0}.txt'.format(paste_id))
    metadata_filepath = os.path.join(output_dir, '{0}.json'.format(paste_id))

    # Skip if already saved
    if os.path.exists(item_filepath) and os.path.exists(metadata_filepath):
        return False

    # Get paste metadata
    metadata_url = 'http://pastebin.com/api_scrape_item_meta.php?i={0}'.format(paste_id)
    metadata_response = requests.get(metadata_url)

    # Get paste raw data
    item_url = 'http://pastebin.com/api_scrape_item.php?i={0}'.format(paste_id)
    item_response = requests.get(item_url)

    # Save both metadata and raw data
    with open(metadata_filepath, "wb") as mf:
        mf.write(metadata_response.content)

    with open(item_filepath, "wb") as mf:
        mf.write(item_response.content)

    logging.debug('Saved pasteID {0!r}'.format(paste_id))
    return True


def download_pastes(paste_ids, output_dir):
    logging.debug('Downloading paste_ids: {0!r}'.format(paste_ids))
    for paste_id in paste_ids:
        download_paste(paste_id=paste_id, output_dir=output_dir)
    return


def download_user_pastes(user, output_dir):
    # To save everything by a user:
    logging.debug('Saving pastes for user: {0!r}'.format(user))
    # Parse the listing for that user
    user_pastes = []
    for p in xrange(1,100):
        # Load the page
        user_page_url = 'http://pastebin.com/u/{0}/{1}'.format(user, p)
        logging.debug('Loading: {0!r}'.format(user_page_url))
        user_page_request = requests.get(user_page_url)
        page = user_page_request.content
        # Parse that page
        # Stop if this is the last page
        if '<table class="maintable">' not in page:
            break
        # Remove the top and bottom of the page
        page_without_top = page.split('<table class="maintable">')[1]
        page_pastes_section = page_without_top.split('</tbody></table>')[0]
        # Get the links to the user's pastes
        page_results = re.findall('<a\shref="/(\w{8})">', page_pastes_section)
        user_pastes += page_results
        continue

    # Save the found pastes
    if len(user_pastes) == 0:
        logging.debug('No pastes found for user: {0!r}'.format(user))
        return
    user_output_dir = os.path.join(output_dir, user)
    if not os.path.exists(user_output_dir):
        os.makedirs(user_output_dir)

    download_pastes(paste_ids=user_pastes, output_dir=user_output_dir)

    logging.debug('Finished saving pastes for user: {0!r}'.format(user))
    return


def test_scraping_api():
    # Verify we're authenticated
    api_test_url = 'http://pastebin.com/api_scraping.php'
    api_test_request = requests.get(api_test_url)

    if len(api_test_request.content) < 200:
        logging.error('API test response was too short')
        return False# There should be 50 results provided
    if api_test_request.content[0] != '[':
        logging.error('API test response was not in the expected format')
        return False# The response should be a JSON array

    if '"scrape_url":' in api_test_request.content:
        return True# Test for one of the keys in the results
    raise Exception('Unknown API test response')


### To login:
##
##login_url = 'http://pastebin.com/api/api_login.php'


output_dir = os.path.join('download')
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

##paste_id = 'dzKzY6SR'







download_user_pastes(user='waterapple', output_dir=output_dir)



##user_url = (
##    'http://pastebin.com/api/api_post.php?'
##    'api_dev_key={dev_key}'
##    '&api_user_key={user_key}'
##    '&'
##    ).format()






##'http://pastebin.com/api/api_post.php?api_dev_key=REMOVED&api_user_key={user_key}'



def main():
    logging.basicConfig()
    if not test_scraping_api():
        logging.error('Pastebin scraping API unavailible.')
        return
    else:
        pass


if __name__ == '__main__':
    main()
