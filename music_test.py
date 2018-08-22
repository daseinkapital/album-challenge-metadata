# -*- coding: utf-8 -*-
"""
Created on Mon Aug 13 15:45:00 2018

@author: Andrew Samuelson
"""
from urllib.request import urlopen
import urllib.request
from bs4 import BeautifulSoup as bs
import datetime as dt


### Setup for albums and URL fetches
#create the album class
class Album:
    artist = ""
    name = ""
    time = ""
    release_date = ""
    album_art = ""

    def __init__(self, artist, name):
        self.artist = artist
        self.name = name

    def __str__(self):
        return str(self.__dict__)

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    def time_check(self):
        if self.time != "":
            return False
        else:
            return True
    
    def release_date_check(self):
        if self.release_date != "":
            return False
        else:
            return True

    def album_art_check(self):
        if self.album_art != "":
            return False
        else:
            return True

    def all_info_found(self):
        if not self.album_art_check and not self.release_date_check and not self.time_check:
            return True
        else:
            return False

def make_album(artist, name):
    return Album(artist, name)

#grab the html for the page
def fetch_url(url):
    url = url.encode('ascii', errors="ignore").decode()
    html = urlopen(url)
    soup = bs(html, "html.parser")
    return soup


#### Helper functions
#### WIKIPEDIA HELPER FUNCTIONS
#disambiguation check (multiple pages)
def wiki_artist_check(soup, album_object):
    description = soup.find('th', {'class':'description'})
    if description:
        if album_object.artist in description.getText():
            return True
        else:
            return False
    else:
        return False

def disambiguation_check(album):
    album_name = album.name.replace(" ", "_")
    url = "https://en.wikipedia.org/wiki/" + album_name + "_(disambiguation)"
    try:
        fetch_url(url)
    except(ValueError, urllib.error.HTTPError):
        #disambig exists
        url = "https://en.wikipedia.org/wiki/" + album_name
    return url

#double check for an album that shares a name with other albums (or things)
def wiki_double_named_album(url, album):
    try:
        soup = fetch_url(url)
    except(urllib.error.HTTPError):
        return url
    message = album.name + ' may refer to:'
    check = soup.find('div', {'class':'mw-parser-output'}).getText()
    url = "https://en.wikipedia.org/wiki/"
    album_name = album.name.replace(" ", "_")
    if message in check:
        artist_name = album.artist.replace(" ", "_")
        url += album_name + '_(' + artist_name + '_album)'
        return url
    else:
        return url + album_name
    
#finds the full length of the album
def wiki_full_length(soup):
    span = soup.find('span', {'class':'min'})
    if span:
        minutes = span.getText() 
        seconds = soup.find('span', {'class':'s'}).getText()
        total_time = dt.timedelta(minutes=int(minutes), seconds=int(seconds))
        return total_time
    else:
        return ""

#clean the wiki release date before parsing
def wiki_clean_date(soup):
    for child in soup.find_all("span"):
        child.decompose()
    for child in soup.find_all("sup"):
        child.decompose()

#finds the release date of the album
def wiki_release_date(soup):
    span = soup.find('td', {'class':'published'})
    if span:
        wiki_clean_date(span)
        unparsed_date = span.getText().strip('\n')
        try:
            released = dt.datetime.strptime(unparsed_date, '%d %B %Y')
        except(ValueError):
            released = dt.datetime.strptime(unparsed_date, '%B %d, %Y')
        return released
    else:
        return ""

def wiki_album_art(soup):
    sidebar = soup.find('table', {'class': 'infobox vevent haudio'})
    if sidebar:
        img = sidebar.find('img')['src']
        if img:
            return img
    return ""


#### BANDCAMP HELPER FUNCTIONS
#helps filter if weird characters
def filter_str(string):
    return string.encode('ascii', errors="ignore").decode().replace(" ", "")

#loop through pages search results for proper url; returns nothing if match not found
def search_results(results_list, album, search_term):
    album_artist = album.artist.lower()
    album_name = album.name.lower()
    for item in results_list:
        if item.find('div', {'class':'itemtype'}).getText().strip() == search_term:
            album = item.find('div', {'class':'heading'}).getText().lower().strip()
            artist = item.find('div', {'class':'subhead'}).getText().lower().strip()[3:]
            url = item.find('a', {'class':'artcont'})['href']
            if (filter_str(artist) == filter_str(album_artist)) and (filter_str(album) == filter_str(album_name)):
                end = url.find("?")
                return url[:end]
    return ""

