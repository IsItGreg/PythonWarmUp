import urllib2
from bs4 import BeautifulSoup

urls = ["https://www.voanews.com/a/trump-offers-contradictory-explanation-for-comey-firing/4417821.html"]

for i in range(0, len(urls)):
    tempUrl = urls[i]
    tempText = urllib2.urlopen(tempUrl)


