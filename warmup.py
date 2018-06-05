import urllib2
import string
from bs4 import BeautifulSoup

def cleanArticle(url, number):
    '''

    :param url:
    :param number:
    :return article title:
    '''
    try:
        html = urllib2.urlopen(url)
    except:
        return "emptyfile"
    soup = BeautifulSoup(html, 'html.parser')
    content = soup.find_all("p")
    count = 0
    keepGoing = True

    print(url)
    with open("article"+"{:0>3d}".format(number)+".txt", "w") as text_file:
        #text_file.write(soup.title.string.encode('ascii', 'ignore') +"\n")
        for line in content:
            if keepGoing == True:
                if line.string == None:
                    for text in line.stripped_strings:
                        if len(text) >= 15 and text != "No media source currently available":
                            #print(str(text.encode('ascii', 'ignore')) + " : " + str(str(text.encode('ascii', 'ignore')).count(' ') + 1))
                            if str(text.encode('ascii', 'ignore')).count(' ') + 1 > 5:
                                count += str(text.encode('ascii', 'ignore')).count(' ') + 1
                            else:
                                text_file.write(text.encode('ascii', 'ignore').upper() + "\n")
                                break
                            if count <=340:
                                text_file.write(text.encode('ascii', 'ignore') +"\n")
                            else:
                                keepGoing = False
                else:
                    #print(str(line.string.encode('ascii', 'ignore')) + " :: " + str(str(line.string.encode('ascii', 'ignore')).count(' ') + 1))
                    if str(text.encode('ascii', 'ignore')).count(' ') + 1 > 5:
                        count += str(line.string.encode('ascii', 'ignore')).count(' ') + 1
                    else:
                        text_file.write(text.encode('ascii', 'ignore').upper() + "\n")
                        continue
                    if count <= 340:
                        text_file.write(line.string.encode('ascii', 'ignore') +"\n")
                    else:
                        keepGoing = False
            else:
                break

    print (str(number) + " " + str(count))

    if count < 300:
        #clear file
        return "emptyfile"

    return soup.title.string


