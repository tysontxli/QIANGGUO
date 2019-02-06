#-*-coding:utf-8-*-
from bs4 import BeautifulSoup
import requests
import re
import json
import pandas
import MySQLdb
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

#要改写成类
#还要再写一个判断数据库中是否已存在这条数据的语句
class news_scrapy(object):
    def __init__(self):
        # 这里是真的懒得想英文.....而且一共没有几个栏目，不需要写爬虫
        self.__columnUrlDict = {
            "zhongyaoxinwen": "https://www.xuexi.cn/98d5ae483720f701144e4dabf99a4a34/5957f69bffab66811b99940516ec8784.html",
            "zhongyaohuodong": "https://www.xuexi.cn/c06bf4acc7eef6ef0a560328938b5771/9a3668c13f6e303932b5e0e100fc248b.html",
            "zhongyaohuiyi": "https://www.xuexi.cn/89acb6d339cd09d5aaf0c2697b6a3278/9a3668c13f6e303932b5e0e100fc248b.html",
            "zhongyaojianghua": "https://www.xuexi.cn/588a4707f9db9606d832e51bfb3cea3b/9a3668c13f6e303932b5e0e100fc248b.html",
            "zhongyaowenzhang": "https://www.xuexi.cn/6db80fbc0859e5c06b81fd5d6d618749/9a3668c13f6e303932b5e0e100fc248b.html",
            "chuguofangwen": "https://www.xuexi.cn/2e5fc9557e56b14ececee0174deac67f/9a3668c13f6e303932b5e0e100fc248b.html",
            "zhishipishi": "https://www.xuexi.cn/682fd2c2ee5b0fa149e0ff11f8f13cea/9a3668c13f6e303932b5e0e100fc248b.html",
            "handianzhici": "https://www.xuexi.cn/13e9b085b05a257ed25359b0a7b869ff/9a3668c13f6e303932b5e0e100fc248b.html",
            "xinshidaijishi": "https://www.xuexi.cn/9ca612f28c9f86ad87d5daa34c588e00/9a3668c13f6e303932b5e0e100fc248b.html",
            "xuexishipin": "https://www.xuexi.cn/d05cad69216e688d304bb91ef3aac4c6/9a3668c13f6e303932b5e0e100fc248b.html",
            "zonghexinwen": "https://www.xuexi.cn/7097477a9643eacffe4cc101e4906fdb/9a3668c13f6e303932b5e0e100fc248b.html"
            }

    def __getArticleDetail__(self,newsUrl):
        """
        :param newsUrl:新闻页面的html地址，而不是js格式的请求地址
        :return: 一个包含了这篇新闻的各种信息的字典对象
        """
        jsUrlTemp = newsUrl.rsplit('/')
        jsUrl = jsUrlTemp[0] + '//' + jsUrlTemp[2] + '/' + jsUrlTemp[3] + '/data' + jsUrlTemp[4].replace('html', 'js')
        unitInfObj = requests.get(jsUrl)
        unitInfObj.encoding = 'utf-8'
        articleDict={}
        for key,value in json.loads(unitInfObj.text.lstrip('globalCache = ').rstrip(';'),encoding="utf-8").items():
            if key == 'sysQuery':
                pass
            elif key!= 'sysQuery':
                articleDict['frst_name'] =value['detail']['frst_name']
                articleDict['source']=value['detail']['source']
                articleDict['editor']=value['detail']['editor']
                articleDict['original_time']=value['detail']['original_time']
                articleDict['cate_id']=value['detail']['cate_id']
                articleDict['article_url']=newsUrl
                articleDict['page_id']=value['detail']['_id']
                return articleDict
                # return json.dumps(result, encoding="UTF-8", ensure_ascii=False)

    def __getPercolumn_allUrl__(self,columnUrl):
        """
        :param：columnUrl，栏目的网址
        :return:urlList，单个栏目中所有新闻的网址
        """
        jsUrlTemp = columnUrl.rsplit('/')
        jsUrl = jsUrlTemp[0] + '//' + jsUrlTemp[2] + '/' + jsUrlTemp[3] + '/data' + jsUrlTemp[4].replace('html', 'js')
        res = requests.get(jsUrl)
        res.encoding = 'utf-8'
        urlList = []
        for key,value in json.loads(res.text.lstrip('globalCache = ').rstrip(';'),encoding="utf-8").items():
            if key != 'sysQuery':
                for item in  value['list']:
                    urlList.append(item['static_page_url'])
        return urlList

    def __firstTime__(self):
        # newstotal = []
        db = MySQLdb.connect("111.230.140.27","tyson","123456","QIANGGUO",charset='utf8')
        cursor = db.cursor()
        for columnUrl in self.__columnUrlDict.values():
            for url in self.__getPercolumn_allUrl__(columnUrl):
                # newsItemList = []
                newsItemdict = self.__getArticleDetail__(url)
                # newstotal.append(result)
                # data = pandas.DataFrame(newsItemList)
                # pandas.io.sql.write_frame(data,"qiangguoNews",engine)
                # data.to_sql('qiangguoNews', con=engine,if_exists='replace')
                #直接使用DB-API把数据存进去↓
                insertsql = "INSERT INTO QGNews(article_id,article_title,article_url,article_date,article_editor,article_source,column_id) VALUES('%s','%s','%s','%s','%s','%s','%s')"%(newsItemdict['page_id'],newsItemdict['frst_name'],newsItemdict['article_url'],newsItemdict['original_time'],newsItemdict['editor'],newsItemdict['source'],newsItemdict['cate_id'])
                try:
                    cursor.execute(insertsql)
                    db.commit()
                    print insertsql
                except:
                    print "这一次错误"
        cursor.close()

    def __Maintain__(self):
        # newstotal = []
        db = MySQLdb.connect("111.230.140.27", "tyson", "123456", "QIANGGUO", charset='utf8')
        cursor = db.cursor()
        columnNum = 1
        for columnUrl in self.__columnUrlDict.values():
            count = 0
            print "现在对第%s个栏目进行检测" % (columnNum)
            for url in self.__getPercolumn_allUrl__(columnUrl):
                newsItemdict = self.__getArticleDetail__(url)
                selectsql = "select * from QGNews where article_id = '%s'"%(newsItemdict['page_id'])
                cursor.execute(selectsql)
                if cursor.rowcount != 0:
                    if count < 5:
                        selectResult = cursor.fetchone()
                        print "id为%s的文章已存在，不需要更新" % (selectResult[1])
                        count +=1
                    else:
                        print "第%s个栏目的文章已经不需要更新了"%(columnNum)
                        columnNum = columnNum+1
                        break
                else:
                    insertsql = "INSERT INTO QGNews(article_id,article_title,article_url,article_date,article_editor,article_source,column_id) VALUES('%s','%s','%s','%s','%s','%s','%s')" % (
                    newsItemdict['page_id'], newsItemdict['frst_name'], newsItemdict['article_url'],
                    newsItemdict['original_time'], newsItemdict['editor'], newsItemdict['source'],
                    newsItemdict['cate_id'])
                    try:
                        cursor.execute(insertsql)
                        db.commit()
                        print "这是一则新的文章，id为%s，已为您更新到数据库" % (newsItemdict['page_id'])
                    except:
                        print "这一次插入数据错误"

        else:
            print "本日的更新已完成"

        cursor.close()

if __name__ == '__main__':
    scrapy = news_scrapy()
    # scrapy.__firstTime__()
    scrapy.__Maintain__()
