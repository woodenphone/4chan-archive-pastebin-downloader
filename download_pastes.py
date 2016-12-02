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
# Libraries
import requests
# Local
import config





def download_paste(paste_id, output_dir):
    """Save a single paste"""
    # Get paste metadata
    metadata_url = 'http://pastebin.com/api_scrape_item_meta.php?i={0}'.format(paste_id)
    metadata_response = requests.get(metadata_url)

    # Get paste raw data
    item_url = 'http://pastebin.com/api_scrape_item.php?i={0}'.format(paste_id)
    item_response = requests.get(item_url)

    # Save both metadata and raw data
    metadata_filepath = os.path.join(output_dir, '{0}.json'.format(paste_id))
    with open(metadata_filepath, "wb") as mf:
        mf.write(metadata_response.content)

    item_filepath = os.path.join(output_dir, '{0}.txt'.format(paste_id))
    with open(item_filepath, "wb") as mf:
        mf.write(item_response.content)

    logging.debug('Saved pasteID {0!r}'.format(paste_id))
    return






output_dir = os.path.join('download')
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

paste_id = 'dzKzY6SR'




# To save everything by a user:
username = 'waterapple'
user_url = ('http://pastebin.com/api_scraping.php?u={username}').format(username=username)


download_paste(paste_id, output_dir)







def main():
    pass

if __name__ == '__main__':
    main()
