# -*- coding:utf-8 -*-
import pymysql
import requests
from bs4 import BeautifulSoup

def put_db(title, url):
	title = str(title)
	url = str(url)
	
	try:
		conn = pymysql.connect(host='127.0.0.1', user='root', password='123', db='sdpp', port=3306, charset='utf8')
		cur = conn.cursor()
		sql = "INSERT INTO articles_urls (title,url)VALUES(%s,%s)"
		cur.execute(sql,(title, url))
		conn.commit()
		print(u"成功添加")
	except Exception as e:
		print(u"异常")
	finally:
		cur.close()
		conn.close()

def get_article(html):
	soup = BeautifulSoup(html,'html.parser')
	for a in soup.find_all('a',class_='red'):
		title = a.get_text().encode('utf-8').strip()
		url = a['href'].encode('utf-8').strip()
		print(u"准备入库")
		put_db(title,url)
	
def get_news_url(id):
	id=str(id)
	for a in range(1,21):
		b=str(a)
		news_url='http://www.china-10.com/ajaxstream/?do=loadblock&dataType=text&param=v2_news_col1_brandid%3A'+id+'_num%3A10_page%3A'+b
		print news_url
		response = requests.get(news_url)
		if response.status_code==200:
			html = response.text
			get_article(html)
		else:
			print(u'没有文章啊啊啊啊啊啊啊啊啊')

def get_db():
	conn = pymysql.connect(host='127.0.0.1', user='root', password='123', db='sdpp', port=3306, charset='utf8')
	cur = conn.cursor()
	sql = "SELECT url FROM news"
	cur.execute(sql)
	conn.commit()
	urls = cur.fetchall()
	for url in urls:
		url = url[0]
		id = url[35:-5]
		get_news_url(id)
		
if __name__=='__main__':
	get_db()