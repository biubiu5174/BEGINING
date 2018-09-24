import os
import GetInfoFromDevice
import GetIDShareLink
import CombineInfo


if __name__ == "__main__":

    """
    # 先获取最新的截图
    getInfoFromDev = GetInfoFromDevice.Action()
    getInfoFromDev.getDouyinHaoSharePic()
    
   

    # 拉取截图
    pull = GetInfoFromDevice.PullFileFromPhone()
    pull.getPicFromPhone()

    # 生成url到 DOUYINHAO_SHARE_URL
    getIDShareLink = GetIDShareLink.getLinkFromFile()
    getIDShareLink.getShareLink()
    
     """

    # 获取完整信息
    combine = CombineInfo.GetInfoByConID()
    combine.CombineInfo()






