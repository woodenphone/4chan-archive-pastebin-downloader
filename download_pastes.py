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
import config_pastebin as config





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

    print('Saved pasteID {0!r}'.format(paste_id))
    return True


def download_pastes(paste_ids, output_dir):
    print('Downloading paste_ids: {0!r}'.format(paste_ids))
    for paste_id in paste_ids:
        download_paste(paste_id=paste_id, output_dir=output_dir)
    return


def download_user_pastes(user, output_dir):
    # To save everything by a user:
    print('Saving pastes for user: {0!r}'.format(user))
    # Parse the listing for that user
    user_pastes = []
    for p in xrange(1,100):
        # Load the page
        user_page_url = 'http://pastebin.com/u/{0}/{1}'.format(user, p)
        print('Loading: {0!r}'.format(user_page_url))
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
        print('No pastes found for user: {0!r}'.format(user))
        return
    user_output_dir = os.path.join(output_dir, user)
    if not os.path.exists(user_output_dir):
        os.makedirs(user_output_dir)

    download_pastes(paste_ids=user_pastes, output_dir=user_output_dir)

    print('Finished saving pastes for user: {0!r}'.format(user))
    return


def test_scraping_api():
    # Verify we're authenticated
    api_test_url = 'http://pastebin.com/api_scraping.php'
    api_test_request = requests.get(api_test_url)

    if len(api_test_request.content) < 200:
        print('API test response was too short')
        return False# There should be 50 results provided
    if api_test_request.content[0] != '[':
        print('API test response was not in the expected format')
        return False# The response should be a JSON array

    if '"scrape_url":' in api_test_request.content:
        return True# Test for one of the keys in the results
    raise Exception('Unknown API test response')


### To login:
##
##login_url = 'http://pastebin.com/api/api_login.php'




##paste_id = 'dzKzY6SR'











##user_url = (
##    'http://pastebin.com/api/api_post.php?'
##    'api_dev_key={dev_key}'
##    '&api_user_key={user_key}'
##    '&'
##    ).format()






##'http://pastebin.com/api/api_post.php?api_dev_key=REMOVED&api_user_key={user_key}'


def download_users_from_file(user_list_filepath, output_dir):
    with open(user_list_filepath, "rb") as uf:
        with open(config.DONE_USERS_FILEPATH, 'wb') as df:
            c = 0
            for line in uf:
                c += 1
                if c % 100 == 0:
                    print('Up to users line {0}'.format(c))

                user_link = line.strip()
                user = re.search('http://pastebin.com/u/([a-zA-Z0-9-_]+)', user_link).group(1)
                download_user_pastes(user=user, output_dir=output_dir)

                df.write('{0}\n'.format(user))
                continue
    return


def download_pastes_from_file(paste_list_filepath, output_dir):
    with open(paste_list_filepath, "rb") as pf:
        with open(config.DONE_PASTES_FILEPATH, 'wb') as df:
            c = 0
            for line in pf:
                c += 1
                if c % 100 == 0:
                    print('Up to pastes line {0}'.format(c))

                paste_link = line.strip()
                paste_id = re.search('pastebin.com/([a-zA-Z0-9]{8})', paste_link).group(1)
                download_paste(paste_id, output_dir=output_dir)

                df.write('{0}\n'.format(paste_id))
                continue
    return


def main():
    #logging.basicConfig()
    if not test_scraping_api():
        logging.error('Pastebin scraping API unavailible.')
        return

    else:
        # Create output folder if it does not exist
        output_dir = os.path.join('download')
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        # Perform downloads
        download_pastes_from_file(paste_list_filepath=config.FOUND_PASTES_FILEPATH, output_dir=output_dir)

        download_users_from_file(user_list_filepath=config.FOUND_USERS_FILEPATH, output_dir=output_dir)

    print('Done.')
    return


if __name__ == '__main__':
    main()