#check for album
def check_album(album):
    num = 1
    while num <= 5:
        url = 'https://bandcamp.com/search?page=' + str(num) + '&q=' + album.name.replace(" ", "%20")
        html = fetch_url(url)
        search_term = "ALBUM"
        left_div = html.find('ul', {'class', 'result-items'})
        list_items = left_div.findAll('li')   
        album_url = search_results(list_items, album, search_term)
        if album_url:
            return album_url
        else:
            num += 1
    return ""

#check for artist instead of album
def check_artist(album):
    num = 1
    while num <= 5:
        url = 'https://bandcamp.com/search?page=' + str(num) + '&q=' + album.artist.replace(" ", "%20")
        if url == 'https://bandcamp.com/search?q=':
            return
        html = fetch_url(url)
        search_term = "ALBUM"
        left_div = html.find('ul', {'class', 'result-items'})
        list_items = left_div.findAll('li')
        album_url = search_results(list_items, album, search_term)
        if album_url:
            return album_url
        else:
            num += 1

#find a search result on bandcamp that matches
def bc_navigate_to_page(album):
    url = check_album(album)
    if not url:
        url = check_artist(album)
        if not url:
            return "skip"
        else:
            return url
    else:
        return url        

#find the length of the album on bandcamp    
def bc_full_length(soup):
    times = soup.findAll('span', {'class':'time secondaryText'})
    lengths = []
    pass
    for time in times:
        time = time.getText().strip()
        lengths.append(time)
    total_length = dt.timedelta()
    for i in lengths:
        (m, s) = i.split(':')
        d = dt.timedelta(minutes=int(m), seconds=int(s))
        total_length += d
    return total_length

#find the release date of the album on bandcamp
def bc_release_date(soup):
    init_div = soup.find('div', {'class':'tralbumData tralbum-credits'})
    unparsed_date = init_div.find('meta')['content']
    release_date = dt.datetime.strptime(unparsed_date, '%Y%m%d')
    return release_date

def bc_album_art(soup):
    div = soup.find('div', {'id': 'tralbumArt'})
    if div:
        img = div.find('img')['src']
        if img:
            return img
    return ""    

#### main functions

#check wikipedia for the album
def scrape_wiki(album_object):
    url = disambiguation_check(album_object)
    url = wiki_double_named_album(url, album_object)
    try:
        html = fetch_url(url)
    except(ValueError, urllib.error.HTTPError):
        #print("Couldn't find Wikipedia page")
        return album_object
    if wiki_artist_check(html, album_object):

        if album_object.time_check():
            album_object.time = wiki_full_length(html)
        
        if album_object.release_date_check():
            album_object.release_date = wiki_release_date(html)
        
        if album_object.album_art_check():
            album_object.album_art = wiki_album_art(html)
    
    return album_object
        
def scrape_bc(album_object):
    url = bc_navigate_to_page(album_object)
    if url == "skip":
        return
    try:
        html = fetch_url(url)
    except(ValueError):
        print("Couldn't find bandcamp page")
        return album_object

    if album_object.time_check():
        album_object.time = bc_full_length(html)
    
    if album_object.release_date_check():
        album_object.release_date = bc_release_date(html)

    if album_object.album_art_check():
        album_object.album_art = bc_album_art(html)
    
    return album_object
        
def scrape(album_object):
    # print("Checking Wikipedia")
    scrape_wiki(album_object)
    
    if album_object.all_info_found():
        return
    else:
        # print("Checking Bandcamp")
        scrape_bc(album_object)
    
    if album_object.time_check():
        print("Unable to find total length of album")
    if album_object.release_date_check():
        print("Unable to find album publish date")
    return album_object

def test(artist, album):
    alb = make_album(artist, album)
    scrape_wiki(alb)
    return "Success"
    pass



#album only on bandcamp

def test_suite():
    #standard album on wikipedia
    test1 = test("The Rolling Stones", "Let It Bleed")
    print(test1)
    
    #album from wikipedia that has the same name as other albums
    test2 = test("Jay-Z", "The Black Album")
    print(test2)
    
    #album from bandcamp
    test3 = test("Home", "Odyssey")
    print(test3)
    
    #album from bandcamp that is on the second page
    test4 = test("Taylor Davis", "Odyssey")
    print(test4)
    
    #album on bandcamp that has the same name as an album on wikipedia (different artist)
    test5 = test("Death Engine", "Amen", ['16:41', '6/20/13'])
    print(test5)
    
    #album that is on wikipedia, but album name alone is a separate page
    test6 = test("Rich Brian", "Amen")
    