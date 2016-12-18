#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      User
#
# Created:     18-12-2016
# Copyright:   (c) User 2016
# Licence:     <your licence>
#-------------------------------------------------------------------------------
from download_pastes import *




INPUT_LIST_FILEPATH = os.path.join('debug', 'find_links_in_downloaded_pastes.found_links.txt')
DONE_LIST_FILEPATH= os.path.join('debug', 'download_links_from_downloaded_pastes.done.txt')
OUTPUT_DIR = os.path.join('download')



def download_from_file(paste_list_filepath, output_dir):
    with open(paste_list_filepath, "rb") as pf:
        with open(DONE_LIST_FILEPATH, 'wb') as df:
            c = 0
            for line in pf:
                c += 1
                if c % 100 == 0:
                    print('Up to line {0}'.format(c))
                if line[0] in ['#','\r','\n']:# Skip empty lines and comments
                    continue
                link = line.strip()
                if '/u/' in link:
                    user = re.search('pastebin.com/u/([a-zA-Z0-9-_]+)', link).group(1)
                    download_user_pastes(user=user, output_dir=output_dir)
                else:
                    paste_id = re.search('pastebin.com/([a-zA-Z0-9]{8})', link).group(1)
                    download_paste(paste_id, output_dir=output_dir)

                df.write('{0}\n'.format(link))
                continue
    print('Finished saving pastes from file.')
    return


def main():
    if not test_scraping_api():
        print('Pastebin scraping API unavailible.')
        return

    else:
        # Create output folder if it does not exist
        output_dir = OUTPUT_DIR
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        # Perform downloads
        download_from_file(paste_list_filepath=INPUT_LIST_FILEPATH, output_dir=output_dir)
        # Save from links found in pastes

    print('Done.')
    return

if __name__ == '__main__':
    main()
