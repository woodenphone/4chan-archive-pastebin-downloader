#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      User
#
# Created:     05-12-2016
# Copyright:   (c) User 2016
# Licence:     <your licence>
#-------------------------------------------------------------------------------
import datetime

### Desustorage /mlp/
### Config vars
##BASE_URL = 'http://desuarchive.org'# ex. 'http://desuarchive.org'
##BOARD = 'mlp'# ex. 'mlp'
##MAX_SEARCH_PAGES = (1000/25)+1# desustorage shows 25 posts per page, with a maximum of 1000 results
##
##START_DATE = datetime.date(2016,11,1)
##END_DATE = datetime.date(2017,1,1)
##STEP_LENGTH = datetime.timedelta(7)
##
##
### Output paths
##FOUND_USERS_FILEPATH = 'found_users.txt'
##FOUND_PASTES_FILEPATH = 'found_pastes.txt'



# http://thebarchive.com/ /b/
# Config vars
BASE_URL = 'http://thebarchive.com'# ex. 'http://desuarchive.org'
BOARD = 'b'# ex. 'mlp'
MAX_SEARCH_PAGES = (1000/25)+1# desustorage shows 25 posts per page, with a maximum of 1000 results

START_DATE = datetime.date(2016,11,1)
END_DATE = datetime.date(2017,1,1)
STEP_LENGTH = datetime.timedelta(7)


# Output paths
FOUND_USERS_FILEPATH = 'b_found_users.txt'
FOUND_PASTES_FILEPATH = 'b_found_pastes.txt'



def main():
    pass

if __name__ == '__main__':
    main()
