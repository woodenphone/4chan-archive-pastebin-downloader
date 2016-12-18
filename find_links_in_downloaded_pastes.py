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
# Local
import config_download_scan





def parse_file(file_path):
    with open(file_path, "rb") as f:
        data = f.read()
        # Find all pastebin user links
        page_user_links = re.findall('pastebin.com/u/[a-zA-Z0-9-_]+', concatenated_comments)

        # Find all pastebin paste links
        page_paste_links = re.findall('pastebin.com/[a-zA-Z0-9]{8}', concatenated_comments)

    found_links = page_user_links + page_paste_links
    print('found_links: {0!r}'.format(found_links))
    return found_links


def parse_files(base_path):
    all_links = []
    c = 0
    print('Starting walk for {0!r}'.format(base_path))
    for directory, dirnames, filenames in os.walk(base_path):
        print('Now walking over folder {0!r}'.format(directory))
        for filename in filenames:
            c += 1
##            if len(all_links) > 10:
##                return all_links
            current_file_path = os.path.join(directory, filename)
            print('Processing file {0}: {1!r}'.format(c, current_file_path))
            links = parse_file(current_file_path)
            all_links.append(all_links)
            continue
        print('Done walking over folder {0!r}'.format(directory))
        continue
    print('Finished walk for {0!r}'.format(base_path))
    print('{0} items in all_links.'.format(len(all_links)))
##    print('all_links:\r\n {0!r}'.format(all_links))
    return all_links





def main():
    output_filepath = os.path.join('debug', 'find_links_in_downloaded_pastes.found_links.txt')
    found_links = parse_files('download')
    output_string = '\n'.join(found_links)
    with open(output_filepath, "wb") as f:
        f.write(output_string)
    print('Finished.')
    return


if __name__ == '__main__':
    main()
