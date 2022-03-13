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

    four_tuple_hash_list = list()
    select_sql = "SELECT id, packageName, srcAddr, dstAddr, srcPort, dstPort FROM Stack"
    db_cursor.execute(select_sql)
    results = db_cursor.fetchall()
    print("select done")
    print(len(results))
    for i in results:

        four_tuple_hash = "-".join([
            str(i["srcAddr"]),
            str(i["dstAddr"]),
            str(i["srcPort"]),
            str(i["dstPort"]),
        ])
        four_tuple_hash = "+".join([
            str(i["packageName"]),
            four_tuple_hash
        ])
        four_tuple_hash_list.append([four_tuple_hash, i['id']])

    try:
        update_sql = "UPDATE Stack set four_tuple_hash=%s where id=%s"
        db_cursor.executemany(update_sql, four_tuple_hash_list)
        db_connection.commit()
    except Exception as e:
        print(e)
        db_connection.rollback()

    db_connection.close()


if __name__ == "__main__":
    execute_sql()
