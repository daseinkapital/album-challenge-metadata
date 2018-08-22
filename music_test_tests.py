# -*- coding: utf-8 -*-
"""
Created on Fri Aug 17 13:44:17 2018

@author: Andrew Samuelson
"""

import unittest
import datetime as dt
from music_test import make_album, scrape

class TestWebscraping(unittest.TestCase):

    def test_album_on_wikipedia_time(self):
        alb = make_album("The Rolling Stones", "Let It Bleed")
        scrape(alb)
        time = dt.timedelta(minutes=42, seconds=21)
        self.assertEqual(alb.time, time)
        
    def test_album_on_wikipedia_release_date(self):
        alb = make_album("The Rolling Stones", "Let It Bleed")
        scrape(alb)
        date = dt.datetime.strptime('5 December 1969', '%d %B %Y')
        self.assertEqual(alb.release_date, date)
    
    def test_album_on_wikipedia_album_art(self):
        alb = make_album("The Rolling Stones", "Let It Bleed")
        scrape(alb)
        album_art = "//upload.wikimedia.org/wikipedia/en/thumb/c/c0/LetitbleedRS.jpg/220px-LetitbleedRS.jpg"
        self.assertEqual(alb.album_art, album_art)

    def test_album_on_wikipedia_by_different_artists(self):
        alb1 = make_album("Jay-Z", "The Black Album")
        scrape(alb1)
        alb2 = make_album("Jay-Z", "The Black Album")
        alb2.time = dt.timedelta(minutes=55, seconds=32)
        alb2.release_date =  dt.datetime.strptime('November 14, 2003', '%B %d, %Y')
        alb2.album_art = "//upload.wikimedia.org/wikipedia/en/thumb/0/0e/Jay-Z_-_The_Black_Album.png/220px-Jay-Z_-_The_Black_Album.png"
        self.assertEqual(alb1, alb2)

    def test_album_only_on_bandcamp_time(self):
        alb = make_album("Home", "Odyssey")
        scrape(alb)
        time = dt.timedelta(minutes=47, seconds=41)
        self.assertEqual(alb.time, time)
        
    def test_album_only_on_bandcamp_release_date(self):
        alb = make_album("Home", "Odyssey")
        scrape(alb)
        date = dt.datetime.strptime('July 1, 2014', '%B %d, %Y')
        self.assertEqual(alb.release_date, date)
        
    def test_album_only_on_bandcamp_album_art(self):
        alb = make_album("Home", "Odyssey")
        scrape(alb)
        album_art = "https://f4.bcbits.com/img/a3321951232_16.jpg"
        self.assertEqual(alb.album_art, album_art)

    def test_album_that_uses_characters_from_different_language(self):
        alb1 = make_album("runescape斯凱利", "runescape​.​wav符文風景骨架")
        scrape(alb1)
        alb2 = make_album("runescape斯凱利", "runescape​.​wav符文風景骨架")
        alb2.time = dt.timedelta(minutes=54, seconds=44)
        alb2.release_date = dt.datetime.strptime('January 22, 2018', '%B %d, %Y')
        alb2.album_art = "https://f4.bcbits.com/img/a2793267385_16.jpg"
        self.assertEqual(alb1, alb2)

    def test_album_on_bandcamp_with_name_that_is_also_on_wiki(self):
        alb1 = make_album("Streetlamps for Spotlights", "Sound and Color")
        scrape(alb1)
        alb2 = make_album("Streetlamps for Spotlights", "Sound and Color")
        alb2.time = dt.timedelta(minutes=33 , seconds=36)
        alb2.release_date = dt.datetime.strptime('April 19, 2014', '%B %d, %Y')
        alb2.album_art = "https://f4.bcbits.com/img/a3345060228_16.jpg"
        self.assertEqual(alb1, alb2)

    def test_album_completely_in_another_language(self):
        alb1 = make_album("2 8 1 4","新しい日の誕生")
        scrape(alb1)
        alb2 = make_album("2 8 1 4","新しい日の誕生")
        alb2.time = dt.timedelta(minutes=67 , seconds=23)
        alb2.release_date = dt.datetime.strptime('January 21, 2015', '%B %d, %Y')
        alb2.album_art = "https://f4.bcbits.com/img/a4099353330_16.jpg"
        self.assertEqual(alb1, alb2)

    def test_album_on_bandcamp_second_page(self):
        alb1 = make_album("Taylor Davis", "Odyssey")
        scrape(alb1)
        alb2 = make_album("Taylor Davis", "Odyssey")
        alb2.time = dt.timedelta(minutes=43 , seconds=44)
        alb2.release_date = dt.datetime.strptime('October 28, 2016','%B %d, %Y')
        alb2.album_art = "https://f4.bcbits.com/img/a2565743238_16.jpg"
        self.assertEqual(alb1, alb2)
    

if __name__ == '__main__':
    unittest.main()
    
    
    
#    #standard album on wikipedia
#    test1 = test("The Rolling Stones", "Let It Bleed")
#    print(test1)
#    
#    #album from wikipedia that has the same name as other albums
#    test2 = test("Jay-Z", "The Black Album")
#    print(test2)
#    
#    #album from bandcamp
#    test3 = test("Home", "Odyssey")
#    print(test3)
#    
#    #album from bandcamp that is on the second page
#    test4 = test("Taylor Davis", "Odyssey")
#    print(test4)
#    
#    #album on bandcamp that has the same name as an album on wikipedia (different artist)
#    test5 = test("Death Engine", "Amen")
#    #['16:41', '6/20/13']
#    print(test5)
#    
#    #album that is on wikipedia, but album name alone is a separate page
#    test6 = test("Rich Brian", "Amen")