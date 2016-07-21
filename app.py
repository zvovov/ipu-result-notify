from __future__ import print_function, unicode_literals

import re
import json
import sys

import requests
from bs4 import BeautifulSoup

if (sys.version_info > (3, 0)):
    raw_input = input
    unicode = str

base_url = 'http://www.ipu.ac.in/exam_results.php'


def getSoup(_url):
    """
    Returns the html-parsed-BeautifulSoup object for the given URL.

    Parameters:
        _url: String: the http(s) link to get html from
    """

    # try:
    #     r = requests.get(_url.format(_url))
    # except Exception:
    #     sys.exit("\n CONNECTION ERROR: Check your Internet connection again.\n")

    # return BeautifulSoup(r.text, 'html.parser')

    # testing with pre-fetched html
    with open('ipu.html', 'r') as f:
        return BeautifulSoup(f, 'html.parser')


def findRegex(_string, _type):
    """
    Returns either:
        list of dates of format dd-mm-yyyy within _string
        list of link texts of format ...">link-text</a> within _string
        None otherwise

    Parameters:
        _string: List|String: input to search for patterns in
        _type: String: decides which regex will be chosen
    """

    if _type == 'date':
        regex = r'[0-3][0-9]-[0-1][0-9]-[0-9][0-9][0-9][0-9]'
    elif _type == 'link':
        regex = r'">(.*)</a>'
    
    result = re.findall(regex, unicode(_string))
    
    return result if result else None


def main():
    soup = getSoup(base_url)
    result_table = soup.find('table').find('tbody')
    
    latest_date = result_table.find('tr').find_all('td')[-1].string
    result_list = result_table.find_all('tr')

    latest_count = 10
    latest_result_list = result_list[:latest_count]
    first_latest_date = findRegex(latest_result_list[1], 'date')
    last_latest_date = findRegex(latest_result_list[-1], 'date')

    latest_result_text_list = findRegex(latest_result_list, 'link')

    print(latest_result_text_list)





if __name__ == '__main__':
    main()



