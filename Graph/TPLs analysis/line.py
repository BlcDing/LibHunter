import pymysql
from pyecharts import options as opts
from pyecharts.charts import Line, Grid
from pyecharts.render import make_snapshot
from snapshot_selenium import snapshot


def get_db_connection() -> pymysql.Connection:
    host = "***"
    port = "***"
    user = "***"
    password = "***"
    database = "***"
    db_connection = pymysql.connect(host=host, port=port, user=user, password=password, database=database)
    return db_connection


def get_lib():
    with open("lib_manual.txt", "r") as f:
        lib_list = f.read().split("\n")
    return lib_list


def get_not_in_literadar():
    with open("not_in_literadar.txt", "r") as f:
        lib_list = f.read().split("\n")
    return lib_list


def get_not_in_public():
    with open("not_in_public.txt", "r") as f:
        lib_list = f.read().split("\n")
    return lib_list


def get_http_message():
    db_connection = get_db_connection()
    db_cursor = db_connection.cursor(pymysql.cursors.DictCursor)
    select_sql = "select APKName, stack from HTTP"
    db_cursor.execute(select_sql)
    http_message_dict = db_cursor.fetchall()
    print("select done")
    db_connection.close()

    # 我们找到的libradar没找到的, 每一个lib对应的apk
    lib_apk = dict()
    # 我们找到的公开仓库没有的，每一个lib对应的apk
    public_apk = dict()
    # 所有我们找到的
    lib_manual_apk = dict()

    literadar_list = get_not_in_literadar()
    public_list = get_not_in_public()
    lib_list = get_lib()

    for http_message in http_message_dict:
        if http_message["stack"] is None:
            continue
        if "None" in http_message["stack"]:
            continue

        for lib in literadar_list:
            if lib in http_message["stack"]:
                if lib not in lib_apk:
                    lib_apk[lib] = set()
                lib_apk[lib].add(http_message["APKName"])
        for lib in public_list:
            if lib in http_message["stack"]:
                if lib not in public_apk:
                    public_apk[lib] = set()
                public_apk[lib].add(http_message["APKName"])
        for lib in lib_list:
            if lib in http_message["stack"]:
                if lib not in lib_manual_apk:
                    lib_manual_apk[lib] = set()
                lib_manual_apk[lib].add(http_message["APKName"])
    return lib_apk, public_apk, lib_manual_apk


def return_index_1(x):
    return x[1]


if __name__ == '__main__':
    # data1 = list()
    # data2 = list()
    # data3 = list()
    # data4 = list()

    # lib_apk, public_apk, lib_manual_apk = get_http_message()
    # for lib, apk in lib_apk.items():
    #     data1.append([lib, len(apk)])
    
    # for public, apk in public_apk.items():
    #     data2.append([public, len(apk)])

    # for lib, apk in lib_manual_apk.items():
    #     data3.append([lib, len(apk)])

    # for lib, apk in lib_manual_apk.items():
    #     data4.append(len(apk))
    # print(sum(data4))

    # data1.sort(key=return_index_1, reverse=True)
    # data2.sort(key=return_index_1, reverse=True)
    # data3.sort(key=return_index_1, reverse=True)

    # with open("result1.txt", "w") as f:
    #     for x in data1[:20]:
    #         f.write(str(x))
    #         f.write("\n")
    
    # with open("result2.txt", "w") as f:
    #     for x in data2[:20]:
    #         f.write(str(x))
    #         f.write("\n")
    
    # with open("result3.txt", "w") as f:
    #     for x in data3[:20]:
    #         f.write(str(x))
    #         f.write("\n")
    
    # y1_data = [x[1] for x in data1[:20]]
    # y2_data = [x[1] for x in data2[:20]]
    # y3_data = [x[1] for x in data3[:20]]

    # print(y1_data)
    # print(y2_data)
    # print(y3_data)

    # x_data = [x for x in range(21)]
    # s1_data = [sum(y1_data[:x]) for x in range(1, 20)]
    # s1_data.append(sum(y1_data))
    # s2_data = [sum(y2_data[:x]) for x in range(1, 20)]
    # s2_data.append(sum(y2_data))
    # s3_data = [sum(y3_data[:x]) for x in range(1, 20)]
    # s3_data.append(sum(y3_data))

    # print(x_data)
    # print(s1_data)
    # print(s2_data)
    # print(s3_data)


    x_data = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    s1_data = [0, 84, 128, 160, 169, 175, 181, 185, 188, 191, 193, 195, 197, 199, 201, 202, 203, 204, 205, 206, 207]
    s2_data = [0, 71, 103, 127, 145, 154, 160, 164, 167, 169, 171, 173, 174, 175, 176, 177, 178, 179, 180, 181, 182]
    s3_data = [0, 84, 155, 214, 260, 304, 344, 376, 400, 418, 427, 436, 443, 449, 455, 461, 465, 469, 472, 475, 477]
    s1_data = [round(x/514,2) for x in s1_data[:11]]
    s2_data = [round(x/514,2) for x in s2_data[:11]]
    s3_data = [round(x/514,2) for x in s3_data[:11]]
    
    grid = Grid(init_opts=opts.InitOpts(width="800px", height="600px"))

    line = (
        Line()
        .set_colors(["#DC143C", "#234488", "#303030"])
        .add_xaxis(x_data)
        .add_yaxis(
            "newly-emerged TPLs", s1_data, is_smooth=True, is_symbol_show=False,
            linestyle_opts=opts.LineStyleOpts(
                width=4,
            )
        )
        .add_yaxis(
            "non-public available TPLs", s2_data, is_smooth=True, is_symbol_show=False,
            linestyle_opts=opts.LineStyleOpts(
                width=4,
            )
        )
        .add_yaxis(
            "total detected TPLs", s3_data, is_smooth=True, is_symbol_show=False,
            linestyle_opts=opts.LineStyleOpts(
                width=4,
            )
        )
        .set_global_opts(
            xaxis_opts=opts.AxisOpts(
                name="TPL number",
                type_="value",
                split_number=20,
                min_interval=1,
                name_location="center",
                name_gap=40,
                axislabel_opts=opts.LabelOpts(
                    interval=40,
                    is_show=True,
                    font_size=16,
                ),
                name_textstyle_opts=opts.TextStyleOpts(
                    font_size=20,
                ),
            ),
            yaxis_opts=opts.AxisOpts(
                max_=1,
                name="App number percentage",
                name_location="center",
                type_="value",
                name_gap=60,
                # is_scale=True,
                axislabel_opts=opts.LabelOpts(
                    interval=40,
                    is_show=True,
                    font_size=16,
                ),
                name_textstyle_opts=opts.TextStyleOpts(
                    font_size=20,
                ),
                splitline_opts=opts.SplitLineOpts(
                    is_show=True,
                    linestyle_opts=opts.LineStyleOpts(
                        width=2,
                    )
                )
            ),
            legend_opts=opts.LegendOpts(
                pos_top="4%",
                pos_left="55%",
                orient="vertical",
                # item_width=1,
                item_height=4,
                legend_icon="rect",
                textstyle_opts=opts.TextStyleOpts(
                    font_size=20,
                )
            )
        )
        .set_series_opts(
            label_opts=opts.LabelOpts(is_show=False),
        )
        # .render()
    )
    grid.add(line, grid_opts=opts.GridOpts(pos_bottom="20%", pos_left="20%", pos_top="20%"))
    grid.render("line.html")
    # make_snapshot(snapshot, grid.render(), "line.png")

