#coding:utf-8
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import os
import time

driver = webdriver.Chrome()
driver.get("https://sh.ke.com/ershoufang/")
print unicode(driver.title)
assert u"上海二手房" in driver.title

#elems = driver.find_element_by_link_text(u'下一页')
#elems.send_keys(Keys.RETURN)

html = driver.page_source
soup = BeautifulSoup(html)


previewDict = {}
xiaoqu_list=soup.findAll('li',{'class':'clear'})
for xq in xiaoqu_list:
	unitDict = {}
	content=xq.find('div',{'class':'title'})

	theTitle_get = unicode(content.a.get_text())
	theTitle_title = unicode(content.a['title'])
	
	#print 'theTitle_get',theTitle_get,"<<"
	#print 'theTitle_title',theTitle_title,'<<'
	try:
		theTitle_alt = unicode(content.a['alt'])
		#print 'theTitle_alt',theTitle_alt,'<<'
	except:
		print 'no alt'

	
	theTitle_href = content.a['href']
	theTitle_id = os.path.basename(theTitle_href).split('.')[0]

	price_content=xq.find('div',{'class':'totalPrice'})
	priceVal = price_content.span.get_text()

	house_content=xq.find('div',{'class':'houseInfo'})
	position_content=xq.find('div',{'class':'positionInfo'})
	follow_content=xq.find('div',{'class':'followInfo'})
	unit_content=xq.find('div',{'class':'unitPrice'})

	#print 'priceVal',priceVal

	basicText = house_content.get_text()
	basicText = basicText.replace(' ','')
	basicText = basicText.replace('\n','')
	spBasic = basicText.split('|')
	#print 'house_content'
	#for i in spBasic:
	#	print i
	#print 'position_text',position_content.a.get_text()
	#print 'position_url',position_content.a['href']

	followText = follow_content.get_text()
	followText = followText.replace(' ','')
	followText = followText.replace('\n','')
	#print 'follow_content',followText
	#print 'unit_content',unit_content.span.get_text()
	print '=' * 50

	logTime = str(time.time())

	unitDict['title'] = theTitle_title
	unitDict['href'] = theTitle_href
	unitDict['price'] = priceVal
	unitDict['id'] = theTitle_id
	unitDict['detail'] = spBasic
	unitDict['follow'] = followText
	unitDict['unitPrice'] = unit_content.span.get_text()
	unitDict['logTime'] = logTime
	unitDict['pubTime'] = ''

	print 'title', unitDict['title']
	print 'href', unitDict['href']
	print 'price', unitDict['price']
	print 'id', unitDict['id']
	print 'detail', unitDict['detail']
	print 'follow', unitDict['follow']
	print 'unitPrice', unitDict['unitPrice']
	print 'logTime', unitDict['logTime']
	print 'pubTime', unitDict['pubTime']

	if theTitle_id not in previewDict.keys():
		previewDict[theTitle_id] = {}

	previewDict[theTitle_id][logTime] = unitDict

#print previewDict