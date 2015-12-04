# -*- coding: utf-8 -*-
"""
Created on Tue Dec 01 11:43:59 2015

@author: kwher_000
"""
import sys  
from PyQt4.QtGui import *  
from PyQt4.QtCore import *  
from PyQt4.QtWebKit import *  
from lxml import html
import requests
from selenium import webdriver
import csv
import datetime


url = 'http://www.thecurrent.org/listen'  
browser = webdriver.PhantomJS()
browser.get(url)
content = browser.page_source
browser.quit()

tree = html.fromstring(content)
song = tree.xpath('//div[@class="title"]/text()')
artist = tree.xpath('//div[@class="artist"]/text()')
dj = tree.xpath('//div[@class="dj"]/text()')
if len(song)>0:
	song= song[0]
	artist=artist[0]
	if len(dj)<1:
		dj='failed'
	else:
		dj=dj[0]
		dj=dj[3:]

	with open("/home/kyle/currentprev.log","r") as songprev:
		if not song==songprev.read():
			with open("/home/kyle/current.csv","a") as log:
				writer=csv.writer(log)
				writer.writerow([datetime.datetime.now(),song,artist,dj])
		else:
			with open("/home/kyle/current.csv","a") as log:
				writer=csv.writer(log)
				writer.writerow([datetime.datetime.now(),'repeat'])
	with open("/home/kyle/currentprev.log","w") as songprev:
		songprev.write(song)
else:
	print('failed')
	with open("/home/kyle/current.csv","a") as log:
		writer=csv.writer(log)
		writer.writerow([datetime.datetime.now(),'failed'])
