from urllib import request
import re
import socket
import time
import urllib.request
import os
from random import randint

socket.setdefaulttimeout(20)

class class_360:
    def __init__(self):
        self.urllist = []
        # self.baseurl = 'http://zhushou.360.cn/list/index/cid/{}/?page='.format(category)


    def spider(self):
        category_Dict = {'11': '系统安全', '12': '通讯社交', '14': '影音视听', '15': '新闻阅读', '16': '生活休闲',
                         '18': '主题壁纸', '17': '办公商务', '102228': '摄影摄像', '102230': '购物优惠', '102231': '地图旅游',
                         '102232': '教育学习', '102139': '金融理财', '102233': '健康医疗'}
        packageTypeDict = {}
        # category_list = [11, 12, 14, 15, 16, 18, 17, 102228, 102230, 102231, 102232, 102139, 102233]
        # header = {'User-Agent': 'Mozilla/5.0 (Linux; Android 4.4.2; Nexus 4 Build/KOT49H) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.114 Mobile Safari/537.36'}
        USER_AGENTS = [
            "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; AcooBrowser; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
            "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; Acoo Browser; SLCC1; .NET CLR 2.0.50727; Media Center PC 5.0; .NET CLR 3.0.04506)",
            "Mozilla/4.0 (compatible; MSIE 7.0; AOL 9.5; AOLBuild 4337.35; Windows NT 5.1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
            "Mozilla/5.0 (Windows; U; MSIE 9.0; Windows NT 9.0; en-US)",
            "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 2.0.50727; Media Center PC 6.0)",
            "Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 1.0.3705; .NET CLR 1.1.4322)",
            "Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 5.2; .NET CLR 1.1.4322; .NET CLR 2.0.50727; InfoPath.2; .NET CLR 3.0.04506.30)",
            "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN) AppleWebKit/523.15 (KHTML, like Gecko, Safari/419.3) Arora/0.3 (Change: 287 c9dfb30)",
            "Mozilla/5.0 (X11; U; Linux; en-US) AppleWebKit/527+ (KHTML, like Gecko, Safari/419.3) Arora/0.6",
            "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.2pre) Gecko/20070215 K-Ninja/2.1.1",
            "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9) Gecko/20080705 Firefox/3.0 Kapiko/3.0",
            "Mozilla/5.0 (X11; Linux i686; U;) Gecko/20070322 Kazehakase/0.4.5",
            "Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.8) Gecko Fedora/1.9.0.8-1.fc10 Kazehakase/0.5.6",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3) AppleWebKit/535.20 (KHTML, like Gecko) Chrome/19.0.1036.7 Safari/535.20",
            "Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; fr) Presto/2.9.168 Version/11.52",
        ]

        random_agent = USER_AGENTS[randint(0, len(USER_AGENTS)-1)]
        header = {
            'User-Agent': random_agent,
        }

        for key, value in category_Dict.items():
            baseurl = 'http://zhushou.360.cn/list/index/cid/{}/?page='.format(key)
            for i in range(1, 51):
                url = baseurl + str(i)
                try:
                    request = urllib.request.Request(url, headers=header)
                    '''proxy = {'http': '106.46.136.112:808'}
                    proxy_support = urllib.request.ProxyHandler(proxy)
                    opener = urllib.request.build_opener(proxy_support)
                    opener.addheaders = [('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36')]
                    urllib.request.install_opener(opener)'''
                    response = urllib.request.urlopen(request)
                    html = str(response.read())
                    response.close()
                    sid_list = re.findall(r'(?<=/detail/index/soft_id/).*?"', html)
                    sid_list_set = set(sid_list)
                    for sid in sid_list_set:
                        real_url = 'http://zhushou.360.cn/detail/index/soft_id/' + str(sid)
                        try:
                            real_request = urllib.request.Request(real_url, headers=header)
                            real_response = urllib.request.urlopen(real_request)
                            # response = urllib.request.urlopen(url, timeout=30)
                            real_html = str(real_response.read())
                            # print(real_html)
                            pname_tmp = str(real_html).split("\\'pname\\': \"", 1)[1]
                            pname = pname_tmp.split('",', 1)[0]
                            packageTypeDict.update({pname: value})
                            print(str({pname: value}) + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
                            real_response.close()
                        except urllib.error.URLError as e:
                            print(e)
                        time.sleep(1)
                except urllib.error.URLError as e:
                    print(e)
                time.sleep(1)

        txtPath = 'G:\\Chrome downloads\\APKTestEngine-master\\APKTestEngine-master\\Spiders\\'
        os.chdir(txtPath)
        with open('360Type.txt', 'w+', encoding='utf-8') as f:
            for packagename, type in packageTypeDict.items():
                f.write(str(packagename) + ': ' + str(type))
                f.write("\r\n")
        print('finished!!!!!!!!!!!!!!!!!!!!!!')
        print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))



    def start(self):
        self.spider()
        # print("spider success")

if __name__ == '__main__':

    a = class_360()
    a.start()
