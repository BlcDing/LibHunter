from turtle import width
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
                    lib_apk[lib] = 0
                lib_apk[lib] += 1
        for lib in public_list:
            if lib in http_message["stack"]:
                if lib not in public_apk:
                    public_apk[lib] = 0
                public_apk[lib] += 1
        for lib in lib_list:
            if lib in http_message["stack"]:
                if lib not in lib_manual_apk:
                    lib_manual_apk[lib] = 0
                lib_manual_apk[lib] += 1
    return lib_apk, public_apk, lib_manual_apk


def return_index_1(x):
    return x[1]


if __name__ == '__main__':
    # data1 = list()
    # data2 = list()
    # data3 = list()
    # data4 = list()

    # lib_apk, public_apk, lib_manual_apk = get_http_message()
    # for lib, count in lib_apk.items():
    #     data1.append([lib, count])
    
    # for public, count in public_apk.items():
    #     data2.append([public, count])

    # for lib, count in lib_manual_apk.items():
    #     data3.append([lib, count])
    #     data4.append(count)
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
    s1_data = [0, 2292, 3538, 3901, 4012, 4052, 4078, 4102, 4118, 4133, 4148, 4161, 4172, 4182, 4189, 4194, 4198, 4202, 4205, 4208, 4211]
    s2_data = [0, 616, 787, 898, 984, 1024, 1057, 1083, 1099, 1114, 1127, 1138, 1145, 1149, 1152, 1155, 1158, 1161, 1163, 1165, 1167]
    s3_data = [0, 2292, 3538, 4154, 4517, 4841, 5012, 5124, 5236, 5347, 5433, 5493, 5533, 5566, 5599, 5625, 5649, 5665, 5680, 5695, 5708]
    s1_data = [round(x/5805,2) for x in s1_data[:11]]
    s2_data = [round(x/5805,2) for x in s2_data[:11]]
    s3_data = [round(x/5805,2) for x in s3_data[:11]]
    
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
                name="Request number percentage",
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

