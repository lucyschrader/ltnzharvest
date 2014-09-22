#!/usr/bin/env python
# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
import requests, os

replacements = {'<br/><br/>': '</p>\n<p>', '“': '"', '”': '"', "’": "'", '…': '...', '–': '&ndash;'}
urls = ['http://librarytechnz.natlib.govt.nz/2011/04/comparing-2008-and-2010-new-zealand-web.html',
'http://librarytechnz.natlib.govt.nz/2011/02/results-of-our-twitter-user-survey.html',
'http://librarytechnz.natlib.govt.nz/2010/12/join-search-terms-word-cloud-map-mashup.html',
'http://librarytechnz.natlib.govt.nz/2010/12/adding-closed-captions-to-youtube.html']

def harvest(url):
    page = requests.get(url)
    full_html = page.text
    soup = BeautifulSoup(full_html)
    title = soup.title.string
    date = soup.find('h2', {'class': 'date-header'}).string
    author = soup.find('span', {'class': 'fn'}).string
    post_content = soup.find("div", {"class": "post-body entry-content"})
    for tag in post_content.findAll('img'):
        if tag.parent.name == 'a':
            filename = tag.parent['href'].split("/")[-1]
            grab_image(tag.parent['href'], filename)
        else:
            filename = tag['src'].split("/")[-1]
            grab_image(tag['src'], filename)
    post_content = clean_html(str(post_content), replacements)
    new_text = generate_text(title, author, date, post_content)
    file_path = "posts/%s.txt" % title
    harvested_post = open(file_path, "w+")
    harvested_post.write(new_text)
    harvested_post.close()

def grab_image(url, filename):
    f = open("images/" + filename,'wb')
    f.write(requests.get(url).content)
    f.close()

def clean_html(html, dic):
    for i, j in dic.iteritems():
        html = html.replace(i, j)
    return html

def generate_text(title, author, date, post_content):
    post_content = post_content.decode('utf-8')
    text = '''
    Title: %s \n
    Author: %s \n
    Date: %s \n \n
    %s
    ''' % (title, author, date, post_content)
    return text

def run():
#    f = open('urls.txt', 'r')
#    for line in f:
    for url in urls:
        try:
            harvest(url)
        except UnicodeDecodeError:
            print '*** Damn it people, don\'t paste straight from Word ***'
            raise
#        finally:
#            f.close()

run()