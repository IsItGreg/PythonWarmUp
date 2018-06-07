import urllib2
import string
from bs4 import BeautifulSoup

def fixFile(file):
    wordCount = 0
    lines = []
    with open(file, "r") as text_file:
        for line in text_file:
            if line[0] == ' ':
                line = line[1:]
            if line != "\n" and line[-2] in ['.', ',', '!', '?', '"', "'", ")", "-"]:
                wordCount += line.count(' ') + 1
                lines.append(line)

    with open(file, "w") as text_file:
        for line in lines:
            text_file.write(line)
    return wordCount

def stringToFile(string, file):
    if len(string) >= 15:
        if string.count(' ') + 1 <= 5:
            if any(string.upper() in s for s in ["PRINT", "NO MEDIA SOURCE CURRENTLY AVAILABLE"]):
                return 0

            file.write(string + "\n")
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
                    for text in line:
                        if text.string != None and text.name != "strong":
                            newText = text.string.encode('utf-8')
                            if newText == lastLine:
                                continue
                            if count + newText.count(' ') <=500:
                                #print newText
                                count += stringToFile(newText, text_file)
                                lastLine = newText
                            else:
                                keepGoing = False
                elif "<strong>" not in str(line.contents):
                    #print line.contents
                    newText = line.string.encode('utf-8')
                    if newText == lastLine:
                        continue
                    elif count + newText.count(' ') <= 500:
                        count += stringToFile(newText, text_file)
                        lastLine = newText
                    else:
                        keepGoing = False
            else:
                break

    #print (str(number) + " " + str(count))
    count = fixFile("article"+"{:0>3d}".format(number)+".txt")
    if count < 300:
        #clear file
        #print(count)
        return "emptyfile"

    return soup.title.string


