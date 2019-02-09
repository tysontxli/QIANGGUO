#-*-coding:utf-8-*-
import json
import requests
from bs4 import BeautifulSoup

class get_category_url():
    def __init__(self):
        pass

    def formatSourceData(self):
        """
        栏目的URL格式：https://www.xuexi.cn/密文/pageId.html
        catagoryData.txt文件里面是经过linux各种工具处理的含有所有栏目的pageId的js对象，学习强国网页版是通过md5加密json字串的方式去设置每一个栏目的密文，
        通过测试python和js用各自的md5加密方法加密出来的结果不一样，所以为了准确，我们应该继续使用js来进行md5加密，所以这个函数的目的是处理catagoryData.txt中所有js对象，
        使得这些对象成为js数组中的元素。
        :return:
        """
        with open ("./catagoryData.txt","r") as f:
            with open("./FomatCatagoryData.txt","w") as n:
                temp = f.readlines()
                count = 0
                for line in temp:
                    if line.find("param") != -1:
                        new = "param[" + str(count)+"]"
                        line = line.replace("var param", new)
                        count += 1
                    n.writelines(line)

    def formatUrl(self):
        """
        经过get_category_url.js对FomatCatagoryData的处理，拿到了一个包含所有栏目url的json字串，这个字串在json_url_data.txt中
        :return:
        """
        with open ("./json_url_data.txt") as u:
            urlList = json.loads(u.readline())
            return urlList

    def getValidurlList(self):
        urlList = self.formatUrl()
        validurlList = []
        for url in urlList:
            if url != None and url.find('undefined') == -1:
                validurlList.append(url)
        return validurlList

if __name__ == '__main__':
    scrapy = get_category_url()
    scrapy.getValidurlList()
