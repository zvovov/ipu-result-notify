from __future__ import print_function, unicode_literals

import re
import json
import sys
import smtplib

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

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

    date = _content[0]
    text = _content[1]

    result="""\
<html>
<body>
<h3>IPU Result - Latest</h3>
<table>
  <tr>
    <th>Date</th>
    <th>Result</th>
  </tr>
  <tr>
    <td>{}</td>
    <td>{}</td>
  </tr>
  <tr>
    <td>{}</td>
    <td>{}</td>
  </tr>
  <tr>
    <td>{}</td>
    <td>{}</td>
  </tr>
  <tr>
    <td>{}</td>
    <td>{}</td>
  </tr>
  <tr>
    <td>{}</td>
    <td>{}</td>
  </tr>
  <tr>
    <td>{}</td>
    <td>{}</td>
  </tr>
  <tr>
    <td>{}</td>
    <td>{}</td>
  </tr>
  <tr>
    <td>{}</td>
    <td>{}</td>
  </tr>
  <tr>
    <td>{}</td>
    <td>{}</td>
  </tr>
  <tr>
    <td>{}</td>
    <td>{}</td>
  </tr>

</table>
<hr>
<p><a href="http://www.ipu.ac.in/exam_results.php">DOWNLOAD RESULT</a></p>
</body>
</html>
""".format(date[0], text[0], date[1], text[1], date[2], text[2], date[3], text[3],
           date[4], text[4], date[5], text[5], date[6], text[6], date[7], text[7],
           date[8], text[8], date[9], text[9])

    from_addr = ""
    to_addr = ""
    msg = MIMEMultipart()
    msg['From'] = from_addr
    msg['To'] = to_addr
    msg['Subject'] = "TESTING"
    msg.attach(MIMEText(result, 'html'))

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(from_addr, "")
    server.sendmail(from_addr, to_addr, msg.as_string())
    server.quit()


def main():
    current_latest = getLatestResult(_only_last=True)

    if checkUpdate():
        sendMail(getLatestResult())


if __name__ == '__main__':
    main()
