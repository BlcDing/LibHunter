import re
import urllib.request
import os
import platform
import pathlib


category_name_dict = {
    "11": "system",  # 系统安全
    "12": "communication",  # 通讯社交
    "14": "media",  # 影音视听
    "15": "news",  # 新闻阅读
    "16": "life",  # 生活休闲
    "18": "themes",  # 主题壁纸
    "17": "business",  # 办公商务
    "102228": "photography",  # 摄影摄像
    "102230": "shopping",  # 购物优惠
    "102231": "travel",  # 地图旅游
    "102232": "education",  # 教育学习
    "102139": "finance",  # 金融理财
    "102233": "health",  # 健康医疗
}


class class_360:
    def __init__(self,category):
        self.urllist = []
        self.baseurl = "http://zhushou.360.cn/list/index/cid/{}/?page=".format(category)

    def geturl(self, pageindex):
        for i in range(1, pageindex):
            self.urllist.append(self.baseurl+str(i))

    def spider(self):
        for i in range(len(self.urllist)):
            response = urllib.request.urlopen(self.urllist[i])
            html = str(response.read())
            link_list = re.findall(r'(?<=&url=).*?apk"', html)
            for url in link_list:
                try:
                    url = url[:-1]
                    file_name = url.split("?")[0].split("/")[-1]
                    file_path = "/".join([".", category_name, file_name])
                    print(file_path)
                    if os.path.exists(file_path):
                        print("apk exists")
                        continue
                    urllib.request.urlretrieve(url, file_path)
                    print("downloading success")
                except Exception as e:
                    print("download failed")
                    continue

    def start(self):
        self.geturl(50)
        self.spider()


if __name__ == "__main__":
    load_path = "./360APPStore/"
    path = pathlib.Path(load_path)
    if not path.exists():
        path.mkdir()
    os.chdir(load_path)
    for category, category_name in category_name_dict.items():
        # print(category_name)
        print("="*40 + category_name + "="*40)
        path = pathlib.Path(category_name)
        if not path.exists():
            path.mkdir()
        a = class_360(category)
        a.start()
