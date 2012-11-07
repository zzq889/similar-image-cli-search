#!/usr/bin/env python
# -*- encoding: UTF-8 -*-
from searchByText import getImagesWithText
from tineye import getImagesWithImage, getImagesWithUrl
import tempfile

def getBigImagesWithText(keyword):
	f = getImagesWithText(keyword)
	results = []
	results.append(f)
	for i in f:
		#用字典中的缩略图data到tineye中搜索得到结果列表
		'''
		tmp = tempfile.TemporaryFile()
		tmp.write(i['thumb_data'])
		tmp.seek(0)
		results.append( getImagesWithImage(tmp) )
		tmp.close()
		'''
		#用字典中缩略图的url到tineye中搜索得到结果列表
		results.append( getImagesWithUrl(i['thumb_url']) )
	return results

if __name__ == '__main__':
	text = u'世博会'
	text = text.encode('utf-8')
	print getBigImagesWithText(text)
