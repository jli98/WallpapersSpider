# coding=utf-8
import urllib
import requests
import re
import time
import smtplib


def getHtml(url):  # get web page source code
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
    response = requests.get(url, headers=headers)
    html = response.content
    return html


def getUrlHead(url):  # get the first part of URL
    a = url.split('/')
    b = ''
    for i in range(len(a) - 1):
        b += a[i] + '/'
    return b


def getImg(html):  # download the picture
    global x
    reg = r'<img id="imageview" src="(.+?\.jpg)" alt='
    imgre = re.compile(reg)
    imglist = re.findall(imgre, getHtml(html))
    for imgurl in imglist:
        urllib.urlretrieve(imgurl, '%s.jpg' % x)
        x += 1
    return imglist


def reminder(user, pwd, recipient, subject,
             body):  # use SMTP protocol to send emails, Gmail setting: Allow less secure apps: OFF
    gmail_user = user
    gmail_pwd = pwd
    FROM = user
    TO = recipient if type(recipient) is list else [recipient]
    SUBJECT = subject
    TEXT = body
    message = """From: %s\nTo: %s\nSubject: %s\n\n%s
    """ % (FROM, ", ".join(TO), SUBJECT, TEXT)
    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.ehlo()
        server.starttls()
        server.login(gmail_user, gmail_pwd)
        server.sendmail(FROM, TO, message)
        server.close()
        print 'successfully sent the mail'
    except:
        print "failed to send mail"


def main(html):  # main function
    try:
        global x
        reg = r'href="(.+?\.htm)" target="_blank"><img src="http://'
        pagereg = re.compile(reg)
        pagelist = re.findall(pagereg, html)
        for i in range(len(pagelist)):
            getImg(getUrlHead(url) + pagelist[i] + '#turn')  # call other functions
            print "download " + str(x) + " pics now."
            time.sleep(1)
    except:
        print 'Error!'
        reminder('liberator1992@gmail.com', '******', 'liberator1992@gmail.com', 'Python,here.', 'An error occurs!')
        exit()


x = 0
url = "http://www.zhuoku.com/zhuomianbizhi/star-starcn/20161111011343.htm"  # album page
main(getHtml(url))
print "all downloads done."
reminder('liberator1992@gmail.com', '******', 'liberator1992@gmail.com', 'Python,here.', 'all downloads done.')
