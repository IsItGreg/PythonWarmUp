import urllib2
import string
from bs4 import BeautifulSoup

def stringToFile(string, file):
    if len(string) >= 15:
        if string.count(' ') + 1 <= 5:
            if any(string.upper() in s for s in ["PRINT", "NO MEDIA SOURCE CURRENTLY AVAILABLE"]):
                return 0
            file.write(string.upper() + "\n")
            return 0
        else:
            file.write(string + "\n")
            return string.count(' ') + 1
    return 0

def cleanArticle(url, number):
    try:
        html = urllib2.urlopen(url)
    except:
        return "emptyfile"
    soup = BeautifulSoup(html, 'html.parser')
    content = soup.find_all("p")
    count = 0
    keepGoing = True
    lastLine = ""
    #print(url)
    with open("article"+"{:0>3d}".format(number)+".txt", "w") as text_file:
        for line in content:
            if keepGoing == True:
                if line.string == None:
                    for text in line.stripped_strings:
                        newText = text.encode('ascii', 'ignore')
                        if newText == lastLine:
                            continue
                        if count + newText.count(' ') <=340:
                            count += stringToFile(newText, text_file)
                            lastLine = newText
                        else:
                            keepGoing = False
                else:
                    newText = line.string.encode('ascii', 'ignore')
                    if newText == lastLine:
                        continue
                    elif count + newText.count(' ') <= 340:
                        count += stringToFile(newText, text_file)
                        lastLine = newText
                    else:
                        keepGoing = False
            else:
                break

    #print (str(number) + " " + str(count))

    if count < 300:
        #clear file
        #print(count)
        return "emptyfile"

    return soup.title.string


