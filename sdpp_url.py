# -*- coding:utf-8 -*-
import requests
from bs4 import BeautifulSoup
import re
import pymysql

cnames = []
curls = []
def put_db(cname,curl):
	cname = str(cname)
	curl = str(curl)
	
	try:
		conn = pymysql.connect(host='127.0.0.1', user='root', password='123', db='sdpp', port=3306, charset='utf8')
		cur = conn.cursor()
		sql = "INSERT INTO company (name,url)VALUES(%s,%s)"
		cur.execute(sql,(cname,curl))
		conn.commit()
		print(u"成功添加")
	except Exception as e:
		print(u"异常"+e)
	finally:
		cur.close()
		conn.close()

def get_db(url):
	response = requests.get(url)
	soup = BeautifulSoup(response.text,'html.parser')
	for comp in soup.find_all('li'):
		cname = comp.get_text().encode('utf-8').strip()
		curl = comp.contents[1]['href'].encode('utf-8').strip()
		print(u'准备入库')
		put_db(cname,curl)
		
def get_url(start):
	url='http://www.china-10.com/ajaxstream/?do=loadblock&dataType=text&param=v2_brand_col5_catid%3A7_num%3A20_morename%3A1_page%3A'
	i = start
	while i<426:
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
	