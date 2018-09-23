# -*- coding:utf-8 -*-
# Author: Z.W.
from splinter.driver.webdriver.chrome import Options, Chrome
from splinter.browser import Browser
from contextlib import closing
import requests, json, time, re, os, sys, datetime
from bs4 import BeautifulSoup
import argparse
import random
from Tools import Tools


class LemonLemon_douyin(object):

    def __init__(self, width=500, height=300):
        """
        抖音App视频下载
        """
        # 无头浏览器
        chrome_options = Options()
        chrome_options.add_argument(
            'user-agent="Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36"'
        )
        self.driver = Browser(
            driver_name="chrome", options=chrome_options, headless=True
        )

        self.tool = Tools()

    def get_video_urls(self, input_f):
        """
        获得视频播放地址
        Parameters:
            user_id：查询的用户ID
        Returns:
            video_names: 视频名字列表
            video_urls: 视频链接列表
            nickname: 用户昵称
        """
        video_names = []
        video_urls = []
        i = 1
        now_date = datetime.datetime.now()
        self.date_today = (
            str(now_date.date()) + "_" + str(now_date.hour) + ":" + str(now_date.minute)
        )

        with open(input_f) as f:
            for line in f:
                info = eval(line)
                ID = info["ID"]
                des_md5 = info["des_md5"]
                url = info["link"]
                video_urls.append(url)
                video_names.append(ID + "_" + des_md5 + ".mp4")
                i += 1

        return video_names, video_urls  # video_names, video_urls, nickname

    def get_download_url(self, video_url):
        """
        获得带水印的视频播放地址
        Parameters:
            video_url：带水印的视频播放地址
        Returns:
            download_url: 带水印的视频下载地址
        """
        req = requests.get(url=video_url, verify=False)
        bf = BeautifulSoup(req.text, "lxml")
        script = bf.find_all("script")[-1]
        video_url_js = re.findall("var data = \[(.+)\];", str(script))[0]
        video_html = json.loads(video_url_js)
        download_url = video_html["video"]["play_addr"]["url_list"][0]
        return download_url

    def video_downloader(self, video_url, video_name, watermark_flag=True):
        """
        视频下载
        Parameters:
            video_url: 带水印的视频地址
            video_name: 视频名
            watermark_flag: 是否下载不带水印的视频

        """
        size = 0
        if watermark_flag == True:
            video_url = self.remove_watermark(video_url)
        else:
            video_url = self.get_download_url(video_url)
        with closing(requests.get(video_url, stream=True, verify=False)) as response:
            chunk_size = 1024
            content_size = int(response.headers["content-length"])
            if response.status_code == 200:
                sys.stdout.write(
                    "  [文件大小]:%0.2f MB\n" % (content_size / chunk_size / 1024)
                )

                with open(video_name, "wb") as file:
                    for data in response.iter_content(chunk_size=chunk_size):
                        file.write(data)
                        size += len(data)
                        file.flush()

                        sys.stdout.write(
                            "  [下载进度]:%.2f%%" % float(size / content_size * 100) + "\r"
                        )
                        sys.stdout.flush()

    def remove_watermark(self, video_url):
        """
        获得无水印的视频播放地址
        Parameters:
            video_url: 带水印的视频地址
        Returns:
            无水印的视频下载地址
        """
        self.driver.visit("http://douyin.iiilab.com/")
        self.driver.find_by_tag("input").fill(video_url)
        self.driver.find_by_xpath('//button[@class="btn btn-default"]').click()
        html = self.driver.find_by_xpath('//div[@class="thumbnail"]/div/p')[0].html
        bf = BeautifulSoup(html, "lxml")
        return bf.find("a").get("href")

    def run(self, input_f):
        """
        运行函数
        Parameters:
            None
        Returns:
            None
        """
        # self.hello()
        # user_id = input('请输入ID(例如40103580):')
        error_url = []
        video_names, video_urls = self.get_video_urls(input_f)

        file = os.path.join(os.path.abspath(os.path.dirname(os.getcwd())),"DOWNLOAD")

        if not os.path.exists(file):
            os.mkdir(file)

        print("视频下载中:共有%d个作品!\n" % len(video_urls))
        for num in range(len(video_urls)):
            print("  解析第%d个视频链接 [%s] 中，请稍后!\n" % (num + 1, video_urls[num]))
            random_wait = random.uniform(3, 5)
            print("waiting...", random_wait)
            time.sleep(random_wait)

            """
            if "\\" in video_names[num]:
                video_name = video_names[num].replace("\\", "")
            elif "/" in video_names[num]:
                video_name = video_names[num].replace("/", "")
            else:
                video_name = video_names[num]
            """
            video_name = video_names[num]
            ID = video_name.split("_")[0]

            # 判断文件夹是否存在
            if  ID not in os.listdir(file):
                os.mkdir(os.path.join(file,ID))

            # 判断要下载的文件是否存在

            video_file = os.path.join(file ,ID, video_name)
            if not os.path.exists(video_file):
                try:

                    self.video_downloader(
                        video_urls[num],
                        os.path.join(file ,ID, video_name),
                    )

                    self.tool.writeToFile(video_name,"SuccessDownload")

                except:
                    print("**************************")
                    print("ERROR", video_urls[num])
                    error_url.append(video_urls[num])
                print("\n")
            else:
                print(video_name + "文件已存在")

        #self.driver.close()
        with open("error_url.txt", "w") as f:
            f = error_url
        print("下载完成!")

        print("出错数量：", len(error_url))






#

if __name__ == "__main__":
    # Parsing args
    parser = argparse.ArgumentParser(description="Please state dowload list file")
    parser.add_argument("input_file", help="path to input file")
    args = parser.parse_args()
    douyin = LemonLemon_douyin()
    douyin.run(args.input_file)
