import urllib2
import pandas
from bs4 import BeautifulSoup
from warmup import cleanArticle

urls = ["https://www.voanews.com/author/4365.html",
        "https://www.voanews.com/author/25810.html",
        "https://www.voanews.com/author/4345.html",
        "https://www.voanews.com/author/4511.html",
        "https://www.voanews.com/author/25555.html",
        "https://www.voanews.com/author/24557.html",
        "https://www.voanews.com/author/4349.html",
        "https://www.voanews.com/author/23467.html"]

#item = {number, author, title, url}
#list = [items]

k = 0
links = []
authors = []
titles = []
indexes = []
lastLink = ""
for i in range(0, len(urls)):
    print(k)
    tempUrl = urls[i]
    tempHtml = urllib2.urlopen(tempUrl)
    soup = BeautifulSoup(tempHtml, 'html.parser')
    author = soup.find('h1').string
    j = 0
    for link in soup.find_all('a'):
        if link.get('href').startswith("/a/") and len(link.get('href')) > 15 and link.get('href') != lastLink:
            links = links + [link.get('href')]
            authors = authors + [author]
            lastLink = link.get('href')
            url = "https://www.voanews.com" + lastLink
            titles = titles + [cleanArticle([url], k)]
            indexes = indexes + ["{:0>3d}".format(k)]
            j = j + 1
            k = k + 1
    if j >= 19:
        tempHtml = str(tempHtml) + "?page=2"
        soup = BeautifulSoup(tempHtml, 'html.parser')
        for link in soup.find_all('a'):
            if link.get('href').startswith("/a/") and len(link.get('href')) > 15 and link.get('href') != lastLink:
                links = links + [link.get('href')]
                lastLink = link.get('href')
                authors = authors + [author]
                url = "https://www.voanews.com" + lastLink
                titles = titles + [cleanArticle([url], k)]
                indexes = indexes + ["{:0>3d}".format(k)]
                j = j + 1
                k = k + 1
data = {'Author':authors, 'Title':titles, 'URL':links}
df = pandas.DataFrame(data, index=indexes).rename_axis("Text #", axis=1)
df.to_csv('urlMetadata.txt', sep='\t', encoding='utf-8')
