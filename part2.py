

import urllib2
import pandas
from bs4 import BeautifulSoup
from warmup import cleanArticle

def getArticle(author, soup, num, aArtCur):
    tAuthors = []
    tLinks = []
    tTitles = []
    tLastLink = ""
    tIndexes = []
    newNum = num
    aFromP = 0
    if aArtCur >= 35:
        print("Already found 25 articles for " + author)
        return tIndexes, tAuthors, tTitles, tLinks, aFromP
    for link in soup.find_all('a'):
        if link.get('href').startswith("/a/") and len(link.get('href')) > 16 and link.get('href') != tLastLink \
                and aArtCur + aFromP < 35:
            tLinks += ["https://www.voanews.com/" + link.get('href')]
            tAuthors += [author]
            tLastLink = link.get('href')
            tIndexes += ["{:0>3d}".format(newNum + aArtCur + aFromP)]
            #print(tLastLink)
            tTitles += [cleanArticle("https://www.voanews.com" + tLastLink, newNum + aArtCur + aFromP)]
            if tTitles[len(tTitles) - 1] == "emptyfile":
                tTitles.pop()
                tIndexes.pop()
                tAuthors.pop()
                tLinks.pop()

            else:
                aFromP += 1
    #print(aFromP)
    return tIndexes, tAuthors, tTitles, tLinks, aFromP

def main():
    urls = ["https://www.voanews.com/author/4365.html",
            "https://www.voanews.com/author/25810.html",
            "https://www.voanews.com/author/4345.html",
            "https://www.voanews.com/author/19900.html",
            "https://www.voanews.com/author/24557.html",
            "https://www.voanews.com/author/4349.html",
            "https://www.voanews.com/author/23467.html",
            "https://www.voanews.com/author/4945.html"]

    totalArticles = 0
    links = []
    authors = []
    titles = []
    indexes = []
    for i in range(0, len(urls)):
        aArticles = 0
        tempHtml = urllib2.urlopen(urls[i])
        soup = BeautifulSoup(tempHtml, 'html.parser')
        author = soup.find('h1').string
        print(author)

        tempIndexes, tempAuthors, tempTitles, tempLinks, pageArticles = getArticle(author, soup, totalArticles, 0)
        indexes += tempIndexes
        authors += tempAuthors
        titles += tempTitles
        links += tempLinks
        aArticles += pageArticles
        print(aArticles)

        for l in range(2, 10):
            if aArticles >= 35:
                print("Skipping pages")
                break
            pageArticles = 0
            print("pag" + str(l))
            try:
                tempHtml = urllib2.urlopen(str(urls[i]) + "?page=" + str(l))
            except:
                print("No page number " + str(l))
                break
            soup = BeautifulSoup(tempHtml, 'html.parser')
            tempIndexes, tempAuthors, tempTitles, tempLinks, pageArticles = getArticle(author, soup, totalArticles, aArticles)
            indexes += tempIndexes
            authors += tempAuthors
            titles += tempTitles
            links += tempLinks
            aArticles += pageArticles
            print(aArticles)
        totalArticles += aArticles

    data = {'Author': authors, 'Title': titles, 'URL': links}
    df = pandas.DataFrame(data, index=indexes).rename_axis("Text #", axis=1)
    df.to_csv('urlMetadata.txt', sep='\t', encoding='utf-8')


if __name__=="__main__":
    main()