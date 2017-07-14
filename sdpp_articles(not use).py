# -*- coding:utf-8 -*-
import requests
from bs4 import BeautifulSoup
import re
import pymysql

def put_db(cname, ctitle, turl):
	cname = str(cname)
	ctitle = str(title)
	turl = str(turl)
	
	try:
		conn = pymysql.connect(host='127.0.0.1', user='root', password='123', db='sdpp', port=3306, charset='utf8')
		cur = conn.cursor()
		sql = "INSERT INTO articles (name,title,url)VALUES(%s,%s,%s)"
		cur.execute(sql,(cname,ctitle, turl))
		conn.commit()
		print(u"成功添加")
	except Exception as e:
		print(u"异常"+e)
	finally:
		cur.close()
		conn.close()

def get_article(url,cname):
	response = requests.get(url)
	soup = BeautifulSoup(response.text,'html.parser')
	for a in soup.find_all('a', class_='red'):
		name = cname.encode('utf-8').strip()
		title = a.get_text.encode('utf-8').strip()
		url = a['href'].encode('utf-8').strip()
		print(u"准备入库")
		put_db(name,title,url)

def get_article_url(response):
	soup =BeautifulSoup(response.text,'html.parser')
	try:
		a=soup.find(class_='loadblockmore font16').get_text.encode('utf-8').strip()
	except Exception as e:
		print(u'没有文章或者没有下一页')
	else:
		print a
		b=int(a[4:-10])/10
		print(u'已获取文章页数')
		for n in range(1,b+2):
			news_url = 'http://www.china-10.com/ajaxstream/?do=loadblock&dataType=text&param=v2_news_col1_brandid%3A'+curl[30:-5]+'_num%3A10_page%3A'+n
			get_article(news_url,cname)
		
def get_db(url):
	response = requests.get(url)
	soup = BeautifulSoup(response.text,'html.parser')
	for comp in soup.find_all('li'):
		cname = comp.get_text().encode('utf-8').strip()
		curl = comp.contents[1]['href'].encode('utf-8').strip()
		curl = str(curl[0:30]+"news_"+curl[30:])
		response=requests.get(curl)   #链接不存在，即公司没有热点新闻
		if response.status_code==200:
			print(u'准备获取文章链接')
			get_article_url(response)
		else:
			print(u'链接无效')
		
def get_url(start):
	url='http://www.china-10.com/ajaxstream/?do=loadblock&dataType=text&param=v2_brand_col5_catid%3A49_num%3A20_morename%3A1_page%3A'
	i = start
	while i<18:
		try:
			a=str(i)
			url1=url+a
			print url1
			get_db(url1)
		except Exception as e:
			print(u"部分信息获取失败")
		finally:
			i+=1
			
if __name__=='__main__':
	get_url(1)
	