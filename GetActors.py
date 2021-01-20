import requests
import sys
import os
from bs4 import BeautifulSoup


def get_pic(s , movie):
    s2 = s.replace(' ','_')
    s2 = 'https://fr.wikipedia.org/wiki/' + s2

    req = requests.get(s2)
    soup = BeautifulSoup(req.text, "lxml")

    #with open('txt.html', 'w+') as file:
        #file.write(str(soup))

    for a in soup.find_all("div", {"class":"infobox_v3 large"}):
        #print(str(a) + "\n")
        pic = a.select("img")[0]
        #print('https:' + str(pic['src']))
        ext = str(pic['src']).split('.')[-1]
        #print(ext)
        pic = requests.get('https:' + str(pic['src']))
        #print(pic)
    os.mkdir('data/' + movie + '/' + s)

    try:
        
        with open('data/' + movie + '/' + s + '/' + s + '.' + ext, 'wb+') as file:
            #file.write(pic.text)
            for block in pic.iter_content(1024):
                    if not block:
                        break
                    file.write(block)
        
    except:
        #os.remove(movie + '/' + s + '/' + s + '.' + ext)
        os.rmdir('data/' + movie + '/' + s)

                
s = sys.argv[1]
os.mkdir('data/' + s)
s2 = s.replace(' ','+')
s2 = 'https://www.google.com/search?q=' + s + '+film+distribution'
 
req = requests.get(s2)
soup = BeautifulSoup(req.text, "lxml")

r = 0

for a in soup.find_all("a", {"class":"BVG0Nb"}):
    #print(str(a) + "\n")
    for actor in a.select("div", {"class":"BNeawe s3v9rd AP7Wnd"}):
        if str(actor).count('div') < 3 and 'img' not in str(actor):
            if r % 2 == 0:
                get_pic(actor.text, s)
            #print(actor.text)
            #print('\n')
            r += 1
