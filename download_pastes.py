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
            # Detect and handle certain known error pages
            if ('<title>Pastebin.com - Heavy Load Warning :(</title>' in response.content[0:500]):# Server overload error page, see private/error cases/heavy load/
                print('Overload error page detected, retrying...'.format())
                continue# Retry
            return response

    raise Exception('Giving up!')


def detect_error_page(data):
    """Detect paste-related error pages (Not site overload page)
    return True if error, False if okay"""
    if data == 'Error, we cannot find this paste.':# Deleted or otherwise invalid pasteid?
        return True
    elif data == 'Error, this is not a public paste.':# Unlisted?
        return True
    elif data == 'Error, this is a private paste. If this is your private paste, please login to Pastebin first.':# Private paste /raw/
        return True
    return False



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


def download_paste(paste_id, output_dir):
    """Save a single paste"""
    assert(len(paste_id) == 8)
    # Prebuild filepaths
    scrape_filepath = os.path.join(output_dir, '{0}.api_raw.txt'.format(paste_id))
    raw_filepath = os.path.join(output_dir, '{0}.raw.txt'.format(paste_id))
    webpage_filepath = os.path.join(output_dir, '{0}.htm'.format(paste_id))
    metadata_filepath = os.path.join(output_dir, '{0}.json'.format(paste_id))

    # Skip if known bad pasteID
    if paste_id in ['scraping', 'download']:
        print('PasteID forbidden: {0!r}'.format(paste_id))
        return False

    # Ensure output dir exists
    if not os.path.exists(output_dir):
        print('Creating dir: {0!r}'.format(output_dir))
        os.makedirs(output_dir)

    # Download things
    # Get paste metadata
    if not os.path.exists(metadata_filepath):
        metadata_url = 'https://pastebin.com/api_scrape_item_meta.php?i={0}'.format(paste_id)
        metadata_response = fetch(metadata_url)
        if (metadata_response.content[0:9] == 'THIS IP: '):# Scraping  API not configured
            raise Exception('API failure!')
        with open(metadata_filepath, "wb") as meta_f:# API metadata
            meta_f.write(metadata_response.content)

    # Get paste scrape api raw data
    if not os.path.exists(scrape_filepath):
        scrape_url = 'https://pastebin.com/api_scrape_item.php?i={0}'.format(paste_id)
        scrape_response = fetch(scrape_url)
        if (scrape_response.content[0:9] == 'THIS IP: '):# Scraping  API not configured
            raise Exception('API failure!')
        with open(scrape_filepath, "wb") as api_f:# API raw paste
            api_f.write(scrape_response.content)

    # Get paste regular raw data
    if not os.path.exists(raw_filepath):
        raw_url = 'https://pastebin.com/raw/{0}'.format(paste_id)
        raw_response = fetch(raw_url)
        with open(raw_filepath, "wb") as reg_f:# Regular raw paste
            reg_f.write(raw_response.content)

    # Get paste webpage data
    if not os.path.exists(webpage_filepath):
        webpage_url = 'https://pastebin.com/{0}'.format(paste_id)
        webpage_response = fetch(webpage_url)
        with open(webpage_filepath, "wb") as web_f:# Webpage of paste
            web_f.write(webpage_response.content)

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
        user_page_url = 'https://pastebin.com/u/{0}/{1}'.format(user, p)
        print('Loading: {0!r}'.format(user_page_url))
        user_page_request = fetch(user_page_url)
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

    download_pastes(paste_ids=user_pastes, output_dir=user_output_dir)

    print('Finished saving pastes for user: {0!r}'.format(user))
    return


def test_scraping_api():
    # Verify we're authenticated
    api_test_url = 'https://pastebin.com/api_scraping.php'
    api_test_request = fetch(api_test_url)
    print('api_test_request.content: {0}'.format(api_test_request.content))

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
##login_url = 'https://pastebin.com/api/api_login.php'




##paste_id = 'dzKzY6SR'











##user_url = (
##    'https://pastebin.com/api/api_post.php?'
##    'api_dev_key={dev_key}'
##    '&api_user_key={user_key}'
##    '&'
##    ).format()






##'https://pastebin.com/api/api_post.php?api_dev_key=REMOVED&api_user_key={user_key}'


def download_users_from_file(user_list_filepath, output_dir):
    with open(user_list_filepath, "rb") as uf:
        with open(config.DONE_USERS_FILEPATH, 'ab') as df:
            c = 0
            for line in uf:
                c += 1
                if c % 100 == 0:
                    print('Up to users line {0}'.format(c))
                if line[0] in ['#','\r','\n']:# Skip empty lines and comments
                    continue
                user_link = line.strip()
                user = re.search('pastebin.com/u/([a-zA-Z0-9-_]+)', user_link).group(1)
                download_user_pastes(user=user, output_dir=output_dir)

                df.write('{0}\n'.format(user))
                continue
    print('Finished saving users from file.')
    return


def download_pastes_from_file(paste_list_filepath, output_dir):
    with open(paste_list_filepath, "rb") as pf:
        with open(config.DONE_PASTES_FILEPATH, 'ab') as df:
            c = 0
            for line in pf:
                c += 1
                if c % 100 == 0:
                    print('Up to pastes line {0}'.format(c))
                if line[0] in ['#','\r','\n']:# Skip empty lines and comments
                    continue
                paste_link = line.strip()
                paste_id = re.search('pastebin.com/([a-zA-Z0-9]{8})', paste_link).group(1)
                download_paste(paste_id, output_dir=output_dir)

                df.write('{0}\n'.format(paste_id))
                continue
    print('Finished saving pastes from file.')
    return


def main():
    #logging.basicConfig()
    if not test_scraping_api():
        print('Pastebin scraping API unavailible.')
        return

    else:
        # Create output folder if it does not exist
        output_dir = config.OUTPUT_DIR
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

##        # DEBUG/WORK
##        download_paste(paste_id='ucnJ08Dx', output_dir=os.path.join('debug', 'singlemode'))
##        return # REMOVEME
##        # /DEBUG/WORK

        # Perform downloads
        download_pastes_from_file(paste_list_filepath=config.FOUND_PASTES_FILEPATH, output_dir=output_dir)
        download_users_from_file(user_list_filepath=config.FOUND_USERS_FILEPATH, output_dir=output_dir)
        # Save from links found in pastes

    print('Done.')
    return


if __name__ == '__main__':
    main()
