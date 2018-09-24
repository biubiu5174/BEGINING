import os

DOUYINHAO_SHARE_URL = os.path.join(os.path.abspath(os.path.join(os.getcwd(), "..")),"DOUYINHAO_SHARE_URL")

f = open(DOUYINHAO_SHARE_URL,"r")
for line in f.readlines():
    if len(line) > 10:
        line.replace("\n","")
        print(line)
        p = os.popen("python3 amemv-video-ripper.py %s"  %line)
        x =p.read()
        print(x)


