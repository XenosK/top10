# -*- coding:utf-8 -*-
import requests
from bs4 import BeautifulSoup
from multiprocessing import Process
import pymysql

def put_db(name,title,conten):
	name = str(name)
	title = str(title)
	conten = str(conten)
	try:
		conn = pymysql.connect(host='127.0.0.1', user='root', password='123', db='sdpp', port=3306, charset='utf8')
		cur = conn.cursor()
		sql = "INSERT INTO articles_contents (name,title,content)VALUES(%s,%s,%s)"
		cur.execute(sql,(name,title,conten))
		conn.commit()
		print(u'入库成功')
	except Exception as e:
		print(u"异常%s"%e)
	finally:
		cur.close()
		conn.close()
		
def get_article(url):
	try:
		response = requests.get(url)
		soup = BeautifulSoup(response.text,'html.parser')
		title = soup.find(class_='font24').get_text().encode('utf-8').strip()
		name = soup.find(class_='red').get_text().encode('utf-8').strip()
		content = soup.find(class_='only-cont').get_text().encode('utf-8').strip()
		put_db(name,title,content)
	except Exception as e:
		print(u'链接无效')
	
def get_url():
	conn = pymysql.connect(host='127.0.0.1', user='root', password='123', db='sdpp', port=3306, charset='utf8')
	cur = conn.cursor()
	sql = "SELECT url FROM articles_urls LIMIT 24504,1000"
	cur.execute(sql)
	conn.commit()
	urls = cur.fetchall()
	cur.close()
	conn.close()
	for url in urls:
		url1 = url[0]
		get_article(url1)
		
if __name__=='__main__':
	get_url()
	
	

