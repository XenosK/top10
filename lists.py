# -*- coding:utf-8 -*-
import requests
from bs4 import BeautifulSoup
import pymysql

def put_db(list,list1):
	list = str(list)
	list1 = str(list1)
	try:
		conn = pymysql.connect(host='127.0.0.1', user='root', password='123', db='sdpp', port=3306, charset='utf8')
		cur = conn.cursor()
		sql = "INSERT INTO lists (list,list1)VALUES(%s,%s)"
		cur.execute(sql,(list,list1))
		conn.commit()
		print(u'入库成功')
	except Exception as e:
		print(u"异常%s"%e)
	finally:
		cur.close()
		conn.close()

def get_list(url):
	response = requests.get(url)
	soup = BeautifulSoup(response.text,'html.parser')
	lis = soup.find_all('li', class_='menu')
	for li in lis:
		for a in li.find_all('a', class_='dhidden'):
			list1 = a.get_text().encode('utf-8').strip()
			list = li.find('a',class_='item').get_text().encode('utf-8').strip()
			put_db(list,list1)
	
if __name__=='__main__':
	url='http://www.china-10.com/china/036mdb_index.html'
	get_list(url)