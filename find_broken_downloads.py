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
        if data == 'Error, we cannot find this paste.':# Deleted or otherwise invalid pasteid?
            return False
        elif data == 'Error, this is not a public paste.':# Unlisted?
            return False
        elif data == 'Error, this is a private paste. If this is your private paste, please login to Pastebin first.':# Private paste /raw/
            return False
    return True



def check_files(base_path):
    failed_test = []
    c = 0
    print('Starting walk for {0!r}'.format(base_path))
    for directory, dirnames, filenames in os.walk(base_path):
        print('Now walking over folder {0!r}'.format(directory))
        for filename in filenames:
            c += 1
##            if len(failed_test) > 10:
##                return failed_test
            current_file_path = os.path.join(directory, filename)
##            print('Testing file {0}: {1!r}'.format(c, current_file_path))
            if not check_file(current_file_path):
##                print('Failed.')
                failed_test.append(current_file_path)
##            else: print('Passed')
            continue
        print('Done walking over folder {0!r}'.format(directory))
        continue
    print('Finished walk for {0!r}'.format(base_path))
    print('{0} files failed a test.'.format(len(failed_test)))
##    print('Failed filepaths:\r\n {0!r}'.format(failed_test))
    return failed_test



def main():
    output_filepath = os.path.join('debug', 'find_broken_downloads.failed_test.txt')
    failed_test = check_files('download')
    output_string = '\n'.join(failed_test)
    with open(output_filepath, "wb") as f:
        f.write(output_string)
    print('Finished.')
    return


if __name__ == '__main__':
    main()
