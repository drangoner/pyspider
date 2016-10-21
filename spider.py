#encoding=utf-8
import urllib2
import sys
import MySQLdb

from bs4 import BeautifulSoup

reload(sys)  
sys.setdefaultencoding('utf8')


def get_html_soup(url):
	response = urllib2.urlopen(url)
	html = response.read()
	soup = BeautifulSoup(html)
	return soup 

bobao_url = "http://bobao.360.cn/search/index?keywords=%E5%8D%97%E6%98%8C%E5%A4%A7%E5%AD%A6&type="

soup = get_html_soup(bobao_url)
content = soup.select('.results > li')
#connect to mysql
db = MySQLdb.connect(host="127.0.0.1", port=3306, user="root", passwd="", db="spider",charset='utf8')
cursor = db.cursor()
for x in content:
	title = str(x.a.string)
	release_time = str(x.select('.sub-time')[0].string)
	source = str(x.select('.orig')[0].string)
	url = str("http://bobao.360.cn" + x.a['href'])
	sql = "INSERT INTO bobao(title, release_time, source, url)	VALUES ('%s', '%s','%s', '%s')"%(title,release_time,source,url)
	try:
		if(cursor.execute("SELECT id from bobao WHERE url='%s'" % url)):
			print "该条信息数据库中已存在！"
		else:
			cursor.execute(sql)
			db.commit()
	except:
		db.rollback()
db.close()