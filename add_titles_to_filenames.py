#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      User
#
# Created:     19-12-2016
# Copyright:   (c) User 2016
# Licence:     <your licence>
#-------------------------------------------------------------------------------
# stdlib
import os
import json
import re
import shutil



#INPUT_DIR = os.path.join('download')
INPUT_DIR = os.path.join('debug', 'singlemode')
OUTPUT_DIR = os.path.join('debug', 'renamed_pastes2')



def find_username(html):
    """Find a paste's username from the HTML. Note that this username is unsanitised."""
    pm_link_search = re.search('<a\shref="/message_compose\?to=([a-zA-Z0-9-_]+)">', html)# Find the username
    if pm_link_search:
        # If there is a username
        username = pm_link_search.group(1)
        return username
    else:
        # If there is no username
        return 'ZZZ_NO_USERNAME_FOUND'


def find_title(html):# TODO
    """Find a paste's title from the HTML. Note that this title is unsanitised."""
    raw_title_search = re.search('<div\sclass="paste_box_line1"\stitle="([^"]+)">', html)# Find the title
    if raw_title_search:
        # If there is a title
        raw_title = raw_title_search.group(1)
        print('raw_title: {0!r}'.format(raw_title))
        return raw_title
    else:
        # If there is no title
        return 'ZZZ_NO_TITLE_FOUND'



def handle_single_paste(paste_id, origin_dir, base_output_dir):
    """Process a single paste.
    Find the title and user, generate a filename, and copy the paste files to a subfolder in a target location.
    Return True if successful, False if unsuccessful."""
    print('Processing paste_id: {0} in origin_dir: {1!r} to base_output_dir: {2!r}'.format(paste_id, origin_dir, base_output_dir))
    # Prebuild filepaths
    input_scrape_filepath = os.path.join(origin_dir, '{0}.api_raw.txt'.format(paste_id))
    input_raw_filepath = os.path.join(origin_dir, '{0}.raw.txt'.format(paste_id))
    input_webpage_filepath = os.path.join(origin_dir, '{0}.htm'.format(paste_id))
    input_metadata_filepath = os.path.join(origin_dir, '{0}.json'.format(paste_id))

    # Test expected filepaths
    if not os.path.exists(input_scrape_filepath):
        print('Expected {0!r} to exist but it does not! Skipping this paste.'.format(input_scrape_filepath))
        return False
    if not os.path.exists(input_raw_filepath):
        print('Expected {0!r} to exist but it does not! Skipping this paste.'.format(input_raw_filepath))
        return False
    if not os.path.exists(input_webpage_filepath):
        print('Expected {0!r} to exist but it does not! Skipping this paste.'.format(input_webpage_filepath))
        return False
    if not os.path.exists(input_metadata_filepath):
        print('Expected {0!r} to exist but it does not! Skipping this paste.'.format(input_metadata_filepath))
        return False

    # Try to find username and title
    # HTML file always has them
    with open(input_webpage_filepath, "rb") as web_f:
        html = web_f.read()
        # Find username
        username = find_username(html)
        sanitised_username = re.sub('[^0-9a-zA-Z-_]', '', username)
        # Find title
        title = find_title(html)
        sanitised_title = re.sub('[^0-9a-zA-Z-_]', '', title)

    # Generate output folder path and ensure it exists
    output_dir = os.path.join(base_output_dir, sanitised_username)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Build new filenames
    output_scrape_filepath = os.path.join(output_dir, '{title}.{pasteid}.api_raw.txt'.format(title=sanitised_title,pasteid=paste_id))
    output_raw_filepath = os.path.join(output_dir, '{title}.{pasteid}.raw.txt'.format(title=sanitised_title,pasteid=paste_id))
    output_webpage_filepath = os.path.join(output_dir, '{title}.{pasteid}.htm'.format(title=sanitised_title,pasteid=paste_id))
    output_metadata_filepath = os.path.join(output_dir, '{title}.{pasteid}.json'.format(title=sanitised_title,pasteid=paste_id))

    # Create new files
    shutil.copyfile(src=input_scrape_filepath, dst=output_scrape_filepath)
    shutil.copyfile(src=input_raw_filepath, dst=output_raw_filepath)
    shutil.copyfile(src=input_webpage_filepath, dst=output_webpage_filepath)
    shutil.copyfile(src=input_metadata_filepath, dst=output_metadata_filepath)
    print('Created new files for {0!r}'.format(paste_id))
    return True






base_path = INPUT_DIR
base_output_dir = OUTPUT_DIR
# Walk over files in input path
all_seen_paste_ids = []
done_paste_ids = []
files_seen = 0
print('Starting walk for {0!r}'.format(base_path))
for directory, dirnames, filenames in os.walk(base_path):
    print('Now walking over folder {0!r}'.format(directory))
    # Get paste IDs in this folder
    folder_paste_ids = []
    for filename in filenames:
        files_seen += 1
        if ((filename.endswith('.api_raw.txt'))
        or (filename.endswith('.raw.txt'))
        or (filename.endswith('.htm'))
        or (filename.endswith('.json'))):
            new_paste_id = filename.split('.')[0]
            folder_paste_ids.append(new_paste_id)
    print('folder_paste_ids: {0!r}'.format(folder_paste_ids))
    all_seen_paste_ids += folder_paste_ids

    # Process found paste IDs for this folder
    for paste_id in folder_paste_ids:
        if paste_id not in done_paste_ids:
            handle_single_paste(paste_id=paste_id, origin_dir=directory, base_output_dir=base_output_dir)
            done_paste_ids.append(paste_id)
        continue




def main():
    pass

if __name__ == '__main__':
    main()
