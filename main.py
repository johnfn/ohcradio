import random
import urllib2
import re
import os
import subprocess
import time

# Given the HTML for a OHC page, attempts to grab the theme from that page.
# Might fail on weird weeks.
def find_theme(html):
    theme = re.findall('(Tonights|Tonight\'s|Todays|Today\'s) theme is:? "(.*)"', html)
    if len(theme) > 0:
        return theme[0][1]
    return "???"

# Given an OHC # and a ranking from the top of the page, returns the path to
# the song at that rank.
def get_ohc_url(which_ohc, which_rank):
    idx = 0

    # Download OHC page
    response = urllib2.urlopen('http://compo.thasauce.net/rounds/view/OHC%s' % which_ohc)
    html = response.read()
    
    print "OHC%s, rank %d (Theme: %s)" % (which_ohc, which_rank + 1, find_theme(html))
    
    # skip over "Materials" section, if there is one
    while True:
        i = html.find('a href="/files/', idx)
        if html.find('Download', idx) - i > 100:
            idx = html.find('a href="/files/', idx) + 1
        else: 
            break
    
    url = ""
    
    # Hack our way through the top 5
    for x in range(5):
        idx = html.find('a href="/files/', idx + 1)
        endidx = html.find('">Download', idx)
        url = "http://compo.thasauce.net" + html[idx + len('a href="'):endidx ]
        if x == which_rank:
            return url

# Randomly selects and downloads an OHC song to disk, returning the path of that song
def download_random_song():
    ohc_num = str(int(random.random() * 225)).zfill(3)
    song_rank = int(random.random() * 5)
    
    # Download the song
    print "Downloading..."
    req = urllib2.Request(get_ohc_url(ohc_num, song_rank))
    mp3response = urllib2.urlopen(req)
    
    # write the mp3 out to disk
    print "Saving..."
    data = mp3response.read()
    name = "ohc%s-%d.mp3" % (ohc_num, song_rank)
    song = open(name, "wb")
    song.write(data)
    song.close()
    
    return name

# fire up the radio!
while True:
    song = download_random_song()
    os.startfile(song)
    time.sleep(int(subprocess.check_output(["./mp3length.exe", song])) + 3)
