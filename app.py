from __future__ import print_function, unicode_literals

import json
import sys

import requests
from bs4 import BeautifulSoup

if (sys.version_info > (3, 0)):
    raw_input = input
    unicode = str

_base_url = "http://www.ipu.ac.in/exam_results.php"


def getSoup(_url):
    """
    Returns the html-parsed-BeautifulSoup object for the given URL.

    Parameters:
        _url: String: the http(s) link to get html from
    """

    try:
        r = requests.get(_url.format(_url))
    except Exception:
        sys.exit("\n CONNECTION ERROR: Check your Internet connection again.\n")

    return BeautifulSoup(r.text, 'html.parser')


def main():
    entered_url = "http://www.ipu.ac.in/exam_results.php"
    soup = getSoup(entered_url)
    print(soup.find(table))

if __name__ == "__main__":
    main()



