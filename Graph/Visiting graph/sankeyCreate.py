import pandas
import pymysql
from pyecharts import options as opts
from pyecharts.charts import Sankey
from pyecharts.render import make_snapshot
from snapshot_selenium import snapshot


def get_db_connection() -> pymysql.Connection:
    host = "10.10.103.147"
    port = 3306
    user = "root"
    password = "iiewlz666"
    database = "APKDB"
    db_connection = pymysql.connect(host=host, port=port, user=user, password=password, database=database)
    return db_connection


def get_lib():
    with open("lib_manual.txt", "r") as f:
        lib_list = f.read().split("\n")
    return lib_list


def get_http_message():
    db_connection = get_db_connection()
    db_cursor = db_connection.cursor(pymysql.cursors.DictCursor)
    select_sql = "select host, stack from HTTP"
    db_cursor.execute(select_sql)
    http_message_dict = db_cursor.fetchall()
    print("select done")
    db_connection.close()

    lib_list = get_lib()
    data = dict()

    for http_message in http_message_dict:
        if http_message["stack"] is None:
            continue
        if "None" in http_message["stack"]:
            continue
        
        host = http_message["host"].split(":")[0]
        if host.endswith("com.cn"):
            host = ".".join(host.split(".")[-3:])
        else:
            if len(host.split(".")) > 2:
                host = ".".join(host.split(".")[-2:])
        for lib in lib_list:
            if lib in http_message["stack"]:
                if lib not in data:
                    data[lib] = dict()
                if host not in data[lib]:
                    data[lib][host] = 0
                data[lib][host] += 1
    
    data_final = list()
    for lib in data.keys():
        for host, count in data[lib].items():
            data_final.append([lib, host, count])
    return data_final


# data_final = get_http_message()
# with open("result.txt", "w") as f:
#     for x in data_final:
#         f.write(str(x))
#         f.write("\n")

