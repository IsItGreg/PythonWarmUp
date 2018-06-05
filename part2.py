

import urllib2
import pandas
from bs4 import BeautifulSoup
from warmup import cleanArticle

def getArticle(author, soup, num, count):
    tAuthors = []
    tLinks = []
    tTitles = []
    tLastLink = ""
    tIndexes = []
    newNum = num
    for link in soup.find_all('a'):
        if link.get('href').startswith("/a/") and len(link.get('href')) > 16 and link.get('href') != tLastLink \
                and count < 25:
            tLinks += ["https://www.voanews.com/" + link.get('href')]
            tAuthors += [author]
            tLastLink = link.get('href')
            tIndexes += ["{:0>3d}".format(newNum + count)]
            #print(tLastLink)
            tTitles += [cleanArticle("https://www.voanews.com" + tLastLink, newNum + count)]
            if tTitles[len(tTitles) - 1] == "emptyfile":
                tTitles.pop()
                tIndexes.pop()
                tAuthors.pop()
                tLinks.pop()

            else:
                count+=1
    return tIndexes, tAuthors, tTitles, tLinks, count

def main():
    urls = ["https://www.voanews.com/author/4365.html",
            "https://www.voanews.com/author/25810.html",
            "https://www.voanews.com/author/4345.html",
            "https://www.voanews.com/author/4511.html",
            "https://www.voanews.com/author/25555.html",
            "https://www.voanews.com/author/24557.html",
            "https://www.voanews.com/author/4349.html",
            "https://www.voanews.com/author/23467.html"]

    k = 0
    links = []
    authors = []
    titles = []
    indexes = []
    for i in range(0, len(urls)):
        tempHtml = urllib2.urlopen(urls[i])
        soup = BeautifulSoup(tempHtml, 'html.parser')
        author = soup.find('h1').string
        print(author)

        tempIndexes, tempAuthors, tempTitles, tempLinks, j = getArticle(author, soup, k, 0)
        indexes += tempIndexes
        authors += tempAuthors
        titles += tempTitles
        links += tempLinks
        print(j)

        for l in range(2, 5):
            print("pag" + str(l))
            try:
                tempHtml = urllib2.urlopen(str(urls[i]) + "?page=" + str(l))
            except:
                print("No page number " + str(l))
                continue
            soup = BeautifulSoup(tempHtml, 'html.parser')
            tempIndexes, tempAuthors, tempTitles, tempLinks, j = getArticle(author, soup, k, j)
            indexes += tempIndexes
            authors += tempAuthors
            titles += tempTitles
            links += tempLinks
            k += j
            print(j)

    data = {'Author': authors, 'Title': titles, 'URL': links}
    df = pandas.DataFrame(data, index=indexes).rename_axis("Text #", axis=1)
    df.to_csv('urlMetadata.txt', sep='\t', encoding='utf-8')


if __name__=="__main__":
    main()