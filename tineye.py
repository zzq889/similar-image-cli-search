#!/usr/bin/env python
#_*_ encode:utf-8 _#_
import urllib2_file
import urllib2

def getImagesWithImage(image): 
	data = {
		'image' : image ,
	}

	return getResult(data)
	
def getImagesWithUrl(url):
	from urllib import urlencode
	data = urlencode({
		'url' : url ,
	})
	return getResult(data)
	
def getResult(data):
	response = urllib2.urlopen('http://www.tineye.com/search',data).read()
	import re
	prog = re.compile(r'<li class="image_backlink">\n.+<a href="([^"]+)"')
	results =  prog.findall(response)
	return list( tuple(results) )
	
if __name__ == '__main__':
	print getImagesWithUrl('http://www.google.co.jp/images/srpr/nav_logo11.png')
	print getImagesWithImage(open('1.png'))
