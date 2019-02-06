#-*-coding:utf-8-*-
from bs4 import BeautifulSoup
import requests
import re
import json
import pandas
import MySQLdb

db = MySQLdb.connect("111.230.140.27", "tyson", "123456", "QIANGGUO", charset='utf8')
cursor = db.cursor()
selectsql = "select * from QGNews where article_id = '5b6dbea28951df6091f9843c'"
try:
    cursor.execute(selectsql)
    result = cursor.fetchone()
    if result[1] == '5b6dbea28951df6091f9843c':
        print "匹配成功"

except:
    print "error"