#!/usr/bin/env python
# -*- encoding: UTF-8 -*-
#program: image search api
#author: zzq889@gmail.com

import urllib
import simplejson
import re
import os

def _google(keyword, start, size):
	query = urllib.urlencode({'q':keyword, 'rsz':size, 'start':start,'hl':'en','ie':'UTF-8','v':'1.0'})
	url = 'http://ajax.googleapis.com/ajax/services/search/images?%s' % (query)
	search_results = urllib.urlopen(url)
	json = simplejson.loads(search_results.read())
	results_list = json['responseData']['results']
	results = []
	for i in results_list:
		tmp = {}
		tmp['thumb_url'] = i['tbUrl']
		tmp['original'] = i['url']
		tmp['originalContextUrl'] = i['originalContextUrl']
		results.append(tmp)
		del tmp
	search_results.close()
	return results

def s_google(keyword):
	#get 20 results of google image search
	results = []
	results += _google(keyword, 0, 'large')
	results += _google(keyword, 8, 'large')
	results += _google(keyword, 16, 'small')
	return results

def s_bing(keyword):
	AppId='BA1FFA1E8EB59208668D0A07A23517FDAE99703C'
	query = urllib.urlencode({'query':keyword,'sources':'image','AppId':AppId,'Market':'zh-cn','Image.count':20})
	url='http://api.bing.net/json.aspx?%s' % (query)
	search_results = urllib.urlopen(url)
	json = simplejson.loads(search_results.read())
	results_list = json['SearchResponse']['Image']['Results']
	results = []
	for i in results_list:
		tmp = {}
		tmp['thumb_url'] = i['Thumbnail']['Url']
		tmp['original'] = i['MediaUrl']
		tmp['originalContextUrl'] = i['Url']
		results.append(tmp)
		del tmp
	search_results.close()
	return results

def s_yahoo(keyword):
	appid = 'YahooDemo'
	query = urllib.urlencode({'appid':appid,'query':keyword,'results':20,'output':'json','ei':'utf-8'})
	url='http://search.yahooapis.com/ImageSearchService/V1/imageSearch?%s' % (query)
	search_results = urllib.urlopen(url)
	json = simplejson.loads(search_results.read())
	results_list = json['ResultSet']['Result']
	results = []
	for i in results_list:
		tmp = {}
		tmp['thumb_url'] = i['Thumbnail']['Url']
		tmp['original'] = i['Url']
		tmp['originalContextUrl'] = i['RefererUrl']
		results.append(tmp)
		del tmp
	search_results.close()
	return results

def s_flickr(keyword):
	api_key='8397e112823946809261a6da48ea33c0'
	query = urllib.urlencode({'text':keyword,'format':'json','method':'flickr.photos.search','per_page':20,'sort':'date-posted-desc','lang':'zh-hk','api_key':api_key})
	url='http://api.flickr.com/services/rest/?%s' % (query)
	search_results = urllib.urlopen(url)
	json = simplejson.loads(search_results.read()[14:-1])
	results_list = json['photos']['photo']
	results = []
	for i in results_list:
		tmp = {}
		thumb_url = 'http://farm' + str(i['farm']) + '.static.flickr.com/' + i['server'] + '/' + i['id'] + '_' + i['secret'] + '_t.jpg'
		original = 'http://farm' + str(i['farm']) + '.static.flickr.com/' + i['server'] + '/' + i['id'] + '_' + i['secret'] + '_b.jpg'
		originalContextUrl = 'http://www.flickr.com/photos/' + i['owner'] + '/' + i['id'] + '/'
		tmp['thumb_url'] = thumb_url
		tmp['original'] = original
		tmp['originalContextUrl'] = originalContextUrl
		results.append(tmp)
		del tmp
	search_results.close()
	return results

def s_altavista(keyword):
	query = urllib.urlencode({'q':keyword})
	url='http://www.altavista.com/image/results?itag=ody&mik=photo&mik=graphic&mip=all&mis=all&miwxh=all&%s' % (query)
	search_results = urllib.urlopen(url)
	result1 = re.findall(r'<div class=xs>(.+?)</table>',search_results.read(),re.S)[0]
	result2 = re.findall(r'<td(.+?)</td>',result1,re.S)
	rule_thumb_url = re.compile(r'src="(.+?)"',re.S)
	rule_url = re.compile(r'href="(.+?)"',re.S)
	results = []
	for i in result2[:-1]:
		tmp = {}
		tmp['thumb_url'] = rule_thumb_url.search(i).group(1)
		tmp['originalContextUrl'] = rule_url.findall(i)[0]
		tmp['details'] = rule_url.findall(i)[1]
		results.append(tmp)
		del tmp
	search_results.close()
	return results

def s_exalead(keyword):
	query = urllib.urlencode({'q':keyword,'elements_per_page':20})
	url='http://www.exalead.com/search/images/results/?%s' % (query)
	search_results = urllib.urlopen(url)
	result1 = re.findall(r'id="results"(.+?)</ol>',search_results.read(),re.S)[0]
	result2 = re.findall(r'<li(.+?)</li>',result1,re.S)
	rule_url = re.compile(r'href="(.+?)"',re.S)
	rule_thumb_url = re.compile(r'src="(.+?)"',re.S)	
	results = []
	for i in result2:
		tmp = {}
		results.append(tmp)
		tmp['thumb_url'] = rule_thumb_url.search(i).group(1)
		tmp['original'] = rule_url.findall(i)[0]
		tmp['originalContextUrl'] = rule_url.findall(i)[3]
		del tmp
	search_results.close()
	return results

def getImagesWithText(keyword):
	results = []
	#results += s_google(keyword)
	#results += s_bing(keyword)
	#results += s_yahoo(keyword)
	#results += s_flickr(keyword)
	#results += s_altavista(keyword)
	results += s_exalead(keyword)
	
	#get thumbnail with thumb_url, That could be slow
	#getThumbData(results)
	return results
	
def getThumbData(results):
	for i in results:
		t = urllib.urlopen( i['thumb_url'] )
		i['thumb_data'] = t.read()
		t.close()
	return results

if __name__ == '__main__':
	text = u'上海'
	text = text.encode('utf-8')
	s_results = getImagesWithText(text)
	for i in range( len(s_results) ):
		if  s_results[i].has_key( 'original' ):
			print 'Original: ',  s_results[i]['original']
		else:
			print 'Details: ', s_results[i]['details']
		print 'originalContextUrl: ',  s_results[i]['originalContextUrl']
		print 'ThumbUrl: ',  s_results[i]['thumb_url']
		print 'ThumbData: '#, s_results[i]['thumb_data']
		print '-' * 60
		#save images to local
		'''
		try:
			output = file( str(i) + '.jpg','w' )
			output.write( s_results[i]['thumb_data'] )
			output.close()
		except IOError:
			print 'IOError'
			pass
		'''
