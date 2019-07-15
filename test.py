#coding:utf-8
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import os
import time
import re

driver = webdriver.Chrome()
driver.get("https://sh.ke.com/ershoufang/18120717410100309898.html")
print unicode(driver.title)
assert u"上海贝壳找房" in driver.title

#elems = driver.find_element_by_link_text(u'下一页')
#elems.send_keys(Keys.RETURN)

html = driver.page_source
soup = BeautifulSoup(html)

transDict = {
	u'房屋户型':'layout',
	u'所在楼层':'floor',
	u'建筑面积':'proportion',
	u'户型结构':'layout_type',
	u'建筑类型':'type',
	u'房屋朝向':'direct',
	u'建筑结构':'struct',
	u'装修情况':'decoration',
	u'梯户比例':'ratio',
	u'配备电梯':'elevator',
	u'产权年限':'years',
	u'挂牌时间':'sell_time',
	u'交易权属':'sell_type',
	u'上次交易':'sell_last',
	u'房屋用途':'usage',
	u'房屋年限':'sell_policy',
	u'产权所属':'right',
	u'抵押信息':'hypothec',
	u'房本备件':'paperwork'
}

transDataDict = {
	
	u'有':True,
	u'满两年':2,
	u'满五年':5,
	u'精装':10,
	u'简装':5,
	u'共有':'share',
	u'非共有':'single',
	u'平层':'flat',
	u'砖混结构':'brick',
	u'砖混结构':'brick',
	u'板楼':'plane',
	u'塔楼':'toward',
	u'普通住宅':'normal',
	u'商品房':'Commercial',
	u'无抵押':False,
	u'高':'high',
	u'中':'middle',
	u'低':'low'
}

def filterData(theKey,theVal):

	if theKey in ['floor']:
		spVal = theVal.split(u'楼层')
		attr1 = transDataDict[spVal[0]]
		attr2 = int(re.findall(r"\d+",labelText_short)[0])
		theVal = [attr1,attr2]

	if theKey in ['proportion','years']:
		theVal = float(re.findall(r"\d+\.?\d*",labelText_short)[0])

	if theKey == 'elevator':
		if theVal in transDataDict.keys():
			theVal = transDataDict[theVal]
		else:
			theVal = False

	if theKey in ['hypothec','decoration','sell_policy','right','layout_type','struct','usage','type','sell_type']:
		if theVal in transDataDict.keys():
			theVal = transDataDict[theVal]


	if theKey in ['sell_time','sell_last','layout']:
		theVal = []
		theTemp = re.findall(r"\d+",labelText_short)
		for tt in theTemp:
			theVal.append(int(tt))

	return theKey,theVal


pageDict = {}
xiaoqu_list=soup.findAll('div',{'class':'content'})
for xq in xiaoqu_list:


	#theText = xq['li'].get_text()

	theLi = xq.findAll('li')
	if theLi:
		for li in theLi:
			#print li
			_span = li.findAll('span',{'class':'label'})
			labelTitle = _span[0].get_text()
			labelText_long = li.get_text()
			labelText_short = labelText_long.split(labelTitle)[-1]

			theKey = transDict[labelTitle]
			theVal = labelText_short
			if '\n' in theVal:
				spVal = theVal.split('\n')
				theVal = spVal[0]

			theKey,theVal = filterData(theKey,theVal)
			pageDict[theKey] = theVal
			#print ''


		#print '='*50

for key,val in pageDict.items():
	print key
	print val
	print ''

