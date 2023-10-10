import requests
from bs4 import BeautifulSoup as BS
import mysql.connector

conn = mysql.connector.connect(
    host='127.0.0.1',
    user='root',
    password='Danil2002',
    database='prelev'
)

class Parser:
    def __init__(self, title:str, pubDate:str, subj:list, tags:str):
        self.title = title
        self.pubDate = pubDate
        self.subj = subj
        self.tags = tags

    def __str__(self):
        newRes = ''
        newRes += self.title +  '\n'
        newRes += self.pubDate +  '\n'
        subStr = ''
        for subs in self.subj:
            subStr += subs + '\n'
        newRes += subStr
        newRes += self.tags + '\n'
        newRes += '\n'
        return newRes

news = []
res = requests.get('https://1prime.ru/export/rss2/index.xml')
soup = BS(res.text, 'xml')
items = soup.find_all('item')
for item in items:
    title = item.find('title')
    pubDate = item.find('pubDate')
    tags = item.find('tags')
    
    if title is not None and pubDate is not None and tags is not None:
        subs = item.find_all('dc:subject')
        subArr = []
        for sub in subs:
            subArr.append(sub.text)
        news.append(Parser(title.text, pubDate.text, subArr, tags.text))

cursor = conn.cursor()

for n in news:
    insert_query = "INSERT INTO news (title, pubDate, subj, tags) VALUES (%s, %s, %s, %s)"
    data = (n.title, n.pubDate, '\n'.join(n.subj), n.tags)
    cursor.execute(insert_query, data)


conn.commit()

cursor.close()
conn.close()
