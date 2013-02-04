import random
import urllib2
import re

ohcnum = str(int(random.random() * 225)).zfill(3)
response = urllib2.urlopen('http://compo.thasauce.net/rounds/view/OHC%s' % ohcnum)
html = ""
html = response.read()

idx = 0

# skip over "Materials" section
while True:
    i = html.find('a href="/files/', idx)
    if html.find('Download', idx) - i > 100:
        idx = html.find('a href="/files/', idx) + 1
    else: 
        break

url = ""

for x in range(5):
    idx = html.find('a href="/files/', idx + 1)
    endidx = html.find('">Download')
    url = "compo.thasauce.net/" + html[idx + len('a href="'):endidx ]
    print url
    break

