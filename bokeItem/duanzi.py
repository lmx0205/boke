import requests
from bs4 import BeautifulSoup
import pymysql
from datetime import datetime
import random
import time

conn = pymysql.connect(
    host='localhost',
    user='root',
    password='root',
    port=3306,
    charset='utf8',
    db='boke'
)
cursor = conn.cursor()

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'}

types = ['娱乐', '军事', '网络', '技术', '美食', '医疗', '旅游', '摄影']

# 小说
url = 'https://www.qidian.com/free/all'
html = requests.get(url, headers=headers).text
soup = BeautifulSoup(html, 'lxml')

imgs = soup.find_all('div', attrs={'class': 'book-img-box'})
# for img in imgs:
#     print(img.find('img').attrs['src'])

articles = soup.find_all('div', attrs={'class': 'book-mid-info'})
for article, img in zip(articles, imgs):
    print(article.find('h4').find('a').text)
    print(article.find('p', attrs={'class': 'intro'}).text.replace(' ', ''))
    print(img.find('img').attrs['src'])
    print()
    title = article.find('h4').find('a').text
    content = article.find('p', attrs={'class': 'intro'}).text.replace(' ', '')
    img = img.find('img').attrs['src']
    try:
        sql = 'insert into article (title,content,time,types,img,readcount,agreecount,isexit,user_id) values ("%s","%s","%s","%s","%s","%d","%d","%d","%d")' % (
            title, content, datetime.now().strftime("%Y-%m-%d %H:%M:%S"), random.choice(types), img, random.randint(0, 100), random.randint(0, 100), random.randint(0, 2), random.randint(1, 3))
        cursor.execute(sql)
        conn.commit()
    except:
        pass

conn.close()
