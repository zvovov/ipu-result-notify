from __future__ import print_function, unicode_literals

import re
import json
import sys
import smtplib

from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText

import requests
from bs4 import BeautifulSoup

if (sys.version_info > (3, 0)):
    raw_input = input
    unicode = str

base_url = 'http://www.ipu.ac.in/exam_results.php'
current_latest = "Result (May 2016) of M. Tech (ITW), 6th Sem "


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


def getLatestResult(_only_last=False):
    """
    Returns either:
        10 latest results from the results page.
        1 lastest result from the results page.
    """
    soup = getSoup(base_url)
    result_table = soup.find('table').find('tbody')
    
    latest_date = result_table.find('tr').find_all('td')[-1].string
    latest_text = result_table.find('tr').find('td').find('a').string
    
    if _only_last:
        return latest_text

    result_list = result_table.find_all('tr')

    latest_count = 10
    latest_result_list = result_list[:latest_count]
    
    latest_result_date_list = findRegex(latest_result_list, 'date')
    latest_result_text_list = findRegex(latest_result_list, 'link')
    
    return latest_result_date_list, latest_result_text_list


def checkUpdate():
    """
    Returns True if result updated. False otherwise. 
    """
    if getLatestResult(_only_last=True) == current_latest:
        return False
    return True


def sendMail(_content):
    """
    Sends email to the recepients with the _content 
    """
    print("MAIL!")
    fromaddr = "YOUR ADDRESS"
    toaddr = "ADDRESS YOU WANT TO SEND TO"
    msg = MIMEMultipart()
    msg['From'] = fromaddr
    msg['To'] = toaddr
    msg['Subject'] = "SUBJECT OF THE MAIL"
     
    body = "YOUR MESSAGE HERE"
    msg.attach(MIMEText(body, 'plain'))
     
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(fromaddr, "YOUR PASSWORD")
    text = msg.as_string()
    server.sendmail(fromaddr, toaddr, text)
    server.quit()


def main():
    current_latest = getLatestResult(_only_last=True)

    if checkUpdate():
        sendMail(getLatestResult())


if __name__ == '__main__':
    main()
