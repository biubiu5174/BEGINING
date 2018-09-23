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
from Tools import Tools
import subprocess


class Action():
    def __init__(self):
        # 启动 appium
        #os.system("appium")

        apk_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "aweme_aweGW_v2.5.1_ec89c14.apk"))
        self.desired_caps = {}
        self.desired_caps['platformName'] = 'Android'  # 设备系统
        #desired_caps['deviceName'] = '127.0.0.1:62001'  # 设备名称
        self.desired_caps['deviceName'] = 'Android'
        self.desired_caps['appPackage'] = 'com.ss.android.ugc.aweme'
        self.desired_caps['appActivity'] = 'main.MainActivity'
        self.desired_caps['unicodeKeyboard'] = True
        self.desired_caps['resetKeyboard'] = True
        self.desired_caps['app'] = apk_path   # 测试apk包的路径
        self.desired_caps['noReset'] = True   # 保留之前的app状态

        self.driver = webdriver.Remote('http://localhost:4723/wd/hub', self.desired_caps)

        """
        # 权限跳过
        try:
            self.driver.find_element_by_id('com.android.packageinstaller:id/permission_allow_button').click()
            self.driver.find_element_by_id('com.android.packageinstaller:id/permission_allow_button').click()


        except:
            pass
        """

        # 点掉版本升级 还有跳过广告
        time.sleep(10)
        os.system("adb shell input tap 500 1370 ")

        try:
            self.driver.find_element_by_id('com.ss.android.ugc.aweme:id/bfw').click()
        except:
            pass

        time.sleep(3)
        os.system("adb shell input tap 500 1370 ")
        os.system("adb shell input tap 500 500 ")  # 停止视频

        #self.driver.keyevent(4)

        # 实例化tools类
        self.tools = Tools()

        print("-----------------初始化完成------------------")


    def getDouyinHao(self):
        # 进入页面
        self.driver.implicitly_wait(10)
        self.driver.find_element_by_xpath("//android.widget.TextView[@text='我']").click()   # 进入 "我"
        count = int(self.driver.find_element_by_id("com.ss.android.ugc.aweme:id/a3f").get_attribute("text"))
        print(count)
        self.driver.find_element_by_id("com.ss.android.ugc.aweme:id/a3f").click()


        # 读取原有信息
        check_f = open("DouyinHao","r")
        all_name = []
        for line in check_f.readlines():
            try:
                print(line)
                all_name.append(eval(line)["name"])
            except:
                print("fuck6")
                pass
        cur_count = len(all_name)
        print("all_name")
        print(all_name)
        check_f.close()


        # 写入信息
        f = open("DouyinHao","a+")

        while count > cur_count :
            try:
                # 遍历所有元素
                items = self.driver.find_elements_by_id("com.ss.android.ugc.aweme:id/amq")
                for line in items:
                    info = {}
                    name = line.get_attribute("text").replace("@", "")

                    # 判断是否已经有了
                    if name in all_name:
                        continue

                    # 进入个人主页
                    line.click()
                    try:
                        # 采集大V信息
                        info["name"] = self.driver.find_element_by_id("com.ss.android.ugc.aweme:id/yc").get_attribute("text")
                        try:
                            temp_string = self.driver.find_element_by_id("com.ss.android.ugc.aweme:id/yb").get_attribute("text")
                            info["douyinID"]= temp_string.split(":")[1]
                        except:
                            pass
                        info["fans"] = self.driver.find_element_by_id("com.ss.android.ugc.aweme:id/a3h").get_attribute("text")
                        info["des"] = self.driver.find_element_by_id("com.ss.android.ugc.aweme:id/a35").get_attribute("text")
                    except:
                        continue

                    print(str(info))
                    f.write(str(info))
                    f.write("\n")
                    cur_count = cur_count +1
                    self.driver.keyevent(4)  # 返回

            except:
                self.driver.keyevent(4)   # 返回


            os.system("adb shell input swipe 500 1400 500 600")
        f.close()



    def getDouyinHaoSharePic(self):

        all_name = []
        f_read = open("Share_Pic_Histroy","r")
        for line in f_read.readlines():
            all_name.append(eval(line)["name"])



        # 获取历史
        f = open("Share_Pic_Histroy","a+")


        # 进入页面
        self.driver.implicitly_wait(10)
        self.driver.find_element_by_xpath("//android.widget.TextView[@text='我']").click()  # 进入 "我"
        count = int(self.driver.find_element_by_id("com.ss.android.ugc.aweme:id/a3f").get_attribute("text"))
        print(count)
        self.driver.find_element_by_id("com.ss.android.ugc.aweme:id/a3f").click()

        i = 0  # 计数
        repetition_time = 0

        while count > i:
            try:
                # 遍历所有元素
                items = self.driver.find_elements_by_id("com.ss.android.ugc.aweme:id/amq")
                for line in items:
                    info = {}
                    name = line.get_attribute("text").replace("@", "")
                    # 进入个人主页 并后去信息
                    line.click()
                    try:
                        # 采集大V信息
                        info["name"] = self.driver.find_element_by_id("com.ss.android.ugc.aweme:id/yc").get_attribute(
                            "text")

                        if info["name"] == "已重置" :
                            self.driver.keyevent(4)
                            continue

                        if info["name"] in all_name:
                            repetition_time = repetition_time + 1
                            continue


                        try:
                            temp_string = self.driver.find_element_by_id("com.ss.android.ugc.aweme:id/yb").get_attribute(
                                "text")
                            info["douyinID"] = temp_string.split(":")[1]
                        except:
                            pass
                        info["fans"] = self.driver.find_element_by_id("com.ss.android.ugc.aweme:id/a3h").get_attribute(
                            "text")
                        info["des"] = self.driver.find_element_by_id("com.ss.android.ugc.aweme:id/a35").get_attribute(
                            "text")

                        # 写入信息
                        print(str(info))
                        f.write(str(info) + "\n")

                        # 判断是否要继续获取
                        fans_num = float(info["fans"].replace("w", ""))

                        i = i + 1
                        repetition_time = 0

                        if "w" in info["fans"] and "重置" not in info["name"] and fans_num > 5:
                            # 获取二维码图片
                            self.driver.find_element_by_id("com.ss.android.ugc.aweme:id/a7b").click()
                            self.driver.find_element_by_xpath("//android.widget.TextView[@text='分享个人名片']").click()
                            self.driver.find_element_by_id("com.ss.android.ugc.aweme:id/oo").click()
                            self.driver.find_element_by_id("com.ss.android.ugc.aweme:id/xg").click()   # 点击下载截图
                            time.sleep(1)
                            os.system("adb shell input tap 300 700 ")
                            os.system("adb shell input tap 600 1716 ")
                            #self.driver.find_element_by_id("com.ss.android.ugc.aweme:id/kg").click()   # 点击取消
                            self.driver.find_element_by_id("com.ss.android.ugc.aweme:id/is").click()   # 返回列表

                        else:
                            self.driver.keyevent(4)
                            continue

                    except Exception as erro:
                        print("fuck3")
                        print(erro)
                        self.driver.keyevent(4)
                        continue


            except Exception as erro:
                print("fuck_mistake",erro)
                self.driver.keyevent(4)  # 返回

            if repetition_time > 20:
                print("already scan all douyinhao")
                break

            os.system("adb shell input swipe 500 1400 500 600")


    # 在视频播放页 获取视频链接
    def getVideoInfo(self):
        """
        link: 视频分享链接
        des: 视频描述
        des_md5: 视频描述md5 值

        :return:
        """


        time.sleep(2)
        # self.driver.find_element_by_id("com.ss.android.ugc.aweme:id/ala").click()
        os.system("adb shell input tap 988 1273")
        time.sleep(2)
        self.driver.swipe(964, 1510, 166, 1510)  # 滑出链接按钮

        # 从剪切板获取分享链接
        os.system("adb shell input tap 948 1428")
        # self.driver.find_element_by_xpath("//android.widget.HorizontalScrollView/android.widget.LinearLayout[6]").click()
        os.system("adb shell  am startservice ca.zgrs.clipper/.ClipboardService ")
        os.system("adb shell am broadcast -a clipper.get ")
        cmd = "adb shell  am startservice ca.zgrs.clipper/.ClipboardService ;adb shell am broadcast -a clipper.get "
        res = os.popen(cmd)
        video_info = {}
        for line in res.readlines():
            print(line)
            if "data" in line:
                video_info["link"] = self.tools.getLinkFromText(line)
                video_info["des"] = self.tools.getDesFromText(line)
                video_info["des_md5"] = self.tools.getTxtMD5(video_info["des"])
        return video_info

    # 搜索页
    def searchByID(self, ID):

        self.driver.find_element_by_id("com.ss.android.ugc.aweme:id/a9k").click()  # 从首页进入搜索页
        self.driver.find_element_by_id("com.ss.android.ugc.aweme:id/a1x").send_keys(ID)
        self.driver.find_element_by_id("com.ss.android.ugc.aweme:id/a1z").click()
        self.driver.find_elements_by_android_uiautomator('text(\"用户\")')[0].click()
        time.sleep(3)
        self.driver.find_element_by_id("com.ss.android.ugc.aweme:id/ati").click()     # 点击搜索结果链接进入

        # 获取作品数
        count = int(self.driver.find_element_by_id('com.ss.android.ugc.aweme:id/bc').text.split(" ")[1])
        print(count)
        if count == 0 :
            print("没有作品")
            self.driver.keyevent(4)   # 返回搜索页
            return "null"
        if count > 0:

            ele_first = self.driver.find_elements_by_id("com.ss.android.ugc.aweme:id/agr")[0]
            ele_first.click()

            i = 0
            while i < count:
               # print(self.driver.page_source)
                info = self.getVideoInfo()
                info["ID"] = ID
                self.tools.writeToFile(str(info), "LinkInfo")    # 写入文件
                self.driver.swipe(600,1300,600,800)
                i = i + 1

            # 返回搜索页
            self.driver.keyevent(4)
            self.driver.keyevent(4)



    # 从手机中获取截图
class PullFileFromPhone():
    def __int__(self):
        pass

    def getPicFromPhone(self):

        # 创建存放图片文件夹
        qr_path = os.path.join(os.getcwd(), "QR_CODE_PIC")
        if not os.path.exists(qr_path):
            os.mkdir(qr_path)
        # 拉去文件
        pic_name = "/sdcard/DCIM/Camera/"
        cmd_pull_pic = "adb pull " + pic_name + " " + qr_path
        os.system(cmd_pull_pic)



if __name__ == '__main__':
    action = Action()
    action.getDouyinHaoSharePic()
