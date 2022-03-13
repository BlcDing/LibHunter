# 生成lib_list.txt

import pymysql  # pip install pymysql


def get_db_connection() -> pymysql.Connection:
    host = "***"
    port = "***"
    user = "***"
    password = "***"
    database = "***"
    db_connection = pymysql.connect(host=host, port=port, user=user, password=password, database=database)
    return db_connection


def execute_sql():
    db_connection = get_db_connection()
    db_cursor = db_connection.cursor(pymysql.cursors.DictCursor)
    select_sql = "select stack from HTTP"
    db_cursor.execute(select_sql)
    stack_list = db_cursor.fetchall()
    print("select done")

    new_stack = set()

    for http_message in stack_list:
        if http_message["stack"] is None:
            continue
        # print(http_message["stack"])
        stack = http_message["stack"].split("|")
        for tmp in stack[::1]:
            if str(tmp).startswith("java") \
                    or str(tmp).startswith("at com.android.okhttp") \
                    or str(tmp).startswith("at org.apache.http") \
                    or str(tmp).startswith("at okio") \
                    or str(tmp).startswith("at okhttp3") \
                    or str(tmp).startswith("at com.android.org") \
                    or str(tmp).startswith("at android.os") \
                    or str(tmp).startswith("at java") \
                    or str(tmp).startswith("at com.android.volley") \
                    or "retrofit2" in str(tmp) \
                    or "reactivex" in str(tmp) \
                    or "intercept" in str(tmp) \
                    or "None" in str(tmp):
                del stack[stack.index(tmp)]
        
        for tmp in stack:
            tmp = tmp.replace("at ", "").split("(")[0]
            if len(tmp.split(".")) > 0 and "$" in tmp.split(".")[0]:
                continue
            if len(tmp.split(".")) > 1 and "$" in tmp.split(".")[1]:
                continue
            if len(tmp.split(".")) > 2 and "$" in tmp.split(".")[2]:
                continue
            if len(tmp.split(".")) > 0 and len(tmp.split(".")[0]) == 1:
                continue
            if len(tmp.split(".")) > 1 and len(tmp.split(".")[1]) == 1:
                continue
            if len(tmp.split(".")) > 2 and len(tmp.split(".")[2]) == 1:
                continue
            if len(tmp.split(".")) > 3:
                tmp = ".".join(tmp.split(".")[:3])
            new_stack.add(tmp)
    
    with open("lib_list.txt", "w") as f:
        new_stack = list(new_stack)
        # new_stack.sort(key=str.lower, reverse=False)
        # new_stack.sort(key = lambda i:len(i), reverse=False)
        for stack in new_stack:
            f.write(stack)
            f.write("\n")


    db_connection.close()


if __name__ == "__main__":
    execute_sql()
