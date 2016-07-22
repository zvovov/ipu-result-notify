#!usr/bin/env python

from __future__ import print_function, unicode_literals

import json
import random
import re
import sys
import smtplib
import time

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import requests
from bs4 import BeautifulSoup

if (sys.version_info > (3, 0)):
    raw_input = input
    unicode = str

base_url = 'http://www.ipu.ac.in/exam_results.php'
current_latest = ""


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
    elif _type == 'text':
        regex = r'">(.*)</a>'
    elif _type == 'link':
        regex = r'href="(.*)"'
    
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
    latest_result_text_list = findRegex(latest_result_list, 'text')
    latest_result_link_list = findRegex(latest_result_list, 'link')

    latest_result_link_list = [base_url[:20] + latest_result_link_list[i] for i in range(10)]

    return latest_result_date_list, latest_result_text_list, latest_result_link_list


def checkUpdate():
    """
    Returns True if result updated. False otherwise.
    """
    if getLatestResult(_only_last=True) == current_latest:
        return False
    return True


def getSubject():
    """
    Returns a string
    """
    choose = ("This is it", "It's finally here", "Countdown ends", "Hope you prayed",
              "There is hope", "D3@D", "Don't panic!", "You'll be surprised",
              "Okay Okay Okay", "Not a prank", "There's always next sem", "Doomsday",
              "Apocalype Now", "IPU - CP5000", "Over here", "Study Harder", "Don't Cry",
              "End is here", "LOL", "OMG", "STFU", "GTFO", "LMAO", "u wot m8", "Please Read Carefully",
              "Destroy after reading", "Self Destruct in 5..", "Hello", "README",
              "Grades aren't everything", "Winter is Coming", "Winter has Come", "You know nuthing JS",
              "O Dear Lord", "Resistance is futile")

    return random.choice(choose)


def sendMail(_content):
    """
    Sends email to the recepients with the _content
    """
    print("Mail Sent!")

    date = _content[0]
    text = _content[1]
    link = _content[2]

    result="""\
<html>
<body>
<h3>IP University Examination Results - Latest</h3>
<table>
  <tr>
    <th>Date</th>
    <th>Result</th>
  </tr>
  <tr>
    <td>{}</td>
    <td><a href="{}"><div>{}</div></a></td>
  </tr>
  <tr>
    <td>{}</td>
    <td><a href="{}"><div>{}</div></a></td>
  </tr>
  <tr>
    <td>{}</td>
    <td><a href="{}"><div>{}</div></a></td>
  </tr>
  <tr>
    <td>{}</td>
    <td><a href="{}"><div>{}</div></a></td>
  </tr>
  <tr>
    <td>{}</td>
    <td><a href="{}"><div>{}</div></a></td>
  </tr>
  <tr>
    <td>{}</td>
    <td><a href="{}"><div>{}</div></a></td>
  </tr>
  <tr>
    <td>{}</td>
    <td><a href="{}"><div>{}</div></a></td>
  </tr>
  <tr>
    <td>{}</td>
    <td><a href="{}"><div>{}</div></a></td>
  </tr>
  <tr>
    <td>{}</td>
    <td><a href="{}"><div>{}</div></a></td>
  </tr>
  <tr>
    <td>{}</td>
    <td><a href="{}"><div>{}</div></a></td>
  </tr>

</table>
<hr>
<p><a href="http://www.ipu.ac.in/exam_results.php">IPU Website</a></p>
<p><a href="https://linkedin.com/in/khatrichirag">^_^</a></p>
</body>
</html>
""".format(date[0], link[0], text[0], date[1], link[1], text[1],
           date[2], link[2], text[2], date[3], link[3], text[3],
           date[4], link[4], text[4], date[5], link[5], text[5],
           date[6], link[6], text[6], date[7], link[7], text[7],
           date[8], link[8], text[8], date[9], link[9], text[9])

    from_addr = "SENDER_EMAIL"
    to_addr = ["RECEIVER_EMAIL", "RECEIVER_EMAIL"]
    msg = MIMEMultipart()
    msg['From'] = from_addr
    msg['To'] = ', '.join(to_addr)
    msg['Subject'] = "[IPU] " + getSubject()
    msg.attach(MIMEText(result, 'html'))

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(from_addr, "PASSWORD")
    server.sendmail(from_addr, to_addr, msg.as_string())
    server.quit()


def main():
    if checkUpdate():
        sendMail(getLatestResult())

    global current_latest
    current_latest = getLatestResult(_only_last=True)


if __name__ == '__main__':
    if len(sys.argv) > 1:
        try:
            wait_seconds = int(sys.argv[1])
        except ValueError:
            sys.exit("Enter waiting time in seconds. Eg.: 300")
        while True:
            main()
            time.sleep(wait_seconds)
    main()
  