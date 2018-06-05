import urllib2
from bs4 import BeautifulSoup, NavigableString


def cleanArticle(urls, number):
    #urls = ["https://www.voanews.com/a/trump-offers-contradictory-explanation-for-comey-firing/4417821.html"]
    for i in range(0, len(urls)):
        tempUrl = urls[i]
        tempHtml = urllib2.urlopen(tempUrl)
        soup = BeautifulSoup(tempHtml, 'html.parser')
        body = soup.find_all('p')
        with open("url"+"{:0>3d}".format(number)+".txt", "w") as text_file:
            text_file.write(soup.title.string.encode('ascii', 'ignore') +"\n")
            for line in body:
                if line.string != None:
                    text_file.write(line.string.encode('ascii', 'ignore') +"\n")
        #print("Done")
    return soup.title.string


