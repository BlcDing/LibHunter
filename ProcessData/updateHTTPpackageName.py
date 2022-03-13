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
    select_sql = "select APKName, packageName from APKMetadata"
    db_cursor.execute(select_sql)
    apkmetadata_dict = db_cursor.fetchall()
    print("select done")

    select_sql = "SELECT id, packageName, four_tuple_hash, four_tuple_hash_re FROM HTTP"
    db_cursor.execute(select_sql)
    http_message_dict = db_cursor.fetchall()
    print(len(http_message_dict))
    print("select done")

    modify_list = list()

    apk_package = dict()
    for apk in apkmetadata_dict:
        if apk["APKName"] not in apk_package:
            apk_package[apk["APKName"]] = apk["packageName"]

    for http_message in http_message_dict:
        if http_message["packageName"] in apk_package:
            packageName = apk_package[http_message["packageName"]]
            four_tuple_hash = "+".join([packageName, http_message["four_tuple_hash"].split("+")[1]])
            four_tuple_hash_re = "+".join([packageName, http_message["four_tuple_hash_re"].split("+")[1]])
            modify_list.append([packageName, four_tuple_hash, four_tuple_hash_re, http_message["id"]])
            # print(modify_list)


    try:
        update_sql = "UPDATE HTTP set packageName=%s, four_tuple_hash=%s, four_tuple_hash_re=%s where id=%s"
        db_cursor.executemany(update_sql, modify_list)
        db_connection.commit()
    except Exception as e:
        print(e)
        db_connection.rollback()

    db_connection.close()


if __name__ == "__main__":
    execute_sql()
