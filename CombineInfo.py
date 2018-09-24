#coding=utf-8
import urllib.request
from bs4 import BeautifulSoup
import os
import gzip
import random
import string
import multiprocessing
from fake_useragent import UserAgent





class GetInfoByConID():
    def __int__(self):
        pass


    def getPage(self,url):
        ua = UserAgent()

    #获取网页
        headers = {'User-Agent': ua.random}
        req = urllib.request.Request(url=url, headers=headers)
        res=urllib.request.urlopen(req)
        page = res.read()

        #判断是否压缩
        if res.info().get('Content-Encoding')=='gzip':
            page=gzip.decompress(page)
        soup = BeautifulSoup(page,"html.parser")
        #print(soup)
        return soup

        # 获取名字
    def getAttr(self,url):
        info ={}
        info["conID"] = url.split("user/")[1].replace("\n","")
        soup = self.getPage(url)
        #print(soup)
        name = soup.find_all("p", class_ = "nickname")[0].string
        info["name"] = name
        return info

    def getAllAttr(self):
        file_name = "DOUYINHAO_SHARE_URL"
        f = open(file_name,"r")

        all_info =[]

        for line in f.readlines():
            print(line)
            if len(line) > 10:
                try:
                    info = self.getAttr(line)
                    print(info)
                    all_info.append(info)
                except Exception as erro:
                    print(erro)
                    print("fuck")
                    continue
        return all_info



    def CombineInfo(self):

        all_conID = self.getAllAttr()

        f_conID = open("DouyinHao_ConID","w+")
        f = open("DouyinHao", "r")
        for line in f.readlines():
            origin_info = eval(line)
            origin_name = origin_info["name"]
            for item in all_conID:
                if item["name"] == origin_name and  "重置" not in origin_name:
                    origin_info["conID"] =item["conID"]
                    print(origin_info)
                    f_conID.write(str(origin_info) + "\n")





if __name__ == "__main__":
    url = "https://www.douyin.com/share/user/55497002327"
    info = GetInfoByConID()
    info.CombineInfo()


