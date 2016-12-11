#-------------------------------------------------------------------------------
# Name:        find_broken_downloads.py
# Purpose:     Go through downloaded pastes and produce a list of ones that have problems
#
# Author:      User
#
# Created:     11-12-2016
# Copyright:   (c) User 2016
# Licence:     <your licence>
#-------------------------------------------------------------------------------


import os



def check_file(file_path):
    """Given a file path, test if it is a known-bad configuration
    Return True if good, False if bad."""
    with open(file_path, "rb") as f:
        data = f.read()
        if data == 'Error, we cannot find this paste.':
            return False
    return True



def check_files(base_path):
    failed_test = []
    print('Starting walk for {0!r}'.format(base_path))
    for directory, dirnames, filenames in os.walk(base_path):
        print('Now walking over folder {0!r}'.format(directory))
        for filename in filenames:
            current_file_path = os.path.join(directory, filename)
            print('Testing file {0!r}'.format(current_file_path))
            if not check_file(current_file_path):
                print('Failed.')
                failed_test += current_file_path
            else:
                print('Passed')
            continue
        print('Done walking over folder {0!r}'.format(directory))
        continue
    print('Finished walk for {0!r}'.format(base_path))
    print('{0} files failed a test.'.format(len(failed_test)))
    #print('Failed filepaths:\r\n {0!r}'.format(failed_test))
    return failed_test



def main():
    check_files('download')

if __name__ == '__main__':
    main()