data_final = [
    ['com.alibaba.sdk', '1.65', 29],
    ['com.alibaba.sdk', 'funshion.com', 1],
    ['com.alibaba.sdk', 'aliyuncs.com', 25],
    ['com.alibaba.sdk', 'umeng.com', 6],
    ['com.alibaba.sdk', 'umsns.com', 1],
    ['com.alibaba.sdk', 'xqmob.com', 2],
    ['com.alibaba.sdk', '1.1', 13],
    ['com.alibaba.sdk', 'ctobsnssdk.com', 4],
    ['com.alibaba.sdk', '234.145', 5],
    ['com.umeng.commonsdk', 'zhengzhaoxi.com', 1],
    ['com.umeng.commonsdk', 'meizu.com', 2],
    ['com.umeng.commonsdk', 'umeng.com', 80],
    ['com.umeng.commonsdk', 'funshion.com', 1],
    ['com.umeng.commonsdk', 'yximgs.com', 5],
    ['com.umeng.commonsdk', 'qq.com', 28],
    ['com.umeng.commonsdk', 'gdtimg.com', 2],
    ['com.umeng.commonsdk', 'oupeng.com', 1],
    ['com.umeng.commonsdk', 'ludashi.com', 3],
    ['com.umeng.commonsdk', 'snssdk.com', 3],
    ['com.umeng.commonsdk', 'jpush.cn', 3],
    ['com.umeng.commonsdk', 'unity3d.com', 2],
    ['com.umeng.commonsdk', 'hljetckc.cn', 1],
    ['com.umeng.commonsdk', 'com.hk', 1],
    ['com.umeng.commonsdk', 'flurry.com', 1],
    ['com.umeng.commonsdk', 'peake.com.cn', 3],
    ['com.umeng.commonsdk', 'cbcday.com', 1],
    ['com.umeng.commonsdk', 'mobkeeper.com', 1],
    ['com.umeng.commonsdk', 'baidu.com', 2],
    ['com.umeng.commonsdk', 'ctobsnssdk.com', 7],
    ['com.umeng.commonsdk', 'aliyuncs.com', 3],
    ['com.umeng.commonsdk', 'uc.cn', 2],
    ['com.umeng.commonsdk', '3gu.com', 2],
    ['com.umeng.commonsdk', 'shengyaoo.com', 1],
    ['com.umeng.commonsdk', 'wlanbanlv.com', 2],
    ['com.umeng.commonsdk', 'taobao.com', 3],
    ['com.umeng.commonsdk', 'qszzz.cn', 4],
    ['com.umeng.commonsdk', 'pstatp.com', 1],
    ['com.umeng.commonsdk', 'umsns.com', 1],
    ['com.umeng.commonsdk', 'amap.com', 1],
    ['com.umeng.commonsdk', 'gzsrun.cn', 1],
    ['com.umeng.commonsdk', 'xiaoyuanjijiehao.com', 1],
    ['com.umeng.commonsdk', 'fraudmetrix.cn', 1],
    ['com.baidu.ocr', 'umeng.com', 1],
    ['com.baidu.ocr', 'zhengzhaoxi.com', 1],
    ['com.uc.crashsdk', 'umeng.com', 31],
    ['com.uc.crashsdk', 'iflytek.com', 1],
    ['com.uc.crashsdk', 'saikr.com', 1],
    ['com.uc.crashsdk', 'funshion.com', 1],
    ['com.uc.crashsdk', 'qq.com', 30],
    ['com.uc.crashsdk', '2345cdn.net', 1],
    ['com.uc.crashsdk', 'amap.com', 4],
    ['com.uc.crashsdk', 'ucweb.com', 2],
    ['com.uc.crashsdk', 'alipay.com', 3],
    ['com.uc.crashsdk', 'gdtimg.com', 5],
    ['com.uc.crashsdk', 'sm.cn', 3],
    ['com.uc.crashsdk', 'uc.cn', 4],
    ['com.uc.crashsdk', 'mobkeeper.com', 1],
    ['com.uc.crashsdk', 'anythinktech.com', 4],
    ['com.uc.crashsdk', 'aliyun.com', 1],
    ['com.uc.crashsdk', 'zuimeitianqi.com', 2],
    ['com.uc.crashsdk', 'shengyaoo.com', 2],
    ['com.uc.crashsdk', 'taobao.com', 1],
    ['com.uc.crashsdk', 'jpush.cn', 3],
    ['com.uc.crashsdk', 'baidu.com', 1],
    ['com.uc.crashsdk', 'yungaoad.cn', 1],
    ['com.uc.crashsdk', 'ctobsnssdk.com', 2],
    ['com.uc.crashsdk', 'gifshow.com', 3],
    ['com.uc.crashsdk', 'cpatrk.net', 3],
    ['com.uc.crashsdk', '360.cn', 1],
    ['com.baidu.mobads', 'baidu.com', 160],
    ['com.baidu.mobads', 'qq.com', 64],
    ['com.baidu.mobads', 'kuaishou.com', 77],
    ['com.baidu.mobads', 'gdtimg.com', 3],
    ['com.baidu.mobads', 'ugdtimg.com', 4],
    ['com.baidu.mobads', 'baidustatic.com', 5],
    ['com.baidu.mobads', 'multiopen.cn', 1],
    ['com.baidu.mobads', 'appota.cn', 2],
    ['com.baidu.mobads', 'yximgs.com', 1],
    ['com.baidu.mobads', '360.cn', 1],
    ['com.baidu.mobads', 'amap.com', 1],
    ['com.baidu.mobads', 'umeng.com', 1],
    ['com.baidu.mobads', 'jpush.cn', 1],
    ['com.baidu.mobads', 'ucweb.com', 1],
    ['com.baidu.mobads', 'xdrig.com', 1],
    ['com.baidu.mobads', 'mediav.com', 1],
    ['com.kuaishou.weapon', 'baidu.com', 29],
    ['com.kuaishou.weapon', 'kuaishou.com', 197],
    ['com.kuaishou.weapon', 'aliyuncs.com', 2],
    ['com.kuaishou.weapon', 'umsns.com', 1],
    ['com.kuaishou.weapon', 'qq.com', 103],
    ['com.kuaishou.weapon', 'saikr.com', 7],
    ['com.kuaishou.weapon', 'yximgs.com', 139],
    ['com.kuaishou.weapon', 'weibo.com', 2],
    ['com.kuaishou.weapon', 'ctobsnssdk.com', 10],
    ['com.kuaishou.weapon', 'gifshow.com', 15],
    ['com.kuaishou.weapon', 'taobao.com', 3],
    ['com.kuaishou.weapon', 'kwimgs.com', 31],
    ['com.kuaishou.weapon', 'aliyun.com', 1],
    ['com.kuaishou.weapon', '2345.com', 1],
    ['com.kuaishou.weapon', 'snssdk.com', 14],
    ['com.kuaishou.weapon', 'umengcloud.com', 1],
    ['com.kuaishou.weapon', 'umeng.com', 7],
    ['com.kuaishou.weapon', 'avlyun.com', 1],
    ['com.kuaishou.weapon', '0.1', 4],
    ['com.kuaishou.weapon', '360.cn', 6],
    ['com.kuaishou.weapon', 'gdtimg.com', 9],
    ['com.kuaishou.weapon', 'yotu.cn', 3],
    ['com.kuaishou.weapon', 'kspkg.com', 2],
    ['com.kuaishou.weapon', 'sandai.net', 5],
    ['com.kuaishou.weapon', 'xiaohongshu.com', 1],
    ['com.kuaishou.weapon', 'pinduoduo.com', 3],
    ['com.kuaishou.weapon', 'soulapp.cn', 1],
    ['com.kuaishou.weapon', 'ttwanjia.com', 1],
    ['com.kuaishou.weapon', 'netease.com', 2],
    ['com.kuaishou.weapon', 'yungaoad.cn', 2],
    ['com.kuaishou.weapon', 'yilanvaas.com', 13],
    ['com.baidu.mobstat', 'umeng.com', 2],
    ['com.baidu.mobstat', 'baidu.com', 51],
    ['com.baidu.mobstat', 'jiaxunyun.com', 1],
    ['com.baidu.mobstat', 'taobao.com', 1],
    ['com.baidu.mobstat', 'bdstatic.com', 1],
    ['com.baidu.mobstat', 'cpatrk.net', 1],
    ['com.baidu.mobstat', 'ctobsnssdk.com', 2],
    ['com.baidu.mobstat', 'qq.com', 1],
    ['com.meizu.cloud', 'umeng.com', 1],
    ['com.meizu.cloud', 'meizu.com', 1],
    ['com.bytedance.sdk', 'ctobsnssdk.com', 99],
    ['com.bytedance.sdk', 'umeng.com', 44],
    ['com.bytedance.sdk', 'aliyun.com', 1],
    ['com.bytedance.sdk', 'qq.com', 124],
    ['com.bytedance.sdk', 'pglstatp-toutiao.com', 182],
    ['com.bytedance.sdk', 'yximgs.com', 31],
    ['com.bytedance.sdk', 'snssdk.com', 116],
    ['com.bytedance.sdk', 'uc.cn', 69],
    ['com.bytedance.sdk', 'toutiao.com', 8],
    ['com.bytedance.sdk', 'getui.net', 1],
    ['com.bytedance.sdk', 'yilanvaas.com', 29],
    ['com.bytedance.sdk', '2345cdn.net', 1],
    ['com.bytedance.sdk', '50bang.org', 190],
    ['com.bytedance.sdk', '2345.com', 13],
    ['com.bytedance.sdk', '360buyimg.com', 8],
    ['com.bytedance.sdk', 'zhimg.com', 1],
    ['com.bytedance.sdk', 'byteimg.com', 1],
    ['com.bytedance.sdk', 'taobao.com', 1],
    ['com.bytedance.sdk', 'kuaishou.com', 55],
    ['com.bytedance.sdk', 'gifshow.com', 7],
    ['com.bytedance.sdk', 'gdtimg.com', 28],
    ['com.bytedance.sdk', 'bytesmanager.com', 4],
    ['com.bytedance.sdk', 'mobo168.com', 6],
    ['com.bytedance.sdk', 'ugdtimg.com', 7],
    ['com.bytedance.sdk', 'amap.com', 7],
    ['com.bytedance.sdk', 'pstatp.com', 3],
    ['com.bytedance.sdk', '0.1', 2],
    ['com.bytedance.sdk', 'netduorou.com', 21],
    ['com.bytedance.sdk', 'x8zs.com', 19],
    ['com.bytedance.sdk', '9game.cn', 5],
    ['com.bytedance.sdk', 'aiqu.com', 5],
    ['com.bytedance.sdk', 'tsyule.cn', 1],
    ['com.bytedance.sdk', 'wakaifu.com', 5],
    ['com.bytedance.sdk', 'bytesfield.com', 3],
    ['com.bytedance.sdk', '168play.cn', 8],
    ['com.bytedance.sdk', 'umsns.com', 3],
    ['com.bytedance.sdk', '50union.com', 1],
    ['com.bytedance.sdk', 'anythinktech.com', 14],
    ['com.bytedance.sdk', 'baidustatic.com', 2],
    ['com.bytedance.sdk', 'baidu.com', 17],
    ['com.bytedance.sdk', 'ixigua.com', 1],
    ['com.bytedance.sdk', 'ugapk.cn', 1],
    ['com.bytedance.sdk', '360.cn', 15],
    ['com.bytedance.sdk', '1.1', 1],
    ['com.bytedance.sdk', 'iapple123.com', 1],
    ['com.bytedance.sdk', 'aliyuncs.com', 1],
    ['com.bytedance.sdk', 'yotu.cn', 4],
    ['com.bytedance.sdk', 'jd.com', 2],
    ['com.bytedance.sdk', 'coolapk.com', 22],
    ['com.bytedance.sdk', '1sapp.com', 12],
    ['com.bytedance.sdk', 'sinaimg.cn', 12],
    ['com.bytedance.sdk', 'gtimg.com', 6],
    ['com.bytedance.sdk', 'wlanbanlv.com', 6],
    ['com.bytedance.sdk', 'umengcloud.com', 3],
    ['com.bytedance.sdk', 'qszzz.cn', 1],
    ['com.bytedance.sdk', 'dftoutiao.com', 4],
    ['com.bytedance.sdk', 'bcebos.com', 1],
    ['com.bytedance.sdk', 'sm.cn', 4],
    ['com.bytedance.sdk', 'shuqireader.com', 1],
    ['com.bytedance.sdk', 'ucweb.com', 4],
    ['com.bytedance.sdk', 'uczzd.cn', 1],
    ['com.bytedance.sdk', 'bytedance.com', 1],
    ['com.mopub.volley', 'mopub.com', 10],
    ['com.tencent.bugly', 'qq.com', 92],
    ['com.tencent.bugly', 'amap.com', 1],
    ['com.tencent.bugly', 'avlyun.com', 4],
    ['com.tencent.bugly', 'anythinktech.com', 1],
    ['com.tencent.bugly', 'jd.com', 1],
    ['com.tencent.bugly', 'coolapk.com', 6],
    ['com.tencent.bugly', 'aliyuncs.com', 1],
    ['com.tencent.bugly', 'baidu.com', 1],
    ['com.tencent.bugly', 'snssdk.com', 1],
    ['com.tencent.bugly', 'xdaozwg.com', 1],
    ['com.tencent.bugly', 'gdtimg.com', 1],
    ['com.tencent.bugly', 'umeng.com', 1],
    ['com.tencent.bugly', '360.cn', 1],
    ['com.getui.gtc', 'igexin.com', 1],
    ['com.sensorsdata.analytics', '17k.com', 24],
    ['com.sensorsdata.analytics', 'yiyongcad.com', 1],
    ['com.sensorsdata.analytics', 'shoujihuifu.com', 1],
    ['cn.jiguang.jmlinksdk', 'jpush.cn', 1],
    ['com.igexin.push', 'igexin.com', 1],
    ['com.igexin.push', 'getui.com', 1],
    ['com.alipay.sdk', 'alipay.com', 4],
    ['com.alipay.sdk', 'umeng.com', 1],
    ['com.qihoo.sdk', '360.cn', 21],
    ['com.qihoo.sdk', 'so.com', 2],
    ['com.qihoo.sdk', 'adblockplus.org', 3],
    ['com.qihoo.sdk', 'qq.com', 3],
    ['com.qihoo.sdk', 'snssdk.com', 1],
    ['com.qihoo.sdk', 'yotu.cn', 1],
    ['com.qihoo.sdk', 'gifshow.com', 2],
    ['cn.jpush.android', 'jpush.cn', 6],
    ['cn.jpush.android', 'baidu.com', 1],
    ['com.amap.api', 'amap.com', 237],
    ['com.amap.api', 'autonavi.com', 121],
    ['com.amap.api', 'ucweb.com', 2],
    ['com.amap.api', 'ctobsnssdk.com', 1],
    ['com.amap.api', '1.1', 1],
    ['com.amap.api', 'yximgs.com', 1],
    ['com.tencent.connect', 'qq.com', 1],
    ['com.uc.sdk', 'uc.cn', 1],
    ['com.uc.sdk', 'amap.com', 1],
    ['com.uc.sdk', 'ucweb.com', 1],
    ['com.uc.sdk', 'taobao.com', 1],
    ['com.appsflyer.AppsFlyerLib', 'appsflyer.com', 9],
    ['com.appsflyer.AppsFlyerLib', 'yahoo.net', 1],
    ['com.appsflyer.AppsFlyerLib', 'batch.com', 2],
    ['com.appsflyer.AppsFlyerLib', 'tradeinterceptor.com', 1],
    ['com.appsflyer.AppsFlyerLib', 'lonlife.org', 2],
    ['com.appsflyer.AppsFlyerLib', '163yun.com', 1],
    ['com.flurry.sdk', 'startappservice.com', 2],
    ['com.flurry.sdk', 'flurry.com', 3],
    ['com.flurry.sdk', 'goguphone.com', 1],
    ['com.flurry.sdk', 'ahanet.net', 1],
    ['com.google.ads', 'flurry.com', 1],
    ['com.google.ads', 'doubleclick.net', 2],
    ['com.google.analytics', 'google-analytics.com', 30],
    ['com.google.analytics', 'startappservice.com', 1],
    ['com.google.analytics', 'flurry.com', 2],
    ['com.iflytek.cloud', 'openspeech.cn', 1],
    ['com.iflytek.cloud', 'voicecloud.cn', 13],
    ['com.iflytek.cloud', 'iflytek.com', 1],
    ['com.baidu.lbsapi', 'net.cn', 1],
    ['cn.magicwindow.common', 'mlinks.cc', 10],
    ['cn.magicwindow.common', 'amap.com', 1],
    ['cn.magicwindow.common', 'xdrig.com', 2],
    ['com.weibo.ssosdk', 'umeng.com', 1],
    ['com.weibo.ssosdk', 'meizu.com', 2],
    ['com.google.firebase', 'adjust.com', 3],
    ['com.adjust.sdk', 'adjust.com', 1],
    ['com.baidu.push', 'baidu.com', 3],
    ['com.anythink.core', 'mobkeeper.com', 3],
    ['com.anythink.core', 'ctobsnssdk.com', 2],
    ['com.anythink.core', 'anythinktech.com', 2],
    ['com.kwad.sdk', 'gifshow.com', 21],
    ['com.kwad.sdk', 'umeng.com', 5],
    ['com.kwad.sdk', '360.cn', 7],
    ['com.kwad.sdk', 'qhupdate.com', 2],
    ['com.kwad.sdk', 'yximgs.com', 4],
    ['com.kwad.sdk', 'snssdk.com', 1],
    ['com.baidu.tts', '33.8', 1],
    ['com.evernote.edam', 'evernote.com', 2],
    ['com.baidu.speech', 'baidu.com', 112],
    ['com.baidu.cyberplayer', 'baidu.com', 1],
    ['com.tencent.beacon', 'qq.com', 2],
    ['com.baidu.crabsdk', 'baidu.com', 2],
    ['com.baidu.techain', 'baidu.com', 2],
    ['com.huawei.hms', 'xdrig.com', 1],
    ['com.netease.mobsec', 'lonlife.org', 2],
    ['com.pgl.sys', 'snssdk.com', 2],
    ['com.facebook.ads', '0.1', 4],
    ['com.tapjoy.TapjoyURLConnection', 'tapjoyads.com', 4],
    ['com.tapjoy.TapjoyURLConnection', 'tapjoy.com', 4],
    ['com.tapjoy.TapjoyURLConnection', 'amazonaws.com', 6],
    ['com.tapjoy.TapjoyURLConnection', 'flurry.com', 1],
    ['com.alimama.tunion', 'sm.cn', 1],
    ['com.oppo.upgrade', 'oppo.com', 5],
    ['com.oppo.upgrade', 'nearme.com.cn', 6],
    ['com.sigmob.volley', 'xdrig.com', 1],
    ['com.sigmob.volley', 'uc.cn', 2],
]

