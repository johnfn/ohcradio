import random
import urllib2
import re
import os

def find_theme(html):
    theme = re.findall('(Tonights|Tonight\'s|Todays|Today\'s) theme is:? "(.*)"', html)
    if len(theme) > 0:
        return theme[0][1]
    return "???"

def get_ohc_url(which_ohc, which_rank):
    idx = 0

    # Download OHC page
    response = urllib2.urlopen('http://compo.thasauce.net/rounds/view/OHC%s' % ohcnum)
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
        if x == song_place:
            return url

# Download the song

ohcnum = str(int(random.random() * 225)).zfill(3)
song_place = int(random.random() * 5)

print "Downloading..."
req = urllib2.Request(get_ohc_url(ohcnum, song_place))
mp3response = urllib2.urlopen(req)

# write the mp3 out to disk
print "Saving..."
data = mp3response.read()
name = "ohc%s-%d.mp3" % (ohcnum, 1)
song = open(name, "wb")
song.write(data)
song.close()

os.startfile(name)


