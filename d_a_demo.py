# -*- coding:utf-8 -*-
import requests
from bs4 import BeautifulSoup
from multiprocessing import Process,Queue

q=Queue()

def put_db(name,title,conten):
	name = str(name)
	title = str(title)
	conten = str(conten)
	try:
		conn = pymysql.connect(host='127.0.0.1', user='root', password='123', db='sdpp', port=3306, charset='utf8')
		cur = conn.cursor()
		sql = "INSERT INTO articles (name,title,content)VALUES(%s,%s,%s)"
		cur.execute(sql,(name,title,conten))
		conn.commit()
	except Exception as e:
		print(u"异常")
	finally:
		cur.close()
		conn.close()
		
def get_article(url):
	response = requests.get(url)
	soup = BeautifulSoup(response.text,'html.parser')
	name = soup.find(class_='font24').get_text().encode('utf-8').strip()
	title = soup.find(class_='red').get_text().encode('utf-8').strip()
	content = soup.find(class_='only-cont').get_text().encode('utf-8').strip()
	put_db(name,title,content)

def pd_q():
	while q:
		url=q.get()
		get_article(url)
	else:
		print(u'队列没有数据了')
	
def get_url():
	conn = pymysql.connect(host='127.0.0.1', user='root', password='123', db='sdpp', port=3306, charset='utf8')
	cur = conn.cursor()
	sql = "SELECT url FROM articles_urls"
	cur.execute(sql)
	conn.commit()
	urls = cur.fetchall()
	cur.close()
	conn.close()
	for url in urls:
		url1 = url[0]
		q.put(url1,block=False)
		#get_article(url1)
		
if __name__=='__main__':
	get_db = Process(target=get_url, args=())
	get_db.start() 
	put_article = Process(target=get_article, args=())
	put_article.start()
	

