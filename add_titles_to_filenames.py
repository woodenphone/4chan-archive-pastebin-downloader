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





INPUT_DIR = os.path.join('download')
OUTPUT_DIR = os.path.join('debug', 'renamed_pastes')



def find_username(html):
    pm_link_search = re.search('<a\shref="/message_compose\?to=([a-zA-Z0-9-_]+)">', data)# Find the username
    if pm_link_search:
        username = pm_link_search.group(1)
        return username
    else:
        return None


def handle_single_paste(paste_id):

    # Find title
    # Try to find username
    # Build new filename
    new_base_filename = '{user}.{title}.{pasteid}'.format()
    # Create new file



# Walk over files in input path
c = 0
print('Starting walk for {0!r}'.format(base_path))
for directory, dirnames, filenames in os.walk(base_path):
    print('Now walking over folder {0!r}'.format(directory))
    for filename in filenames:
        c += 1
        current_file_path = os.path.join(directory, filename)
        print('Processing file {0}: {1!r}'.format(c, current_file_path))




def main():
    pass

if __name__ == '__main__':
    main()
