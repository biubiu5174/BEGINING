#-*- coding: utf-8 -*-
import zbar
from PIL import Image
import os
import Tools

class QR_Code():
    def __init__(self):
        self.tools = Tools.Tools()
        pass


    def getLinkFromPic(self,pic_path):

        #打开含有二维码的图片
        #pytfile_path = '/Users/didi/PycharmProjects/douyin+youtube/QR_CODE_PIC/1346664679.png'
        image = Image.open(pic_path).convert('L')


        scanner = zbar.Scanner()
        results = scanner.scan(image)

        string =str(results)

        try:
            link = self.tools.getLinkFromText(string).replace("'","").replace(",","")
        except:
            link = "None"

        return link


    def getAllLink(self):

        DOUYINHAO_SHARE_URL = os.path.join(os.getcwd(), "DOUYINHAO_SHARE_URL")

        f = open("DOUYINHAO_SHARE_URL", "a+")
        pic_file_path = os.path.join(os.getcwd(), "QR_CODE_PIC", "Camera")
        print(pic_file_path)
        for line in os.listdir(pic_file_path):
            if ".png" in line:
                pic_path = os.path.join(pic_file_path,line)
                link = self.getLinkFromPic(pic_path)
                print(link)
                if link != "None":
                    f.write(link + "\n")
        f.close


class getLinkFromFile():
    def __int__(self):
        pass

    def getDownloadLink(self):
        file = "DOUYINHAO_SHARE_URL"

        all=[]
        f_read = open(file,"r")
        for line in f_read.readlines():
            all.append(line.replace("\n",""))


        file_path = '/Users/didi/PycharmProjects/douyin+youtube/QR_CODE_PIC/Camera'

        f_write = open(file, "a+")


        for line in os.listdir(file_path):
            if ".png" in line:
                id = line.split(".")[0]
                link = "https://www.douyin.com/share/user/" + id
                if link not in all:
                    f_write.write(link +"\n")
                else:
                    print("already in ")

        f_write.close




if __name__ == "__main__":
    #qr_code = QR_Code()
    #pytfile_path = '/Users/didi/PycharmProjects/douyin+youtube/QR_CODE_PIC/1346664679.png'
    #print(qr_code.getLinkFromPic(pytfile_path))
    #qr_code.getAllLink()
    kk = getLinkFromFile()
    kk.getDownloadLink()



