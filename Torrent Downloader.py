#-------------------------------------------------------------------------------
# Name:        Search new torrent and Download
# Purpose:
#
# Author:      Nagraj Gajengi
#
# Created:     12/21/2014
#-------------------------------------------------------------------------------
#change the client path
import urllib2
import json
import time
import subprocess
from Tkinter import Tk
from tkFileDialog import askopenfilename
import os
def get_page(url):
    hdr={'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'}
    req = urllib2.Request(url, headers=hdr)
    return urllib2.urlopen(req).read()

def go_to_next_page(page):
    start_link=page.find('<div class="results"')
    page=page[start_link:]
    start_link=page.find("<dl>")
    end_link=page.find("</dl>")
    page=page[start_link:end_link]
    start_link=page.find("<a href=")
    if start_link==-1:
        return False
    start_quote=page.find('"',start_link)
    end_quote=page.find('"',start_quote+1)
    url=page[start_quote+1:end_quote]
    return url

def go_to_torrent_page(page):
    kickFind='<a href="http://katproxy'
    start_link=page.find(kickFind)
    if start_link==-1:
        kickFind='<a href="http://extratorrent.cc'
        start_link=page.find(kickFind)
        if start_link==-1:
            return False
        
    page[start_link-3:]
    start_quote=page.find('"',start_link)
    end_quote=page.find('"',start_quote+1)
    url=page[start_quote+1:end_quote]
    return url

def get_magnet(page):
    titleFind="<title>"
    start_link=page.find(titleFind)+15
    end_link=page.find("</title>")
    title=page[start_link:end_link]
    magnetFind='href="magnet:'
    start_link=page.find(magnetFind)
    if start_link==-1:
        return False,False
    page[start_link-3:]
    start_quote=page.find('"',start_link)
    end_quote=page.find('"',start_quote+1)
    url=page[start_quote+1:end_quote]
    return url,title

searchItem=raw_input("Enter the torrent you wish to search(For Starter Try Arrow):")
completeUrl="http://torrentz.in/search?q="+searchItem.replace(" ","+")
pageContent=get_page(completeUrl)
print "30% done"
newUrl="http://torrentz.in"+go_to_next_page(pageContent) 
nextPageContent=get_page(newUrl)
finalUrl=go_to_torrent_page(nextPageContent)
if finalUrl==False:
    print "Cant process Ahead"
else:
    print "60% done"
    finalPageContent=get_page(finalUrl)
    magnet,title=get_magnet(finalPageContent)
    print "100% done"
    if magnet==False:
        print "Error in finding torrent"
    if magnet!=False:
        print "Torrent downloading is "+title
        if (os.path.exists(os.getcwd()+"/torrentClient.txt")):
                f = open('torrentClient.txt', 'r')
                path=f.readline()
                print "Torrent downloading is "+title
                p = subprocess.Popen([path,magnet])
        else:
                Tk().withdraw()
                path = askopenfilename(title='Select Your Torrent Client')
                f = open("torrentClient.txt", 'w+')
                f.write(path)
                print "Torrent downloading is "+title
                p = subprocess.Popen([path,magnet])
        f.close()
