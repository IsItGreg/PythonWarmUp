import urllib2
from bs4 import BeautifulSoup, NavigableString


def cleanArticle(url, number):
    '''

    :param url:
    :param number:
    :return article title
    '''
    html = urllib2.urlopen(url)
    soup = BeautifulSoup(html, 'html.parser')
    content = soup.find_all('p')
    with open("article"+"{:0>3d}".format(number)+".txt", "w") as text_file:
        text_file.write(soup.title.string.encode('ascii', 'ignore') +"\n")
        for line in content:
            if line.string != None:
                text_file.write(line.string.encode('ascii', 'ignore') +"\n")
    return soup.title.string


