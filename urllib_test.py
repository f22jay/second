#!/usr/bin/python 
import urllib
page=urllib.urlopen("http://www.sian.com.cn")
for data in page:
	print data
	#data=page.read().decode('utf-8')
print type(page)
