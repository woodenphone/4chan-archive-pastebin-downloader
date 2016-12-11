#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      User
#
# Created:     11-12-2016
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
from download_pastes import fetch





def download_broken_paste(paste_id, output_dir):
    """Save a single paste"""
    assert(len(paste_id) == 8)
    # Prebuild filepaths
    scrape_filepath = os.path.join(output_dir, '{0}.api_raw.txt'.format(paste_id))
    raw_filepath = os.path.join(output_dir, '{0}.raw.txt'.format(paste_id))
    webpage_filepath = os.path.join(output_dir, '{0}.htm'.format(paste_id))
    metadata_filepath = os.path.join(output_dir, '{0}.json'.format(paste_id))

    # Skip if already saved
    if (os.path.exists(scrape_filepath)
        and os.path.exists(raw_filepath)
        and os.path.exists(webpage_filepath)
        and os.path.exists(metadata_filepath)):
        print('Already saved')
        return None

    # Skip if known bad pasteID
    if paste_id in ['scraping',]:
        print('PasteID forbidden: {0}'.format(paste_id))
        return False

    # Download things
    # Get paste metadata
    metadata_url = 'http://pastebin.com/api_scrape_item_meta.php?i={0}'.format(paste_id)
    metadata_response = fetch(metadata_url)

    # Get paste scrape api raw data
    scrape_url = 'http://pastebin.com/api_scrape_item.php?i={0}'.format(paste_id)
    scrape_response = fetch(scrape_url)

    # Get paste regular raw data
    raw_url = 'http://pastebin.com/raw/{0}'.format(paste_id)
    raw_response = fetch(raw_url)

    # Get paste webpage data
    webpage_url = 'http://pastebin.com/{0}'.format(paste_id)
    webpage_response = fetch(webpage_url)

    # Save data
    with open(metadata_filepath, "wb") as mf:# API metadata
        mf.write(metadata_response.content)

    with open(scrape_filepath, "wb") as mf:# API raw paste
        mf.write(scrape_response.content)

    with open(raw_filepath, "wb") as mf:# Regular raw paste
        mf.write(raw_response.content)

    with open(webpage_filepath, "wb") as mf:# Webpage of paste
        mf.write(webpage_response.content)

    print('Saved pasteID {0!r}'.format(paste_id))
    return True



def delete_broken_pastes(input_filepath):
    print('Deleting files listed in {0!r}'.format(input_filepath))
    # Get the list of filepaths
    c = 0
    with open(input_filepath, "rb") as lf:
        for line in lf:
            c += 1
            if line[0] in ['#', '\r', '\n']: continue# Skip empty lines and comments
            print('Deleting entry on line {1}: {0!r}'.format(line, c))
            # Split into output_dir and paste_id
            full_filepath = lf.strip()
            # Delete them
            print('Deleting: {0!r}'.format(full_filepath))
            #os.remove(full_filepath)
            continue
    print('Finished deleting files listed in {0!r}'.format(input_filepath))
    return


def check_if_download_is_appropriate(file_path):
    with open(file_path, "rb") as f:
        data = f.read()
        if data == 'Error, this is not a public paste.':# Unlisted?
            return True
        elif data == 'Error, we cannot find this paste.':# Deleted or otherwise invalid pasteid?
            return False
    raise Exception('Unexpected file contents!')


def redownload_broken_pastes(input_filepath):
    print('Redownloading pastes listed in {0!r}'.format(input_filepath))
    # Get the list of filepaths
    c = 0
    with open(input_filepath, "rb") as lf:
        for line in lf:
            c += 1
            if line[0] in ['#', '\r', '\n']: continue# Skip empty lines and comments
            print('Redownloading entry on line {1}: {0!r}'.format(line, c))
            # Split into output_dir and paste_id
            full_filepath = line.strip()
            folder_path, filename = os.path.split(full_filepath)
            paste_id = filename.split('.')[0]
            print('paste_id: {0!r}, folder_path: {1!r}'.format(paste_id, folder_path))
            # Test if we should do a download
            if not check_if_download_is_appropriate(full_filepath):
                print('Skipping redownload of nonexistant paste.')
                continue
            # Put in different folder for safety
            output_dir = os.path.join('debug',folder_path)
            # Ensure output folder exists
            if not os.path.exists(output_dir):
                os.makedirs(output_dir)
            # Perform download
            success = download_broken_paste(paste_id, output_dir)
            assert(success is not False)# We should stop is something fails
            continue
    print('Finished redownloading pastes listed in {0!r}'.format(input_filepath))
    return


def main():
    input_filepath = os.path.join('debug', 'find_broken_downloads.failed_test.txt')
    redownload_broken_pastes(input_filepath)

if __name__ == '__main__':
    main()
