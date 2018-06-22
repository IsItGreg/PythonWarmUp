from urllib.request import urlopen
import string
from bs4 import BeautifulSoup


def fixFile(file):
    print("Fixing: " + file)
    wordCount = 0
    lines = []
    with open(file, "r") as text_file:
        for line in text_file:
            print(line)
            wordCount += line.count(' ') + 1
            lines.append(line)

    lastline = ""
    with open(file, "w") as text_file:
        for line in lines:
            print("line: " + line)
            if line == '\n':
                continue
            if len(lastline) > 2 and lastline[-2] == ' ':
                lastline = lastline[:-1] + line
                line = ""
            elif line[0] in ['.', '!', '?', ',', "'", ';', ':', ']', ')', ' ']:
                lastline = lastline[:-1] + line
                line = ""
            #elif len(line) >= 2 and line[0] in :
            #    lastline = lastline[:-1]
            #    print(lastline + line)
            #    line = ""
                #line = line[:-2]
            print("tofile: " + lastline)
            text_file.write(lastline)
            if line != "":
                lastline = line
    return wordCount


def stringToFile(string, file):
    if len(string) >= 1:
        if string.count(' ') + 1 <= 5:
            if any(string.upper() in s for s in ["PRINT", "NO MEDIA SOURCE CURRENTLY AVAILABLE"]):
                return 0
            # print("To be written: " + string)
            file.write(string + "\n")
            return 0
        else:
            # print("To: " + string)
            file.write(string + "\n")
            return string.count(' ') + 1
    return 0


def cleanArticle(url, number):
    try:
        html = urlopen(url)
    except:
        return "emptyfile"
    soup = BeautifulSoup(html, 'html.parser')
    content = soup.find_all("p")
    count = 0
    keepGoing = True
    lastLine = ""
    # print(url)
    with open("article"+"{:0>3d}".format(number)+".txt", "w") as text_file:
        for line in content:
            if keepGoing:
                if line.string is None:
                    for text in line:
                        if text.string is not None and text.name != "strong":
                            if text.name == "cite":
                                keepGoing = False
                                break
                            newText = text.string

                            if newText == lastLine:
                                continue
                            if count + str(newText).count(' ') <= 500:
                                count += stringToFile(newText, text_file)
                                lastLine = newText
                            else:
                                keepGoing = False
                elif "<cite>" in str(line.contents):
                    keepGoing = False
                elif "<strong>" not in str(line.contents):
                    # print line.contents
                    newText = line.string
                    if newText == lastLine:
                        continue
                    elif count + str(newText).count(' ') <= 500:
                        count += stringToFile(newText, text_file)
                        lastLine = newText
                    else:
                        keepGoing = False
            else:
                break

    # print (str(number) + " " + str(count))
    count = fixFile("article"+"{:0>3d}".format(number)+".txt")
    if count < 300:
        return "emptyfile"

    return soup.title.string


