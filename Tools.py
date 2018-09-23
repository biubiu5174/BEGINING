#coding = utf-8
import os
import re
import time
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from appium import webdriver
import sys
import hashlib
import os.path
import pymysql
from moviepy.editor import *
import imageio
import ssl
import time
import random

class Tools():
    def __int__(self):
        pass

    # 提取链接的函数
    def getLinkFromText(self, text):
        pattern = re.compile(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+')  # 匹配模式
        res = re.findall(pattern, text)
        if len(res) >= 1:
            return res[0]
        if len(res) == 0:
            return None

    def getDesFromText(self, text):
        return text.split("活#")[1].split("http")[0].strip()


    def writeToFile(self,content,file_name):
        file_name = os.path.join(os.getcwd(),file_name)
        f = open(file_name,"a+")
        f.write(content)
        f.write("\n")
        f.close()

    def getMD5(self,filename):
        if os.path.isfile(filename):
          fp=open(filename,'rb')
          contents=fp.read()
          fp.close()
          print(hashlib.md5(contents).hexdigest())
        else:
          print('file not exists')

    def getTxtMD5(self, str):
        md5_val = hashlib.md5(str.encode('utf8')).hexdigest()
        return md5_val

    def generate_random_str(self, randomlength=16):
        """
        生成一个指定长度的随机字符串
        """
        random_str = ''
        base_str = 'ABCDEFGHIGKLMNOPQRSTUVWXYZabcdefghigklmnopqrstuvwxyz0123456789'
        length = len(base_str) - 1
        for i in range(randomlength):
            random_str += base_str[random.randint(0, length)]
        return random_str


    def remove_emoji(string):
        sub_str = re.sub(u"([^\u4e00-\u9fa5\u0030-\u0039\u0041-\u005a\u0061-\u007a])", "", string)
        return sub_str


class Video():
    def __int__(self):
        tools = Tools()

    def concat_videos(self,video_list):


        # 看看文件夹是否存在
        upload_dir = os.path.join(os.path.abspath(os.path.join(os.getcwd(), "..")), "UPLOAD")
        if not os.path.exists(upload_dir):
            os.mkdir(upload_dir)

        # 看看当天的文件夹是否存在
        current_day_dir = os.path.join(upload_dir,time.strftime("%Y-%m-%d", time.localtime()))
        if not os.path.exists(current_day_dir):
            os.mkdir(current_day_dir)

        file_name = os.path.join(current_day_dir,
                                 time.strftime("%H-%M-%S", time.localtime())) + tools.generate_random_str(6) + ".mp4"
        print("file_name", file_name)
        # 加载
        video = []
        for line in video_list:
            #print(line)
            video.append(VideoFileClip(line))
        #print(len(video))

        finalclip = concatenate_videoclips(video)
        finalclip.write_videofile(file_name)

    def  get_video_list(self):
        """
        获取要拼接的视频列表
        :return:
        """
        file_name = os.path.join(os.path.abspath(os.path.join(os.getcwd(), "..")), "DOWNLOAD")

        video_list = []
        for line in os.listdir(file_name):
            if "." not in line:
                douyinhao_file = os.path.join(file_name,line)
                for video in os.listdir(douyinhao_file):
                    video_list.append(os.path.join(douyinhao_file, video))
        #print(video_list)
        return video_list


if __name__ == '__main__':
    tools = Tools()
    #video = Video()




