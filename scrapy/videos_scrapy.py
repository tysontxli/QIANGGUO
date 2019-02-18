#-*-coding:utf-8-*-
import json
import MySQLdb
import requests
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

class videos_scrapy(object):
    def __init__(self):
        pass

    def __htmltojs__(self,htmlurl):
        jsUrlTemp = htmlurl.rsplit('/')
        jsUrl = jsUrlTemp[0] + '//' + jsUrlTemp[2] + '/' + jsUrlTemp[3] + '/data' + jsUrlTemp[4].replace('html', 'js')
        return jsUrl

    def __decorateVideoUrlDict__(self):
        from aboutCategory.get_category_url import get_category_url
        scrapy = get_category_url()
        #从其他脚本拿到所有可用的栏目url
        validUrlList = scrapy.getValidurlList()
        completedVideoColumnUrl = ["https://www.xuexi.cn/4426aa87b0b64ac671c96379a3a8bd26/datadb086044562a57b441c24f2af1c8e101.js"]
        #将所有新拿到的且内容文章的栏目url，加入到completedArticleColumnUrl这个列表中
        for columnUrl in validUrlList:
            try:
                jsUrl = self.__htmltojs__(columnUrl)
                temp = self.__getVideoList__(jsUrl)
                if len(temp)!=0:
                    flag = 1
                    for i in completedVideoColumnUrl:
                        if jsUrl == i:
                            flag = 0
                    if flag == 1:
                        completedVideoColumnUrl.append(jsUrl)
            except:
                pass
        else:
            return completedVideoColumnUrl

    def __getVideoList__(self,jsUrl):
        """
                :param newsUrl:新闻页面的html地址，而不是js格式的请求地址
                :return: 一个包含了这篇新闻的各种信息的字典对象
                """
        res = requests.get(jsUrl)
        res.encoding= 'utf-8'
        jsondata = json.loads(res.text.lstrip("globalCache = ").rstrip(";"))
        videoList = []
        for key,value in jsondata.items():
            if key == "sysQuery":
                pass
            elif key!= 'sysQuery':
                outsidevalue =  value
                try:
                    for key,value in outsidevalue.items():
                        list = value
                        for unit in list:
                            unitdict = {}
                            unitdict['static_page_url']=unit['static_page_url']
                            unitdict['frst_name']=unit['frst_name']
                            unitdict['cate_id']=unit['cate_id']
                            unitdict['type']=unit['type']
                            try:
                                unitdict['imgUrl'] = json.loads(unit['thumb_image'], encoding="utf-8")[0]['thumbInfo']
                            except:
                                    pass
                            try:
                                unitdict['original_time'] = unit['original_time']
                            except:
                                pass
                            videoList.append(unitdict)
                except:
                    pass
        else:
            return videoList

    def __firstTime__(self):
        videoList = self.__getVideoList__("https://www.xuexi.cn/4426aa87b0b64ac671c96379a3a8bd26/datadb086044562a57b441c24f2af1c8e101.js")
        db = MySQLdb.connect("111.230.140.27", "tyson", "123456", "QIANGGUO", charset='utf8')
        cursor = db.cursor()
        for video in videoList:
            insertsqlbase = "INSERT INTO QGVideos(video_type,video_title,video_url,column_id) VALUES('%s','%s','%s','%s')" % (video['type'],video['frst_name'],video['static_page_url'],video['cate_id'])
            cursor.execute(insertsqlbase)
            video_date = "null"
            video_img_url = "null"
            for key,value in video.items():
                if key == "original_time":
                    video_date = value
                if key == "imgUrl":
                    video_img_url = value
            updatesqlbase = "UPDATE QGVideos SET video_date='%s',video_img_url='%s' WHERE video_url = '%s'"%(video_date,video_img_url,video['static_page_url'])
            cursor.execute(updatesqlbase)
            db.commit()
        print len(videoList)

    def __maintain__(self):
        completedVideoColumnUrl =  self.__decorateVideoUrlDict__()
        print completedVideoColumnUrl
        for url in completedVideoColumnUrl:
            videoList = self.__getVideoList__(url)
            db = MySQLdb.connect("111.230.140.27", "tyson", "123456", "QIANGGUO", charset='utf8')
            cursor = db.cursor()
            newvideo = 0
            oldvideo = 0
            for video in videoList:
                selectsql = "select * from QGVideos where video_url = '%s'" % (video['static_page_url'])
                cursor.execute(selectsql)
                if cursor.rowcount == 0:
                    # ============下方代码需要写函数复用==================
                    insertsqlbase = "INSERT INTO QGVideos(video_type,video_title,video_url,column_id) VALUES('%s','%s','%s','%s')" % (
                    video['type'], video['frst_name'], video['static_page_url'], video['cate_id'])
                    cursor.execute(insertsqlbase)
                    video_date = "null"
                    video_img_url = "null"
                    for key, value in video.items():
                        if key == "original_time":
                            video_date = value
                        if key == "imgUrl":
                            video_img_url = value
                    updatesqlbase = "UPDATE QGVideos SET video_date='%s',video_img_url='%s' WHERE video_url = '%s'" % (
                    video_date, video_img_url, video['static_page_url'])
                    cursor.execute(updatesqlbase)
                    db.commit()
                    #============上方代码需要写函数复用==================
                    print "发现新视频(或图片故事)：《%s》,已为您添加到数据库"%video['frst_name']
                elif cursor.rowcount > 0:
                    oldvideo +=1
            print "这个栏目长度为%s,有%s个是新视频，有%s个是旧视频"%(len(videoList),newvideo,oldvideo)

if __name__=="__main__":
    scrapy = videos_scrapy()
    scrapy.__maintain__()


