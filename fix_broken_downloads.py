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
from download_pastes import fetch, test_scraping_api, download_paste




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
    """Return wheter it is appropriate to redownload a paste/file
    Return True if it should be redownloaded, return False if it should not be.
    Raise an exception is it is not recognized."""
    with open(file_path, "rb") as f:
        data = f.read()
        if data == 'Error, this is not a public paste.':# Unlisted?
            return True
        elif data == 'Error, we cannot find this paste.':# Deleted or otherwise invalid pasteid?
            return False
        elif (data[0:9] == 'THIS IP: ') and (data[-70:] == 'ES NOT HAVE ACCESS. VISIT: http://pastebin.com/scraping TO GET ACCESS!'):# Scraping  API not configured
            return True
        elif data == 'Error, this is a private paste. If this is your private paste, please login to Pastebin first.':# Private paste /raw/
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
            success = download_paste(paste_id, output_dir)
            assert(success is not False)# We should stop is something fails
            continue
    print('Finished redownloading pastes listed in {0!r}'.format(input_filepath))
    return


def main():
    if not test_scraping_api():
        print('Pastebin scraping API unavailible.')
        return
    input_filepath = os.path.join('debug', 'find_broken_downloads.failed_test.txt')
    redownload_broken_pastes(input_filepath)

if __name__ == '__main__':
    main()
