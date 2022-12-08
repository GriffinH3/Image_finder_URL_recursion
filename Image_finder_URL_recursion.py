'''
John Griffin Harrington
CYBV 473 - Violent Python
October 1, 2020
Assignment#9
'''


import requests
import re
from bs4 import BeautifulSoup
from io import BytesIO
import os
from PIL import Image

pageLinks = set()
baseUrl = "https://casl.website/"
baseDomain = "https://casl/website/"
mustInclude = "casl"
pageLinks.add(baseUrl)

def imageFinder(webpage):
    page = requests.get(webpage)
    soup = BeautifulSoup(page.text, 'html.parser')
    images = soup.findAll('img')    
    for eachImage in images:
        try:
            imgUrl = eachImage['src']
            
            if imgUrl[0:4] != 'http':
                imgUrl = webpage + imgUrl
            response = requests.get(imgUrl)
            imageName = os.path.basename(imgUrl)
            img = Image.open(BytesIO(response.content))
            print(">> Found Image:", imageName)
        except Exception as err:
            print(imgUrl, err)
            continue
   
def urlFinder(webpage):
    page = requests.get(webpage)
    soup = BeautifulSoup(page.text, 'html.parser')    
    urlFind = soup.findAll('link')
    urlFind_1 = soup.findAll('a')    
    for eachUrl in urlFind:
        try:
            foundUrl = eachUrl['href']
            if ( foundUrl[0:4] == 'http' or foundUrl[0:5] == 'https'):
                print(">> Found Url:",foundUrl)
        except:
            continue
    for eachUrl in urlFind_1:
        try:
            foundUrl = eachUrl['href']
            if ( foundUrl[0:4] == 'http' or foundUrl[0:5] == 'https'):
                print(">> Found Url:",foundUrl)
        except:
            continue
        
def titleFinder(webpage):
    page = requests.get(webpage)
    soup = BeautifulSoup(page.text, 'html.parser')
    title = soup.findAll('title')
    for eachTitle in title:
        try:
            foundTitle = eachTitle
            print(">> Found Title:",foundTitle)
        except:
            continue



def RecurseURL(newUrl, base, local):
    try: 
        page = requests.get(newUrl)
        soup = BeautifulSoup(page.text, 'html.parser')
        links = soup.findAll('a')
        if links:
            for eachLink in links:
                newLink = eachLink.get('href')
                
                if not newLink:
                    continue
                
                if 'http' not in newLink:
                    newLink = base+newLink
                    
                if not local in newLink:
                    continue
                
                if newLink not in pageLinks:
                    pageLinks.add(newLink)
                    RecurseURL(newLink, base, local)
                else:
                    continue
                
    except Exception as err:
        print(err)
        

print("Scanning of Main Page:")
titleFinder(baseUrl)
urlFinder(baseUrl)
imageFinder(baseUrl)

print("\nScanning: ", baseUrl, '\n')
RecurseURL(baseUrl, baseDomain, mustInclude)

print("\nScanning Complete\n")
print("Unique URLs Discovered\n")

for eachEntry in pageLinks:
    print(eachEntry)


print("\nScript Complete")