for x in data_final[::1]:
    if x[2]<30:
        data_final.remove(x)
for x in data_final[::1]:
    if x[1] == "0.1":
        data_final.remove(x)
for x in data_final[::1]:
    if x[0] == "com.baidu.mobstat":
        data_final.remove(x)
data_frame = pandas.DataFrame(data_final, columns=['source', 'target', 'value'])

# 生成节点，先合并源节点和目标节点，然后去除重复的节点，最后输出成dict形式
nn = pandas.concat([data_frame['source'], data_frame['target']])
nn = nn.drop_duplicates()
nodes = pandas.DataFrame(nn, columns=['name']).to_dict(orient='records')

# 生成连接，dict形式
links = data_frame.to_dict(orient='records')

colors = [
    "#6f6f6f",
    "#303030",
    "#c8c8c8",
    "#aaaaaa",
    "#888888",
    "#444444"
]

sk =(
    # Sankey(init_opts=opts.InitOpts(width="2000px", height="1200px"))
    Sankey(init_opts=opts.InitOpts(width="800px", height="600px"))
    .set_colors(colors)
    .add(
        series_name="",
        nodes=nodes,
        links=links,
        linestyle_opt=opts.LineStyleOpts(opacity=0.2, curve=0.5, color="source"), 
        label_opts=opts.LabelOpts(font_size=20, position='right'),
        # node_align="left",
        # pos_left="30%",
        pos_right="30%",
        node_gap=18,
        layout_iterations=180,
    )
    .set_global_opts(title_opts=opts.TitleOpts(title=""))
    .render("sankey.html")
)

# make_snapshot(snapshot, sk.render(), "sankey.png")