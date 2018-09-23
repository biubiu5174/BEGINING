#coding = utf-8
import pymysql
import Tools


class Pysql(object):
    def __init__(self):
        self.get_conn()
        self.tools = Tools.Tools


    def get_conn(self):
        try:
            self.a = 1
            self.conn = pymysql.connect(
                host='localhost',
                port=3306,
                user='www',
                password='didi',
                charset='utf8',
                database='DOUYIN'
            )
        except pymysql.Error as e:
            print(e)


    def close_conn(self):
        try:
            if self.conn:
                self.conn.close()
        except pymysql.Error as e:
            print(e)


    def exec_sql(self,sql):
        """
        :return: 获取数据库中的一条数据返回这条数据的title字段
        """

        # 获取cursor
        cursor = self.conn.cursor()
        try:
            # 执行sql
            cursor.execute(sql)
            self.conn.commit()
        except:
            self.conn.rollback()
            print("sql erro")


        # 关闭cursor/连接
        #cursor.close()
        #self.close_conn()

    def build_table(self):
        self.build_douyinhao_table_sql = """
        CREATE TABLE DOUYINHAO (
             douyinID  VARCHAR(50) NOT NULL,
             ID_name VARCHAR(100),
             ID_des VARCHAR(1000),
             ID_fans VARCHAR(10),
             tag  VARCHAR(100),
             share_url VARCHAR(100)
              )  DEFAULT CHARSET=utf8;
        """

        self.build_video_table_sql ="""
        CREATE TABLE VIDEO (
             video_name  VARCHAR(50) NOT NULL,
             douyinID VARCHAR(100),
             is_used INT,
             video_des VARCHAR(10)
              )  DEFAULT CHARSET=utf8;
        """
        self.exec_sql(self.build_douyinhao_table_sql)
        #self.exec_sql(self.build_video_table_sql)

    # 写入DOUYINHAO
    def insert_douyinhao(self,douyinID,ID_name,ID_des,ID_fans):
        sql = """
        INSERT INTO DOUYINHAO (douyinID,ID_name,ID_des,ID_fans)
        VALUES ("%s","%s","%s","%s") ;""" % (douyinID,ID_name,ID_des,ID_fans)
        print(sql)

        self.exec_sql(sql)


    def inert_video(self,video_name,douyinID,is_used,video_des):
        sql = """
        INSERT INTO VIDEO (video_name,douyinID,is_used,video_des)
        VALUES ("%s","%s","%d","%s") ; """ % (video_name,douyinID,is_used,video_des)

        self.exec_sql(sql)


    def get_qualified_ID(self):
        """
        从痘DouyinHao  净化 抖音号内容
        A、去重
        B、按照条件筛选写入数据库
        :return:
        """
        f = open("temp", "r")
        for line in f.readlines():
            try:
                name = self.tools.remove_emoji(eval(line)["name"])
                fans = eval(line)["fans"]
                fans_num = float(fans.replace("w", ""))
                douyinID = eval(line)["douyinID"]
                des = self.tools.remove_emoji(eval(line)["des"])

                # 判断是否满足条件
                if "w" in fans and fans_num > 10 and "重置" not in name :

                    # 写入数据库
                    self.insert_douyinhao(douyinID, name, des, fans)


            except Exception as erro:
                print(erro)
                continue


if __name__ == '__main__':
    pysql = Pysql()
    pysql.get_qualified_ID()
    #pysql.insert_douyinhao("hahah","1221","1231","123吧的吧大师傅")

