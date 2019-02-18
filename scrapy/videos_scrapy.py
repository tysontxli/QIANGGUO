#-*-coding:utf-8-*-
import json
import MySQLdb
import requests

class videos_scrapy(object):
    def __init__(self):
        pass

    def __decorateVideoUrlDict__(self):
        from aboutCategory.get_category_url import get_category_url
        scrapy = get_category_url()
        #从其他脚本拿到所有可用的栏目url
        validUrlList = scrapy.getValidurlList()

        #将原来的栏目url字典变成列表
        completedVideoColumnUrl = ["https://www.xuexi.cn/4426aa87b0b64ac671c96379a3a8bd26/datadb086044562a57b441c24f2af1c8e101.js"]

        #将所有新拿到的且内容文章的栏目url，加入到completedArticleColumnUrl这个列表中
        for columnUrl in validUrlList:
            try:
                temp = self.__getVideoList__(columnUrl)
            except:
                print "这不是视频栏目"


    def __getVideoList__(self,columnurl):
        res = requests.get(columnurl)
        try:
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
        except:
            print "该栏目没有提供视频"

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
        pass

if __name__=="__main__":
    scrapy = videos_scrapy()
    scrapy.__decorateVideoUrlDict__()



